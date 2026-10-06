#!/usr/bin/env python3
"""Standalone rclpy harness for stress-testing rover_mobility's control math live.

The real `mobility_node` executable cannot run at all (see runtime_log.md -
it crashes on import with `ImportError: cannot import name 'DriveCommand'
from 'can_interfaces.msg'`, and even the "corrected" `all_interfaces.msg`
import fails too - DriveCommand is never rosidl-built in either package).
Per this review's scope (report-only, no edits to rover_mobility's own
source), we cannot fix that import to get the real node running.

This harness reconstructs the REAL control loop instead: it imports the
actual, ROS-independent VroomVroom / ExplicitController / DriveController
classes plus MobilityNode's static helpers directly from the installed
rover_mobility package (unmodified), subscribes to /joy and a single
working can_interfaces/msg/MobilityData topic, runs the identical per-wheel
math every tick, and publishes results to a scratch topic instead of the
broken DriveCommand. It is a stress-test aid for the math under live ROS
timing, NOT a substitute for actually validating the real (currently
crashed) mobility_node executable.
"""
import sys

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray

import can_interfaces.msg as _can_msg

# Same in-memory shim as test/conftest.py: mobility_node.py does an
# unguarded top-level `from can_interfaces.msg import DriveCommand` that
# fails (see runtime_log.md) - patch the attribute so the module can be
# imported here too, purely to reach its pure-Python helpers/classes.
if not hasattr(_can_msg, 'DriveCommand'):

    class _StubDriveCommand:
        def __init__(self):
            self.pwm = []
            self.direction = []

    _can_msg.DriveCommand = _StubDriveCommand

from can_interfaces.msg import MobilityData  # noqa: E402

from rover_mobility.controllers.vroomvroom import VroomVroom  # noqa: E402
from rover_mobility.controllers.explicit_steer import (  # noqa: E402
    ExplicitController, deg_to_count, wrap_count_diff, COUNTS_PER_REV,
)
from rover_mobility.controllers.drive_pid import DriveController  # noqa: E402
from rover_mobility.mobility_node import MobilityNode, WHEEL_ORDER  # noqa: E402


class HarnessNode(Node):
    """Re-runs mobility_node.py's real per-tick math loop, without the parts that crash."""

    def __init__(self):
        super().__init__('rover_mobility_review_harness')

        self.dt = 0.01
        self.mag_offsets = [0.0, 0.0, 0.0, 0.0]
        self.steer_input_flip = [False, False, False, False]
        self.steer_output_flip = [False, False, False, False]
        self.vroom_output_flip = [False, False, False, False]
        self.drive_alignment_max_error_deg = 30.0

        self.vroom = VroomVroom(half_width=0.35, half_length=0.45, speed_scalar=250.0)
        self.steer_ctls = [ExplicitController(dt=self.dt) for _ in WHEEL_ORDER]
        self.drive_ctls = [DriveController(dt=self.dt) for _ in WHEEL_ORDER]

        self._latest_steer_z = [None] * 4
        self._new_steer_data = [False] * 4
        self._latest_drive_quad = [None] * 4

        self.joy_x = 0.0
        self.joy_y = 0.0
        self.crabby = False
        self._tick = 0
        self._last_pwms = None

        # single working topic carrying the real, unified MobilityData
        # message - NOT the unbuildable per-wheel MobilityDataFL/FR/BL/BR
        # scheme the real node expects (bug #3).
        self.create_subscription(MobilityData, '/review/can/mobility_data', self.can_receive, 10)
        self.create_subscription(Joy, '/joy', self.joystick_callback, 10)
        self.pub_state = self.create_publisher(Float32MultiArray, '/review/wheel_state_harness', 10)

        self.create_timer(self.dt, self.loop)
        self.get_logger().info('harness_node started - reconstructing mobility_node.py math live')

    def can_receive(self, msg):
        for i, name in enumerate(WHEEL_ORDER):
            suf = name.lower()
            mag = MobilityNode._get_field(msg, 'explicit_mag', suf)
            quad = MobilityNode._get_field(msg, 'explicit_quad', suf)
            imu = MobilityNode._get_field(msg, 'explicit_imu', suf)
            if mag is not None and quad is not None and imu is not None:
                angle = MobilityNode.format_magnetic_angle(self, float(mag), i)
                if self.steer_input_flip[i]:
                    angle = -angle
                self._latest_steer_z[i] = [angle, float(quad), float(imu)]
                self._new_steer_data[i] = True
            drive_quad = MobilityNode._get_field(msg, 'drive_quad', suf)
            if drive_quad is not None:
                self._latest_drive_quad[i] = int(drive_quad)

    def joystick_callback(self, joy_val):
        def safe_axis(idx):
            return joy_val.axes[idx] if idx < len(joy_val.axes) else 0.0

        def safe_button(idx):
            return joy_val.buttons[idx] if idx < len(joy_val.buttons) else 0

        L3 = safe_button(9)
        if L3 == 1:
            self.crabby = not self.crabby
        turning = safe_axis(0)
        lt_val = (safe_axis(2) + 1) / 2
        rt_val = (safe_axis(5) + 1) / 2
        throttle = rt_val - lt_val
        self.joy_x = turning
        self.joy_y = throttle

    def loop(self):
        if self.crabby:
            angles_deg, vels = self.vroom.smooooth_operatorrrr(self.joy_y, 0, self.joy_x)
        else:
            angles_deg, vels = self.vroom.smooooth_operatorrrr(self.joy_y, self.joy_x, 0)

        speed_scalar = self.vroom.speed_scalar or 1.0
        state_out = []
        pwms = []

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

            align_error_deg = abs(wrap_count_diff(target_count, steer_state[0])) * 360.0 / COUNTS_PER_REV
            align_scale = max(0.0, 1.0 - align_error_deg / self.drive_alignment_max_error_deg)
            target_pwm_gated = target_pwm * align_scale

            drive_pwm = None
            quad = self._latest_drive_quad[i]
            if quad is not None:
                drive_pwm = self.drive_ctls[i].step(target_direction, target_pwm_gated, quad)
            drive_pwm_val = drive_pwm if drive_pwm is not None else 0.0

            pwms.append((name, steer_pwm, drive_pwm_val))
            state_out.extend([
                float(steer_state[0]), float(steer_state[1]),
                float('nan') if z is None else float(z[0]),
                float('nan') if z is None else float(z[1]),
                float('nan') if z is None else float(z[2]),
                float(steer_pwm),
                float(drive_pwm) if drive_pwm is not None else float('nan'),
            ])

        self.pub_state.publish(Float32MultiArray(data=state_out))
        self._last_pwms = pwms
        self._tick += 1
        if self._tick % 50 == 0:
            parts = [f'[{n}] steer={sp:+.2f} drive={dp:+.2f}' for n, sp, dp in pwms]
            self.get_logger().info(f'tick {self._tick}: ' + '  '.join(parts))


def main():
    rclpy.init()
    node = HarnessNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    sys.exit(main())
