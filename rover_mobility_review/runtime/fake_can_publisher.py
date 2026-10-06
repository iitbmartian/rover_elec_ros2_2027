#!/usr/bin/env python3
"""Publishes a scripted sequence of synthetic can_interfaces/msg/MobilityData.

messages on /review/can/mobility_data to stress-test harness_node.py's
CAN-telemetry handling: normal small deltas, encoder rollover across the
0/255 boundary, stalled/repeated values, and extreme glitch values.
"""
import sys
import time

import rclpy
from rclpy.node import Node

from can_interfaces.msg import MobilityData


def build_msg(mag, quad, imu, drive_quad):
    msg = MobilityData()
    for suf in ('fl', 'fr', 'bl', 'br'):
        setattr(msg, f'explicit_mag_{suf}', mag)
        setattr(msg, f'explicit_quad_{suf}', quad)
        setattr(msg, f'explicit_imu_{suf}', imu)
        setattr(msg, f'drive_quad_{suf}', drive_quad)
    return msg


SCRIPT = [
    ('normal_small_deltas', [(0, 0, 0, 0), (2, 2, 0, 3), (4, 4, 0, 6), (6, 6, 0, 9)]),
    ('rollover_forward', [(250, 250, 0, 65530), (5, 5, 0, 10), (10, 10, 0, 20)]),
    ('rollover_backward', [(5, 5, 0, 10), (250, 250, 0, 65530), (245, 245, 0, 65520)]),
    ('stalled_repeated', [(90, 90, 0, 1000)] * 5),
    ('extreme_glitch', [(2_000_000_000, -2_000_000_000, 500_000, -2_000_000_000)]),
]


def main():
    rclpy.init()
    node = Node('fake_can_publisher')
    pub = node.create_publisher(MobilityData, '/review/can/mobility_data', 10)

    for label, frames in SCRIPT:
        node.get_logger().info(f'publishing CAN stage: {label}')
        for mag, quad, imu, dquad in frames:
            pub.publish(build_msg(mag, quad, imu, dquad))
            rclpy.spin_once(node, timeout_sec=0.02)
            time.sleep(0.1)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    sys.exit(main())
