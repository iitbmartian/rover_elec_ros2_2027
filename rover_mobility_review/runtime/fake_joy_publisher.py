#!/usr/bin/env python3
"""Publishes a scripted sequence of synthetic /joy messages to stress-test.

harness_node.py's joystick handling (mirrors mobility_node.py's real
joystick_callback logic) with: neutral, full forward/reverse, full
rotate left/right, a crab toggle, simultaneous throttle+rotate+crab, rapid
reversals, and a short/malformed axes array to exercise the safe_axis
fallback-to-0.0 path.
"""
import sys
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy


def make_joy(axes, buttons=None):
    msg = Joy()
    msg.axes = axes
    msg.buttons = buttons if buttons is not None else [0] * 12
    return msg


# axes layout assumed by mobility_node.py: [0]=turn, [2]=LT, [5]=RT (SDL/XInput: rest=-1)
NEUTRAL = [0.0, 0.0, -1.0, 0.0, 0.0, -1.0]
FULL_FORWARD = [0.0, 0.0, -1.0, 0.0, 0.0, 1.0]
FULL_REVERSE = [0.0, 0.0, 1.0, 0.0, 0.0, -1.0]
FULL_LEFT = [-1.0, 0.0, -1.0, 0.0, 0.0, 1.0]
FULL_RIGHT = [1.0, 0.0, -1.0, 0.0, 0.0, 1.0]
SIMULTANEOUS_EXTREME = [1.0, 0.0, 1.0, 0.0, 0.0, 1.0]  # turn + throttle both maxed
SHORT_AXES = [0.0, 0.0]  # malformed: too few axes for indices 2/5


SCRIPT = [
    ('neutral', NEUTRAL, None, 1.0),
    ('full_forward', FULL_FORWARD, None, 1.0),
    ('full_reverse', FULL_REVERSE, None, 1.0),
    ('full_left_rotate', FULL_LEFT, None, 1.0),
    ('full_right_rotate', FULL_RIGHT, None, 1.0),
    ('crab_toggle_on', NEUTRAL, [0] * 9 + [1] + [0] * 2, 0.2),
    ('crab_toggle_off', NEUTRAL, [0] * 9 + [1] + [0] * 2, 0.2),
    ('simultaneous_extreme', SIMULTANEOUS_EXTREME, None, 1.0),
    ('rapid_reversal_1', FULL_FORWARD, None, 0.1),
    ('rapid_reversal_2', FULL_REVERSE, None, 0.1),
    ('rapid_reversal_3', FULL_FORWARD, None, 0.1),
    ('rapid_reversal_4', FULL_REVERSE, None, 0.1),
    ('short_malformed_axes', SHORT_AXES, None, 1.0),
    ('back_to_neutral', NEUTRAL, None, 1.0),
]


def main():
    rclpy.init()
    node = Node('fake_joy_publisher')
    pub = node.create_publisher(Joy, '/joy', 10)

    for label, axes, buttons, hold_s in SCRIPT:
        node.get_logger().info(f'publishing /joy stage: {label}')
        msg = make_joy(list(axes), buttons)
        end_time = time.time() + hold_s
        while time.time() < end_time:
            pub.publish(msg)
            rclpy.spin_once(node, timeout_sec=0.02)
            time.sleep(0.02)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    sys.exit(main())
