"""shoulder_only_test: drive ONE ODrive (the shoulder) from ONE joystick axis.

Talks to the ODrive with the official `odrive` python package over CAN (no can_controller,
no hand-built CAN frames). Needs ODrive firmware >= 0.6.11 and `pip install --upgrade odrive`
(>= 0.6.11). Do not run arm_brakes, odrive_can or joy_velocity at the same time: they also talk
to this ODrive.

Behaviour
  * On start: connect, log and clear any old errors, set velocity control, enter
    CLOSED_LOOP_CONTROL and wait until the ODrive confirms it. The axis stays in closed loop the
    whole time; "stopped" means input_vel = 0, not IDLE.
  * GPIO `gpio_num` is HIGH by default. As soon as the stick leaves the deadzone, the GPIO goes
    LOW and then the velocity is sent. When the stick returns to centre, velocity 0 is sent at
    once and the GPIO goes HIGH again only after the command has been zero for
    `gpio_release_delay_s` (a short debounce, so the GPIO doesn't chatter).
  * Velocity is in MOTOR turns/s: cmd = axis_sign * max_vel * (stick, rescaled past deadzone).
    max_vel can be changed while running:
        ros2 param set /shoulder_only_test max_vel 1.0
    It is rejected if above the ODrive's own controller.config.vel_limit.
  * Joystick silence for `joy_timeout_s` (or deadman released, if a deadman button is set) acts
    as a zero command.

Fault detection (checked every control tick)
  * axis current_state != CLOSED_LOOP_CONTROL, non-zero active_errors, or non-zero
    disarm_reason -> fault. Error flags are decoded to names in the log.
  * Any exception talking to the ODrive (CAN unplugged, ODrive rebooted) -> fault.
  * ODrive watchdog (if watchdog_timeout_s > 0): enabled at runtime only, not saved to flash,
    and fed every tick. If this node hangs or dies, the ODrive drops itself to IDLE.
  On a fault the node sends velocity 0, sets the GPIO HIGH and requests IDLE (best effort), then
  stops. It does NOT clear errors and re-arm by itself; restart the node to recover.
  NOTE: if the node dies or the bus drops while the GPIO is LOW, nothing here can drive it
  HIGH again. The ODrive watchdog stops the motor, but the GPIO stays where it was.

Usage
  ros2 run joy joy_node &
  ros2 run arm_control shoulder_only_test --ros-args -p max_vel:=0.5 -p joy_axis:=1
"""

import threading
import time

import odrive
import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from sensor_msgs.msg import Joy

AXIS_STATE_IDLE = 1
AXIS_STATE_CLOSED_LOOP_CONTROL = 8
CONTROL_MODE_VELOCITY_CONTROL = 2
INPUT_MODE_PASSTHROUGH = 1
INPUT_MODE_VEL_RAMP = 2

# ODriveError flags (docs.odriverobotics.com, firmware 0.6.x), used to decode
# active_errors / disarm_reason
ODRIVE_ERRORS = {
    0x1: 'INITIALIZING',
    0x2: 'SYSTEM_LEVEL',
    0x4: 'TIMING_ERROR',
    0x8: 'MISSING_ESTIMATE',
    0x10: 'BAD_CONFIG',
    0x20: 'DRV_FAULT',
    0x40: 'MISSING_INPUT',
    0x100: 'DC_BUS_OVER_VOLTAGE',
    0x200: 'DC_BUS_UNDER_VOLTAGE',
    0x400: 'DC_BUS_OVER_CURRENT',
    0x800: 'DC_BUS_OVER_REGEN_CURRENT',
    0x1000: 'CURRENT_LIMIT_VIOLATION',
    0x2000: 'MOTOR_OVER_TEMP',
    0x4000: 'INVERTER_OVER_TEMP',
    0x8000: 'VELOCITY_LIMIT_VIOLATION',
    0x10000: 'POSITION_LIMIT_VIOLATION',
    0x20000: 'REQUESTED_CURRENT_TOO_HIGH',
    0x1000000: 'WATCHDOG_TIMER_EXPIRED',
    0x2000000: 'ESTOP_REQUESTED',
    0x4000000: 'SPINOUT_DETECTED',
    0x8000000: 'BRAKE_RESISTOR_DISARMED',
    0x10000000: 'THERMISTOR_DISCONNECTED',
    0x40000000: 'CALIBRATION_ERROR',
}


