#!/usr/bin/env python3
"""
gripperrr.py

Direct word-for-word / contextual 'wrist' -> 'gripper' port of the
WristCan node, interfacing the gripper over CAN (no UART/serial code).
"""

import rclpy

from rclpy.node import Node
from can_interfaces.msg import CanMessage
from can_interfaces.msg import GripperPositionCommand
from can_interfaces.msg import GripperEncoders
import can_controller.arbitration_id as arb

# 1. get commands from some abstract topic for now
# 2. send straight to gripper node for processing there

class GripperCan(Node):
    def __init__(self):
        super().__init__('Gripper_CAN')

        # convention -> 0s is horizontal wrt gearbox and parallel to gearbox
        self.dcm1 = 0
        self.dcm2 = 0

        self.quad_1 = 0
        self.quad_2 = 0
        self.acs_1 = 0
        self.acs_2 = 0
        self.up_check = [0, 0, 0, 0]  # for encoders

        self.can_bus = self.create_publisher(CanMessage, 'can_bus_to_controller', 10)
        self.can_msg_received = self.create_subscription(CanMessage, 'can_messages_received', self.received_callback, 10)
        self.gripper_commands = self.create_subscription(GripperPositionCommand, 'gripper_command', self.gripper_command_callback, 10)
        self.gripper_encoders = self.create_publisher(GripperEncoders, 'gripper_encoders', 10)

    def gripper_command_callback(self, msg):
        self.dcm1 = msg.dcm1
        self.dcm2 = msg.dcm2
        self.send_to_bus(arb.Gripper, arb.gripper_command, [self.dcm1, self.dcm2])

    def send_to_bus(self, nodeid, msgtype, data):
        can_message = CanMessage()
        can_message.nodeid = nodeid
        can_message.msgtype = msgtype
        can_message.data = data
        self.can_bus.publish(can_message)

    def received_callback(self, msg):
        node = msg.nodeid
        msgtype = msg.msgtype
        data = msg.data

        if node == arb.Gripper:
            if msgtype == arb.sensor_data:
                if len(data) < 5:
                    self.get_logger().warn(
                        f'sensor_data frame from Gripper too short ({len(data)} bytes, need 5) - dropping'
                    )
                    return
                self.quad_1 = data[0]
                self.quad_2 = data[1]
                self.acs_1 = data[2]
                self.acs_2 = data[3]
                # Mask to 4 bits rather than formatting data[4] directly:
                # a signed/negative byte (e.g. CanMessage.data as int8[])
                # formats as e.g. '-011' via :04b, and int('-') on the sign
                # character raises ValueError, crashing this callback. `&
                # 0x0F` sidesteps sign entirely and also guarantees exactly
                # 4 bits/list entries regardless of the raw byte's value.
                self.up_check = [int(bit) for bit in f"{data[4] & 0x0F:04b}"]
                gripper_data = GripperEncoders()
                gripper_data.quad_1 = self.quad_1
                gripper_data.quad_2 = self.quad_2
                gripper_data.acs_1 = self.acs_1
                gripper_data.acs_2 = self.acs_2
                gripper_data.up_check = self.up_check

                self.gripper_encoders.publish(gripper_data)


def main(args=None):
    rclpy.init(args=args)
    node = GripperCan()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
