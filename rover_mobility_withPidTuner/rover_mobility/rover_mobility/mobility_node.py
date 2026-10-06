"""
Main ROS2 node for rover mobility, structured like drive_controller.py: this
node owns all ROS plumbing (subscriptions, publishers, timer); the classes
in controllers/ are plain importable objects with no ROS awareness of their
own, same pattern as controllers/vroomvroom.py.

Ported from the standalone rover_mobility package (rover_ws/src/rover_mobility)
with two additions on top of that package's own zero-reference calibration
feature:
  1. PID auto-tuning integration - publishes /telemetry and /pid_commands
     (what tune_pid.py needs to run its RLS system-ID + pole-placement
     gain computation) and subscribes /pid_gains (applies the results
     live). See the "PID calibration" section below.
  2. (inherited, unchanged in spirit from the base package) steering
     zero-reference calibration via zero_wheel_index/zero_all_wheels
     parameters - see _apply_zero().

Only one physical wheel (FL) is wired to real CAN sensors right now, but all
four ExplicitController/DriveController instances run every tick - the other
three just sit on stale/zero feedback until their CAN topics/types exist.
This is a real difference from a "compute 4, use 1" approach: it costs a bit
more CPU now but means adding wheel 2 later is "wire up its CAN topic", not
"go restructure single-instance state into per-wheel arrays".

Each wheel now has its OWN message type (MobilityDataFL/FR/BL/BR) - these
CANNOT all be subscribed on one shared topic name, ROS2 topics have exactly
one message type. Each wheel gets its own topic parameter. The three
non-FL message type imports are optional: if they don't exist yet in your
built can_interfaces package, this node still starts and runs fine on FL
alone, it just logs a warning and skips those subscriptions rather than
crashing on import.

PID calibration (the point of this "withPidTuner" package): whenever the
rover moves to a new surface (or otherwise needs a PID re-tune), run the
tuner alongside this already-running node - no code changes, no restart of
this node, just:
    ros2 launch rover_mobility tune_pid.launch.py
tune_pid.py immediately starts consuming this node's real /telemetry +
/pid_commands (all 4 wheels) and pushing live /pid_gains updates back,
which _pid_gains_cb() below applies to the real steer/drive PID objects -
same PID objects the control loop uses every tick, so a gain update takes
effect immediately. For a faster, cleaner one-shot identification instead
of continuous background auto-tuning, inject a test signal on one wheel/
loop via the tuner's /run_experiment service, e.g.:
    ros2 service call /run_experiment all_interfaces/srv/RunExperiment \
        "{wheel_index: 0, loop: 'pos', signal_type: 'step', duration_s: 5.0, amplitude: 50.0}"
Stop the tuner (Ctrl+C) once you're happy - this node keeps running
unaffected either way, holding whatever gains were last applied.

Steering zero-reference calibration: whenever a wheel's steering angle
needs re-zeroing at its current physical position (e.g. after a mechanical
reset, or just to confirm the mag/quad encoders agree), from any terminal:
    ros2 param set /mobility_node zero_wheel_index 0   # zero one wheel (0-3, WHEEL_ORDER index)
    ros2 param set /mobility_node zero_all_wheels true # zero all 4 at once
This sets mag_offsets[i]/quad_offsets[i] so both sensors read 0 at the
current position, and resets that wheel's EKF state to match immediately -
see _apply_zero().
"""
import time
from functools import partial

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import Float32MultiArray, Int8MultiArray
from sensor_msgs.msg import Joy
from can_interfaces.msg import DriveCommand
from all_interfaces.msg import TelemetryData, PidCommands, PidGains

from .controllers.vroomvroom import VroomVroom
from .controllers.explicit_steer import ExplicitController, deg_to_count, count_to_deg, wrap_count_diff, COUNTS_PER_REV
from .controllers.drive_pid import DriveController


def _try_import_msg(name):
    """Import a message type from can_interfaces.msg if it exists, else
    None. Lets this node run with only a subset of wheel message types
    actually built - see module docstring."""
    try:
        mod = __import__('can_interfaces.msg', fromlist=[name])
        return getattr(mod, name)
    except (ImportError, AttributeError):
        return None


