import rclpy
from rclpy.node import Node
from can_interfaces.msg import CanMessage
from can_interfaces.msg import BasePositionCommand
from can_interfaces.msg import BasePosition
import can_controller.arbitration_id as arb

import struct

class BaseCan(Node):
    def __init__(self):
        super().__init__('Base_CAN')

        self.base_pos = 0

        self.can_bus = self.create_publisher(CanMessage, 'can_bus_to_controller', 10)
        self.can_msg_received = self.create_subscription(CanMessage, 'can_messages_received', self.received_callback, 10)
        self.base_commands = self.create_subscription(BasePositionCommand, 'base_commands', self.base_command_callback, 10)
        self.base_position_pub = self.create_publisher(BasePosition, 'base_position', 10)

    def base_command_callback(self, msg):
        self.base_vel = msg.velocity

        can_msg = CanMessage()

        can_msg.nodeid = arb.Base
        can_msg.msgtype = arb.base_vel_command

        can_msg.data = list(struct.pack('<f', self.base_vel))

        self.can_bus.publish(can_msg)

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

        if node == arb.Base:
            if msgtype == arb.base_position_fb:
                self.base_pos = struct.unpack('<f', bytes(x & 0xFF for x in data[0:4]))[0]

                base_pos_msg = BasePosition()    
                base_pos_msg.position = self.base_pos
                self.base_position_pub.publish(base_pos_msg)

        
def main(args = None):
    rclpy.init(args=args)
    node = BaseCan()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