def decode_errors(code):
    if not code:
        return 'none'
    names = [name for bit, name in ODRIVE_ERRORS.items() if code & bit]
    unknown = code & ~sum(ODRIVE_ERRORS)
    if unknown:
        names.append(f'UNKNOWN({unknown:#x})')
    return f'{code:#x} [' + ', '.join(names) + ']'


class ShoulderOnlyTest(Node):
    def __init__(self):
        super().__init__('shoulder_only_test')

        # connection / ODrive setup (read once at start)
        self.declare_parameter('serial_number', '')        # '' = first ODrive found
        self.declare_parameter('interface', 'can:can0')
        self.declare_parameter('gpio_num', 9)
        self.declare_parameter('watchdog_timeout_s', 0.5)  # 0 = don't touch the ODrive watchdog
        self.declare_parameter('vel_ramp_rate', 0.0)       # motor turns/s^2; 0 = passthrough
        self.declare_parameter('closed_loop_timeout_s', 3.0)
        self.declare_parameter('idle_on_exit', True)
        self.declare_parameter('rate_hz', 25.0)
        # joystick (the joy_node log shows 6 axes, 12 buttons)
        self.declare_parameter('joy_axis', 1)
        self.declare_parameter('deadman_button', -1)       # -1 = no deadman
        self.declare_parameter('joy_timeout_s', 0.5)
        # adjustable while running
        self.declare_parameter('max_vel', 3.0)             # motor turns/s at full stick
        self.declare_parameter('axis_sign', 1.0)
        self.declare_parameter('deadzone', 0.05)
        self.declare_parameter('gpio_release_delay_s', 0.1)

        p = lambda name: self.get_parameter(name).value  # noqa: E731
        self.serial_number = p('serial_number')
        self.interface = p('interface')
        self.gpio_num = p('gpio_num')
        self.watchdog_timeout = p('watchdog_timeout_s')
        self.vel_ramp_rate = p('vel_ramp_rate')
        self.closed_loop_timeout = p('closed_loop_timeout_s')
        self.idle_on_exit = p('idle_on_exit')
        self.joy_axis = p('joy_axis')
        self.deadman_button = p('deadman_button')
        self.joy_timeout = p('joy_timeout_s')
        self.max_vel = p('max_vel')
        self.axis_sign = p('axis_sign')
        self.deadzone = p('deadzone')
        self.gpio_release_delay = p('gpio_release_delay_s')
        self.period = 1.0 / p('rate_hz')

        if self.max_vel < 0.0:
            raise ValueError('max_vel must be >= 0')

        self.lock = threading.Lock()
        self.odrv = None
        self.state = 'connecting'    # connecting -> running -> fault
        self.vel_limit = None        # ODrive controller.config.vel_limit, read at connect
        self.watchdog_enabled = False

        self.joy_value = 0.0
        self.deadman_held = self.deadman_button < 0
        self.last_joy_time = None

        self.gpio_high = True
        self.last_moving_time = 0.0
        self.last_sent_vel = None

        self.add_on_set_parameters_callback(self.on_set_parameters)
        self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.timer = self.create_timer(self.period, self.control_loop)

        threading.Thread(target=self.connect_loop, daemon=True).start()

    # ------------------------------------------------------------------ params
    def on_set_parameters(self, params):
        for prm in params:
            if prm.name == 'max_vel':
                v = float(prm.value)
                if v < 0.0:
                    return SetParametersResult(successful=False, reason='max_vel must be >= 0')
                if self.vel_limit is not None and v > self.vel_limit:
                    return SetParametersResult(
                        successful=False,
                        reason=f'max_vel {v} > ODrive vel_limit {self.vel_limit} turns/s')
        for prm in params:
            if prm.name == 'max_vel':
                self.max_vel = float(prm.value)
                self.get_logger().info(f'max_vel set to {self.max_vel} turns/s')
            elif prm.name == 'axis_sign':
                self.axis_sign = float(prm.value)
            elif prm.name == 'deadzone':
                self.deadzone = float(prm.value)
            elif prm.name == 'gpio_release_delay_s':
                self.gpio_release_delay = float(prm.value)
        return SetParametersResult(successful=True)

    # ---------------------------------------------------------------- joystick
    def joy_callback(self, msg: Joy):
        self.last_joy_time = time.monotonic()
        if 0 <= self.joy_axis < len(msg.axes):
            self.joy_value = msg.axes[self.joy_axis]
        else:
            self.joy_value = 0.0
            self.get_logger().warning(
                f'joy_axis {self.joy_axis} out of range (joystick has {len(msg.axes)} axes)',
                throttle_duration_sec=5.0)
        if self.deadman_button >= 0:
            b = self.deadman_button
            self.deadman_held = b < len(msg.buttons) and msg.buttons[b] == 1

    def commanded_velocity(self, now):
        if self.last_joy_time is None or now - self.last_joy_time > self.joy_timeout:
            return 0.0
        if not self.deadman_held:
            return 0.0
        v = max(-1.0, min(1.0, self.joy_value))
        if abs(v) <= self.deadzone:
            return 0.0
        # rescale so the output ramps from 0 at the deadzone edge to 1 at full stick
        mag = (abs(v) - self.deadzone) / (1.0 - self.deadzone) if self.deadzone < 1.0 else 0.0
        return self.axis_sign * self.max_vel * mag * (1.0 if v > 0 else -1.0)

    # -------------------------------------------------------------- connection
    def connect_loop(self):
        while rclpy.ok():
            try:
                self.get_logger().info(
                    f"searching for ODrive {self.serial_number or '(any)'} on {self.interface}")
                odrv = odrive.find_sync(serial_number=self.serial_number or None,
                                        interfaces=[self.interface])
                self.setup_odrive(odrv)
            except Exception as e:
                self.get_logger().error(f'ODrive setup failed: {e}. Retrying in 1 s')
                time.sleep(1.0)
                continue
            with self.lock:
                self.odrv = odrv
                self.state = 'running'
            self.get_logger().info('ODrive in closed-loop velocity control, joystick active')
            return

    def setup_odrive(self, odrv):
        ax = odrv.axis0
        log = self.get_logger()

        if not odrv.set_gpio(self.gpio_num, True):
            raise RuntimeError(f'set_gpio({self.gpio_num}, True) returned False')
        self.gpio_high = True

        self.vel_limit = float(ax.controller.config.vel_limit)
        if self.max_vel > self.vel_limit:
            log.warning(f'max_vel {self.max_vel} > ODrive vel_limit {self.vel_limit}, clamping')
            self.max_vel = self.vel_limit

        old_err, old_disarm = ax.active_errors, ax.disarm_reason
        if old_err or old_disarm:
            log.warning(f'clearing old errors: active_errors={decode_errors(old_err)} '
                        f'disarm_reason={decode_errors(old_disarm)}')
        odrv.clear_errors()

        ax.controller.input_vel = 0.0
        ax.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        if self.vel_ramp_rate > 0.0:
            ax.controller.config.vel_ramp_rate = self.vel_ramp_rate
            ax.controller.config.input_mode = INPUT_MODE_VEL_RAMP
        else:
            ax.controller.config.input_mode = INPUT_MODE_PASSTHROUGH

        ax.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        deadline = time.monotonic() + self.closed_loop_timeout
        while ax.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            if time.monotonic() > deadline:
                raise RuntimeError(
                    f'did not enter closed loop: state={ax.current_state} '
                    f'procedure_result={ax.procedure_result} '
                    f'disarm_reason={decode_errors(ax.disarm_reason)}')
            time.sleep(0.05)

        if self.watchdog_timeout > 0.0:
            ax.config.watchdog_timeout = self.watchdog_timeout
            ax.watchdog_feed()
            ax.config.enable_watchdog = True
            ax.watchdog_feed()
            self.watchdog_enabled = True
            log.info(f'ODrive watchdog enabled ({self.watchdog_timeout} s, not saved to flash)')

    # ------------------------------------------------------------ control loop
    def control_loop(self):
        with self.lock:
            odrv, state = self.odrv, self.state
        if state != 'running':
            return

        t0 = time.monotonic()
        cmd = self.commanded_velocity(t0)
        moving = cmd != 0.0

        try:
            ax = odrv.axis0

            cur_state = ax.current_state
            err = ax.active_errors
            disarm = ax.disarm_reason
            if cur_state != AXIS_STATE_CLOSED_LOOP_CONTROL or err or disarm:
                self.fault(f'axis_state={cur_state} active_errors={decode_errors(err)} '
                           f'disarm_reason={decode_errors(disarm)}')
                return

            if moving:
                self.last_moving_time = t0
                if self.gpio_high:               # GPIO low first, then move
                    odrv.set_gpio(self.gpio_num, False)
                    self.gpio_high = False
                self.send_vel(ax, cmd)
            else:
                self.send_vel(ax, 0.0)           # stop now, GPIO high after the debounce
                if not self.gpio_high and t0 - self.last_moving_time >= self.gpio_release_delay:
                    odrv.set_gpio(self.gpio_num, True)
                    self.gpio_high = True

            if self.watchdog_enabled:
                ax.watchdog_feed()

        except Exception as e:
            self.fault(f'communication with ODrive failed: {e!r}')
            return

        dt = time.monotonic() - t0
        if dt > self.period:
            self.get_logger().warning(
                f'control tick took {dt*1000:.1f} ms (> {self.period*1000:.1f} ms period); '
                f'lower rate_hz', throttle_duration_sec=5.0)

    def send_vel(self, ax, vel):
        if vel != self.last_sent_vel:
            ax.controller.input_vel = vel
            self.last_sent_vel = vel

    # ------------------------------------------------------- fault / shutdown
    def fault(self, reason):
        with self.lock:
            if self.state == 'fault':
                return
            self.state = 'fault'
            odrv = self.odrv
        self.get_logger().error(f'FAULT: {reason}')
        self.safe_stop(odrv, idle=True)
        self.get_logger().error('motor stopped. Fix the cause, then restart this node to re-arm')

    def safe_stop(self, odrv, idle):
        """Best effort: velocity 0, GPIO high, optionally IDLE. Each step is tried even if one fails."""
        if odrv is None:
            return
        ax = odrv.axis0
        steps = [('input_vel=0', lambda: setattr(ax.controller, 'input_vel', 0.0)),
                 ('gpio high', lambda: odrv.set_gpio(self.gpio_num, True))]
        if idle:
            steps.append(('idle', lambda: setattr(ax, 'requested_state', AXIS_STATE_IDLE)))
        elif self.watchdog_enabled:
            # staying in closed loop after exit: the watchdog would IDLE it once we stop feeding
            steps.append(('disable watchdog', lambda: setattr(ax.config, 'enable_watchdog', False)))
        for name, step in steps:
            try:
                step()
            except Exception as e:
                self.get_logger().error(f'safe stop: {name} failed: {e!r}')
        self.gpio_high = True
        self.last_sent_vel = 0.0

    def shutdown(self):
        with self.lock:
            odrv, state = self.odrv, self.state
            self.state = 'fault'  # stop the control loop from doing anything else
        if state == 'running':
            self.get_logger().info('shutting down: stopping motor')
            self.safe_stop(odrv, idle=self.idle_on_exit)


def main(args=None):
    rclpy.init(args=args)
    node = ShoulderOnlyTest()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