# Single source of truth for wheel order, used for VroomVroom output
# indexing and every other per-wheel array below. FIXED - was previously
# ['FR','FL','BR','BL'], which mislabeled two wheels.
#
# ROOT CAUSE (this resolves the FR/BR/FL/BL ordering conflict flagged
# repeatedly earlier): VroomVroom's w1..w4 have a FIXED geometric pattern
# - w1=(+a,+b), w2=(+a,-b), w3=(-a,+b), w4=(-a,-b), i.e. RIGHT+FRONT,
# RIGHT+BACK, LEFT+FRONT, LEFT+BACK (a=half_width=x, b=half_length=y,
# standard x=right/y=forward). The label order must match that fixed
# pattern - RIGHT+BACK is unambiguously "BR", not "FL". Verified directly
# from the raw w-vectors and a full-range continuity sweep (zero
# discontinuities with this order; the previous order produced a genuine
# front/back role swap between left and right turns of equal magnitude -
# this was a real control bug, not just a display issue, since it swapped
# which physical wheel received which target). VroomVroom's own docstring
# claiming "FR, BL, FL, BR" turns out to be the wrong one.
WHEEL_ORDER = ['FR', 'BR', 'FL', 'BL']

# Per-wheel message type, keyed by name so subscription setup can loop over
# WHEEL_ORDER instead of four hand-written near-duplicate blocks. Any entry
# that fails to import is None - handled at subscription time below.
MSG_TYPES = {
    'FL': _try_import_msg('MobilityDataFL'),
    'FR': _try_import_msg('MobilityDataFR'),
    'BL': _try_import_msg('MobilityDataBL'),
    'BR': _try_import_msg('MobilityDataBR'),
}


class MobilityNode(Node):
    def __init__(self):
        super().__init__('mobility_node')

        self.declare_parameter('joy_topic', '/joy')
        self.declare_parameter('dt', 0.01)

        # per-wheel CAN topics - each wheel's message type is distinct, so
        # each needs its own topic name. Defaults assume a "_fl"/"_fr"/etc.
        # suffix convention; override per your actual CAN bridge setup.
        for name in WHEEL_ORDER:
            self.declare_parameter(f'can_topic_{name.lower()}', f'/can/mobility_data_{name.lower()}')

        # VroomVroom geometry / scaling
        self.declare_parameter('half_width', 0.35)
        self.declare_parameter('half_length', 0.45)
        self.declare_parameter('speed_scalar', 250.0)
        self.declare_parameter('r_scalar', 1.0)
        self.declare_parameter('deadzone', 0.0)

        # steering (explicit/EKF) - shared gains across all 4 wheels for now,
        # since only one wheel is physically calibrated. These are the
        # STARTING gains - once tune_pid.py is running, /pid_gains updates
        # override them live (see _pid_gains_cb).
        self.declare_parameter('steer_t_motor', 0.15)
        self.declare_parameter('steer_k_motor', 0.8)
        self.declare_parameter('steer_q_diag', [0.001, 0.01])
        self.declare_parameter('steer_r_diag', [0.05, 0.02, 0.01])
        self.declare_parameter('steer_pid_kp', 1.0)
        self.declare_parameter('steer_pid_ki', 0.0)
        # was 0.0 (no damping) - retuned via step-response sweep against
        # the SIMULATED plant (rover_sim.py/SteerPlant): kp=1.0, kd=0.15
        # gave zero overshoot, zero tail oscillation, ~0.8s settling.
        # This is a starting point, NOT a value trusted from real hardware
        # - the real motor's dynamics (tau, inertia, load) differ from the
        # simulated first-order-lag plant, so re-verify Kd against actual
        # step-response behavior once wired up, don't assume this transfers.
        # (Or just run the tuner instead of hand-verifying - that's the
        # whole point of this package.)
        self.declare_parameter('steer_pid_kd', 0.15)

        # drive - shared gains across all 4 wheels for now. Same note as
        # above: starting gains only, tune_pid.py's /pid_gains overrides
        # these live once it's running.
        self.declare_parameter('drive_max_ticks_per_dt', 50.0)
        self.declare_parameter('drive_tick_counter_bits', 16)
        self.declare_parameter('drive_pid_kp', 1.0)
        self.declare_parameter('drive_pid_ki', 0.0)
        self.declare_parameter('drive_pid_kd', 0.0)

        # per-wheel calibration. Defaults are placeholders, NOT the real
        # values from drive_controller.py (16.17/93.95/355.80/260.50) -
        # given the FR/BR/FL/BL ordering conflict noted above, reusing
        # those numbers under a possibly-different index would misapply
        # someone else's offset to the wrong wheel. Re-enter them
        # deliberately once you've confirmed which number belongs to which
        # physical corner (or use the zero_wheel_index calibration command
        # below instead of hand-editing these).
        self.declare_parameter('mag_offsets', [0.0, 0.0, 0.0, 0.0])
        # quad_offsets: same idea as mag_offsets but for the steering
        # quadrature reading (explicit_quad) - previously that channel had
        # no offset/zero-reference mechanism at all (raw ticks went
        # straight into the EKF). Added alongside the zero_wheel_index /
        # zero_all_wheels calibration command below - see its docstring.
        self.declare_parameter('quad_offsets', [0.0, 0.0, 0.0, 0.0])
        self.declare_parameter('steer_input_direction_flip', [False, False, False, False])
        self.declare_parameter('vroom_input_direction_flip', [False, False, False, False])
        self.declare_parameter('steer_output_direction_flip', [False, False, False, False])
        self.declare_parameter('vroom_output_direction_flip', [False, False, False, False])

        # joystick smoothing - same constants/shape as drive_controller.py
        self.declare_parameter('joy_x_acc', 0.5)
        self.declare_parameter('joy_y_acc', 2.0)

        # Drive power is scaled down while a wheel's steering angle is still
        # far from its target, ramping back to full power as it aligns -
        # standard swerve-drive technique to avoid driving while mid-turn.
        # Without this, a big abrupt VroomVroom re-steer (see rotate-axis
        # near-singularity) leaves wheels briefly pointed in very different
        # directions while still commanded to drive at full power, which is
        # what was producing the erratic/looping trajectory.
        self.declare_parameter('drive_alignment_max_error_deg', 30.0)

        # ─── Zero-reference calibration trigger (see _on_set_parameters /
        # _apply_zero below) ────────────────────────────────────────────
        # -1 = no zero pending. Set to a wheel's WHEEL_ORDER index (0-3) to
        # zero that wheel's steering angle reference right now:
        #   ros2 param set /mobility_node zero_wheel_index 0
        self.declare_parameter('zero_wheel_index', -1)
        # Same, but zeroes all 4 wheels at once:
        #   ros2 param set /mobility_node zero_all_wheels true
        self.declare_parameter('zero_all_wheels', False)

        self.joy_topic = self.get_parameter('joy_topic').value
        self.dt = self.get_parameter('dt').value

        self.mag_offsets = list(self.get_parameter('mag_offsets').value)
        self.quad_offsets = list(self.get_parameter('quad_offsets').value)
        self.steer_input_flip = list(self.get_parameter('steer_input_direction_flip').value)
        self.vroom_input_flip = list(self.get_parameter('vroom_input_direction_flip').value)
        self.steer_output_flip = list(self.get_parameter('steer_output_direction_flip').value)
        self.vroom_output_flip = list(self.get_parameter('vroom_output_direction_flip').value)

        for name, arr in (('mag_offsets', self.mag_offsets),
                           ('quad_offsets', self.quad_offsets),
                           ('steer_input_direction_flip', self.steer_input_flip),
                           ('vroom_input_direction_flip', self.vroom_input_flip),
                           ('steer_output_direction_flip', self.steer_output_flip),
                           ('vroom_output_direction_flip', self.vroom_output_flip)):
            if len(arr) != 4:
                raise ValueError(f"param '{name}' must have length 4, got {len(arr)}")

        self.vroom = VroomVroom(
            half_width=self.get_parameter('half_width').value,
            half_length=self.get_parameter('half_length').value,
            speed_scalar=self.get_parameter('speed_scalar').value,
            r_scalar=self.get_parameter('r_scalar').value,
            deadzone=self.get_parameter('deadzone').value,
        )

        steer_kwargs = dict(
            dt=self.dt,
            t_motor=self.get_parameter('steer_t_motor').value,
            k_motor=self.get_parameter('steer_k_motor').value,
            q_diag=self.get_parameter('steer_q_diag').value,
            r_diag=self.get_parameter('steer_r_diag').value,
            pid_kp=self.get_parameter('steer_pid_kp').value,
            pid_ki=self.get_parameter('steer_pid_ki').value,
            pid_kd=self.get_parameter('steer_pid_kd').value,
        )
        drive_kwargs = dict(
            dt=self.dt,
            max_ticks_per_dt=self.get_parameter('drive_max_ticks_per_dt').value,
            tick_counter_bits=self.get_parameter('drive_tick_counter_bits').value,
            pid_kp=self.get_parameter('drive_pid_kp').value,
            pid_ki=self.get_parameter('drive_pid_ki').value,
            pid_kd=self.get_parameter('drive_pid_kd').value,
        )
        self.steer_ctls = [ExplicitController(**steer_kwargs) for _ in WHEEL_ORDER]
        self.drive_ctls = [DriveController(**drive_kwargs) for _ in WHEEL_ORDER]

        # STATE
        self._latest_steer_z = [None] * 4     # [mag, quad, imu] per wheel, offsets applied
        self._latest_raw_mag = [None] * 4     # mag BEFORE mag_offsets subtraction - needed
        self._latest_raw_quad = [None] * 4    # quad BEFORE quad_offsets subtraction - needed
        # by _apply_zero() to set new offsets from the current physical
        # position rather than back-deriving them from the wrapped/offset
        # value (which is fiddlier and more wrap-edge-case-prone).
        self._new_steer_data = [False] * 4
        self._latest_drive_quad = [None] * 4
        self._logged_msg_fields = set()   # wheel names already introspected/logged
        self._pending_zero = set()   # wheel indices to zero on the next loop() tick

        self.add_on_set_parameters_callback(self._on_set_parameters)

        # joystick state, same shape/constants as drive_controller.py
        self.crabby = False
        self.L3 = 0
        self.joy_x = 0.0
        self.joy_y = 0.0
        self.joy_x_acc = self.get_parameter('joy_x_acc').value
        self.joy_y_acc = self.get_parameter('joy_y_acc').value
        self.drive_alignment_max_error_deg = self.get_parameter('drive_alignment_max_error_deg').value
        self.joy_t = time.perf_counter()
        self._joy_msg_count = 0

        self._tick = 0

        subscribed = []
        for i, name in enumerate(WHEEL_ORDER):
            msg_type = MSG_TYPES.get(name)
            if msg_type is None:
                self.get_logger().warn(
                    f'MobilityData{name} not found in can_interfaces.msg - skipping CAN '
                    f'subscription for wheel {name}. It will sit on zero/stale feedback '
                    f'until that message type is built and this node is restarted.'
                )
                continue
            topic = self.get_parameter(f'can_topic_{name.lower()}').value
            self.create_subscription(msg_type, topic, partial(self.can_receive, i), 10)
            subscribed.append(f'{name}@{topic}')

        self.create_subscription(Joy, self.joy_topic, self.joystick_callback, 10)

        self.pub_state = self.create_publisher(Float32MultiArray, '/wheel_state', 10)
        self.drive_command_pub = self.create_publisher(DriveCommand, 'drive_command', 10)
        # layout: 7 floats per wheel, in WHEEL_ORDER, concatenated -
        # [theta, omega, mag, quad, imu, steer_pwm, drive_pwm] x4 = 28 floats.
        # Consumers need to know this shape; it changed from the old
        # single-wheel 7-float layout.
        self.pub_steer_pwm = self.create_publisher(Int8MultiArray, '/can/explicit_topic', 10)
        self.pub_drive_pwm = self.create_publisher(Int8MultiArray, '/can/drive_topic', 10)

        # ─── PID auto-tuning integration ───────────────────────────────
        # /telemetry + /pid_commands are published every tick (same dt as
        # everything else here) - tune_pid.py's `Ts` param must match this
        # node's `dt` (see params.yaml) so its RLS/pole-placement math's
        # assumed sample period matches how often samples actually arrive.
        # Angles/pos_cmds/vel_cmds are already fully calibrated by this
        # node (mag_offsets, quad_offsets, flips all already applied) -
        # tune_pid.py's own mag_offsets/pos_flip params should stay neutral
        # (0.0/false) for this reason, see params.yaml comment.
        self.pub_telemetry = self.create_publisher(TelemetryData, '/telemetry', 10)
        self.pub_pid_commands = self.create_publisher(PidCommands, '/pid_commands', 10)
        self.create_subscription(PidGains, '/pid_gains', self._pid_gains_cb, 10)

        self.create_timer(self.dt, self.loop)

        self.get_logger().info(
            f'mobility_node started (joy_topic={self.joy_topic}, dt={self.dt}, '
            f'wheel_order={WHEEL_ORDER}, subscribed={subscribed})'
        )

    # ─────────────────────────────────────────────────────────────────────
    def _pid_gains_cb(self, msg: PidGains):
        """Applies tune_pid.py's latest gains to the SAME PID objects the
        control loop uses every tick - takes effect immediately, no
        restart needed. Indexed positionally against WHEEL_ORDER (tune_pid
        is expected to be configured with wheel_names matching WHEEL_ORDER
        exactly - see params.yaml); needs_manual[i] gates auto-apply per
        wheel per loop, same safety valve tune_pid.py already provides."""
        n = min(len(msg.pos_kp), 4)
        for i in range(n):
            if i < len(msg.needs_manual) and msg.needs_manual[i]:
                continue
            self.steer_ctls[i].pid.kp = float(msg.pos_kp[i])
            self.steer_ctls[i].pid.ki = float(msg.pos_ki[i])
            self.steer_ctls[i].pid.kd = float(msg.pos_kd[i])
            self.drive_ctls[i].pid.kp = float(msg.vel_kp[i])
            self.drive_ctls[i].pid.ki = float(msg.vel_ki[i])
            self.drive_ctls[i].pid.kd = float(msg.vel_kd[i])

    # ─────────────────────────────────────────────────────────────────────
    def _on_set_parameters(self, params):
        """Watches for zero_wheel_index / zero_all_wheels being set and
        queues the actual work for loop() to do - NOT done here directly,
        since calling self.set_parameters() (to reset the trigger back to
        its neutral value) from inside a parameter-set callback is
        reentrant and best avoided; loop() runs in a plain timer-callback
        context where that's safe."""
        for p in params:
            if p.name == 'zero_wheel_index':
                if p.value != -1 and not (0 <= p.value < 4):
                    return SetParametersResult(
                        successful=False,
                        reason='zero_wheel_index must be -1 (none) or 0-3'
                    )
                if 0 <= p.value < 4:
                    self._pending_zero.add(p.value)
            elif p.name == 'zero_all_wheels':
                if p.value:
                    self._pending_zero.update(range(4))
        return SetParametersResult(successful=True)

    def _apply_zero(self, i):
        """Re-zeroes wheel i's steering reference frame at its CURRENT
        physical position: mag_offsets[i] and quad_offsets[i] are set so
        both sensors read 0 right now, and the EKF's own running estimate
        is reset to match immediately rather than drifting there over
        several predict/update cycles."""
        raw_mag = self._latest_raw_mag[i]
        raw_quad = self._latest_raw_quad[i]
        if raw_mag is None or raw_quad is None:
            self.get_logger().warn(
                f'[{WHEEL_ORDER[i]}] zero requested but no CAN steering telemetry '
                f'received yet for this wheel - ignoring.'
            )
            return
        self.mag_offsets[i] = raw_mag
        self.quad_offsets[i] = raw_quad
        self.steer_ctls[i].x = np.zeros(2)
        self.steer_ctls[i].P = np.eye(2) * 1.0
        self.get_logger().info(
            f'[{WHEEL_ORDER[i]}] zeroed: mag_offset={raw_mag:.2f} quad_offset={raw_quad:.2f}'
        )

    def format_magnetic_angle(self, angle, i):
        real_angle = angle - self.mag_offsets[i]
        while real_angle > 180:
            real_angle -= 360
        while real_angle < -180:
            real_angle += 360
        return real_angle

    @staticmethod
    def _get_field(msg, base, suf):
        # Tries several candidate field-name spellings, in priority order:
        #   1. unsuffixed, as originally guessed (e.g. "explicit_mag")
        #   2. unsuffixed, "magn" spelling - mobility_can.py uses
        #      self.explicit_magn_vals internally, real evidence this may
        #      be the actual convention, not just a guess like the rest
        #   3-4. same two, with the old suffixed convention appended
        #      ("_fl" etc) in case wheel identity isn't fully encoded by
        #      the message type after all
        # If NONE of these match your real message, see can_receive()'s
        # field-introspection log below for the ground truth instead of
        # adding a 5th guess here.
        candidates = [base]
        if 'mag' in base and 'magn' not in base:
            candidates.append(base.replace('mag', 'magn'))
        candidates += [f'{c}_{suf}' for c in list(candidates)]

        for name in candidates:
            v = getattr(msg, name, None)
            if v is not None:
                return v
        return None

    def can_receive(self, i, msg):
        """Single callback for all 4 wheels, bound to its wheel index via
        functools.partial at subscription time - replaces 4 near-identical
        can_receiveFL/FR/BL/BR methods that would drift out of sync."""
        name = WHEEL_ORDER[i]
        suf = name.lower()

        # Logs the REAL field names on the first message per wheel, so you
        # can read off ground truth instead of me guessing a 3rd/4th
        # spelling. Check this log line against _get_field()'s candidates
        # above if telemetry still isn't matching.
        if name not in self._logged_msg_fields:
            self._logged_msg_fields.add(name)
            try:
                fields = msg.get_fields_and_field_types()
                self.get_logger().info(f'[{name}] MobilityData{name} actual fields: {fields}')
            except Exception as e:
                self.get_logger().warn(f'[{name}] could not introspect message fields: {e}')

        mag = self._get_field(msg, 'explicit_mag', suf)
        quad = self._get_field(msg, 'explicit_quad', suf)
        imu = self._get_field(msg, 'explicit_imu', suf)
        if mag is not None and quad is not None and imu is not None:
            self._latest_raw_mag[i] = float(mag)
            self._latest_raw_quad[i] = float(quad)
            angle = self.format_magnetic_angle(float(mag), i)
            if self.steer_input_flip[i]:
                angle = -angle
            quad_corrected = float(quad) - self.quad_offsets[i]
            self._latest_steer_z[i] = [angle, quad_corrected, float(imu)]
            self._new_steer_data[i] = True
        elif self._tick % 200 == 0:
            self.get_logger().warn(
                f'[{name}] steering telemetry field(s) not found '
                f'(mag={mag} quad={quad} imu={imu}) - check the field-names '
                f'log above against _get_field()\'s candidates.'
            )

        drive_quad = self._get_field(msg, 'drive_quad', suf)
        if drive_quad is not None:
            self._latest_drive_quad[i] = int(drive_quad)
        elif self._tick % 200 == 0:
            self.get_logger().warn(f'[{name}] drive_quad field not found on message.')

    # ─────────────────────────────────────────────────────────────────────
    def joystick_callback(self, joy_val):
        self._joy_msg_count += 1
        if self._joy_msg_count == 1:
            self.get_logger().info(
                f'First /joy message received on topic "{self.joy_topic}": '
                f'{len(joy_val.axes)} axes, {len(joy_val.buttons)} buttons. '
                f'axes={list(joy_val.axes)} buttons={list(joy_val.buttons)}'
            )
        elif self._joy_msg_count % 50 == 0:
            # confirms /joy is still arriving AND actually changing when you
            # move the stick - if this never changes, the topic is wired up
            # but the physical input isn't reaching it (wrong device, dead
            # stick, etc); if this log never appears at all, /joy isn't
            # being received - check `ros2 topic hz /joy` and joy_topic param
            self.get_logger().info(f'/joy axes={[round(a, 2) for a in joy_val.axes]}')

        def safe_axis(idx):
            if idx < len(joy_val.axes):
                return joy_val.axes[idx]
            if self._joy_msg_count == 1:
                self.get_logger().warn(
                    f'/joy message has only {len(joy_val.axes)} axes, expected index {idx} - '
                    f'using 0.0. Check your controller\'s actual axis layout.'
                )
            return 0.0

        def safe_button(idx):
            if idx < len(joy_val.buttons):
                return joy_val.buttons[idx]
            if self._joy_msg_count == 1:
                self.get_logger().warn(
                    f'/joy message has only {len(joy_val.buttons)} buttons, expected index {idx} - '
                    f'crab toggle disabled.'
                )
            return 0

        # same axes/button extraction as drive_controller.py's joystick_callback
        L3 = safe_button(9)
        if L3 == 1 and self.L3 == 0:
            self.crabby = not self.crabby
        self.L3 = L3

        # rotate sign verified via forward-kinematics analysis (not just
        # assumed): negative rotate -> confirmed LEFT turn under this
        # rover's wheel geometry. Standard SDL convention gives axis(0)=-1
        # when the stick is pushed left, so NO negation here gives
        # push-left -> negative rotate -> LEFT turn, matching intent.
        # A PREVIOUS version of this line had `-safe_axis(0)` based on an
        # earlier, flawed sign-check test - that was backwards. If your
        # controller's axis(0) convention differs from standard SDL, this
        # may need revisiting, but the kinematics side is now correct.
        turning = safe_axis(0)
        # LT/RT trigger axes. Standard SDL/XInput convention: rests at -1,
        # full press at +1 -> (axis+1)/2 gives 0 at rest, 1 fully pressed.
        # VERIFY empirically (print axes[2]/axes[5] while pressing) - this
        # varies by OS/driver, and the original (1-axis)/2 formula was
        # backwards under the standard convention.
        lt_val = (safe_axis(2) + 1) / 2
        rt_val = (safe_axis(5) + 1) / 2
        throttle = rt_val - lt_val

        now = time.perf_counter()
        max_delta_x = self.joy_x_acc * (now - self.joy_t)
        max_delta_y = self.joy_y_acc * (now - self.joy_t)
        delta_x = max(-max_delta_x, min(max_delta_x, turning - self.joy_x))
        delta_y = max(-max_delta_y, min(max_delta_y, throttle - self.joy_y))
        self.joy_x += delta_x
        self.joy_y += delta_y
        self.joy_t = now

    # ─────────────────────────────────────────────────────────────────────
    def loop(self):
        if self._pending_zero:
            for i in list(self._pending_zero):
                self._apply_zero(i)
            self._pending_zero.clear()
            # Reflect the new offsets back into the parameter server (so
            # `ros2 param get /mobility_node mag_offsets` shows the real
            # current calibration) and reset the trigger params to their
            # neutral values now that they've been handled.
            self.set_parameters([
                Parameter('mag_offsets', Parameter.Type.DOUBLE_ARRAY, self.mag_offsets),
                Parameter('quad_offsets', Parameter.Type.DOUBLE_ARRAY, self.quad_offsets),
                Parameter('zero_wheel_index', Parameter.Type.INTEGER, -1),
                Parameter('zero_all_wheels', Parameter.Type.BOOL, False),
            ])

        if self.crabby:
            angles_deg, vels = self.vroom.smooooth_operatorrrr(self.joy_y, 0, self.joy_x)
        else:
            angles_deg, vels = self.vroom.smooooth_operatorrrr(self.joy_y, self.joy_x, 0)

        speed_scalar = self.vroom.speed_scalar or 1.0
        steer_pwm_out = []
        drive_pwm_out = []
        state_out = []   # 7 floats per wheel, WHEEL_ORDER order - see publisher setup comment
        drive_command_msg = DriveCommand()   # local, rebuilt fresh every tick - not self.

        telemetry_angles = []   # for /telemetry - tune_pid.py's y(k) position signal
        telemetry_speed = []    # for /telemetry - tune_pid.py's y(k) velocity signal
        pid_pos_cmds = []       # for /pid_commands - tune_pid.py's u(k) for the pos loop
        pid_vel_cmds = []       # for /pid_commands - tune_pid.py's u(k) for the vel loop

        for i, name in enumerate(WHEEL_ORDER):
            angle_deg = angles_deg[i]
            vel = vels[i]
            if self.steer_output_flip[i]:
                angle_deg = -angle_deg
            if self.vroom_output_flip[i]:
                vel = -vel

            target_count = deg_to_count(angle_deg)
            drive_frac = max(-1.0, min(1.0, vel / speed_scalar))
            target_direction = 1.0 if drive_frac >= 0 else -1.0
            target_pwm = abs(drive_frac)

            z = self._latest_steer_z[i] if self._new_steer_data[i] else None
            self._new_steer_data[i] = False
            steer_pwm, steer_state = self.steer_ctls[i].step(target_count, z)
            steer_pwm_out.extend(self._to_pwm_bytes(steer_pwm))

            # scale drive power down while this wheel is still turning to
            # reach its target angle - see drive_alignment_max_error_deg
            # comment above. abs(...) since we only care about magnitude
            # of misalignment, not which way it's off.
            align_error_deg = abs(wrap_count_diff(target_count, steer_state[0])) * 360.0 / COUNTS_PER_REV
            align_scale = max(0.0, 1.0 - align_error_deg / self.drive_alignment_max_error_deg)
            target_pwm_gated = target_pwm * align_scale

            drive_pwm = None
            quad = self._latest_drive_quad[i]
            if quad is not None:
                drive_pwm = self.drive_ctls[i].step(target_direction, target_pwm_gated, quad)
            # None on first tick / no CAN data yet -> hold at zero rather
            # than fabricate a pwm from an undefined delta
            drive_pwm_val = drive_pwm if drive_pwm is not None else 0.0
            drive_pwm_out.extend(self._to_pwm_bytes(drive_pwm_val))

            state_out.extend([
                float(steer_state[0]), float(steer_state[1]),
                float('nan') if z is None else float(z[0]),
                float('nan') if z is None else float(z[1]),
                float('nan') if z is None else float(z[2]),
                float(steer_pwm),
                float(drive_pwm) if drive_pwm is not None else float('nan'),
            ])

            telemetry_angles.append(count_to_deg(steer_state[0]))
            telemetry_speed.append(self.drive_ctls[i].measured_ticks_per_dt)
            pid_pos_cmds.append(float(steer_pwm))
            pid_vel_cmds.append(float(drive_pwm_val))

            # BUG FIX #2: DriveCommand's direction fields are bool-typed in
            # the .msg (per the PyBool_Check assertion failure) - _to_pwm_bytes
            # returns a plain int(0/1) for use in Int8MultiArray, which is NOT
            # the same as a Python bool even though it's numerically 0 or 1.
            # Only the DriveCommand fields need the explicit bool() cast -
            # Int8MultiArray.data below still wants plain ints, untouched.
            drive_dir, drive_mag = self._to_pwm_bytes(drive_pwm_val)
            steer_dir, steer_mag = self._to_pwm_bytes(steer_pwm)
            drive_command_msg.drive_direction.append(bool(drive_dir))
            drive_command_msg.drive_pwm.append(drive_mag)
            drive_command_msg.explicit_direction.append(bool(steer_dir))
            drive_command_msg.explicit_pwm.append(steer_mag)

        self.pub_steer_pwm.publish(Int8MultiArray(data=steer_pwm_out))
        self.pub_drive_pwm.publish(Int8MultiArray(data=drive_pwm_out))

        msg = Float32MultiArray()
        msg.data = state_out
        self.pub_state.publish(msg)
        # BUG FIX: was `self.drive_command_msg.publish(self.drive_command_msg)`
        # - published ON the message instead of on the publisher, and
        # `self.drive_command_msg` never existed (the message was built as
        # a local variable above, not stored on self). Publisher is
        # self.drive_command_pub; the message to send is the local
        # drive_command_msg built this tick.
        self.drive_command_pub.publish(drive_command_msg)

        telemetry_msg = TelemetryData()
        telemetry_msg.angles = telemetry_angles
        telemetry_msg.speed = telemetry_speed
        self.pub_telemetry.publish(telemetry_msg)

        commands_msg = PidCommands()
        commands_msg.pos_cmds = pid_pos_cmds
        commands_msg.vel_cmds = pid_vel_cmds
        self.pub_pid_commands.publish(commands_msg)

        self._tick += 1
        if self._tick % 10 == 0:
            parts = []
            for i, name in enumerate(WHEEL_ORDER):
                theta = state_out[i * 7 + 0]
                spwm = state_out[i * 7 + 5]
                dpwm = state_out[i * 7 + 6]
                dpwm_str = '----' if dpwm != dpwm else f'{dpwm:+.2f}'  # NaN check
                parts.append(f"[{name}] est:{theta:5.1f}c spwm:{spwm:+.2f} dpwm:{dpwm_str}")
            print("\r" + "  ".join(parts) + "   ", end='', flush=True)

    @staticmethod
    def _to_pwm_bytes(pwm):
        pwm_count = max(-127, min(127, int(round(pwm * 127))))
        return [int(pwm_count > 0), abs(pwm_count)]


def main(args=None):
    rclpy.init(args=args)
    node = MobilityNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
