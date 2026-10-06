import rclpy
from rclpy.node import Node
from can_interfaces.msg import CanMessage
from can_interfaces.msg import WristPositionCommand
from can_interfaces.msg import WristEncoders
import can_controller.arbitration_id as arb

import struct

class WristCan(Node):
    def __init__(self):
        super().__init__('Wrist_CAN')

        # convention -> ig positive can be clockwise looking out of the dc motor
        self.vel_l = 0
        self.vel_r = 0

        self.quad_1 = 0
        self.quad_2 = 0
        self.acs_1 = 0
        self.acs_2 = 0
        self.up_check = [0,0,0,0] # for encoders

        self.can_bus = self.create_publisher(CanMessage, 'can_bus_to_controller', 10)
        self.can_msg_received = self.create_subscription(CanMessage, 'can_messages_received', self.received_callback, 10)
        self.wrist_commands = self.create_subscription(WristPositionCommand, 'wrist_commands', self.wrist_command_callback, 10)
        self.wrist_encoders = self.create_publisher(WristEncoders, 'wrist_encoders', 10)

    def wrist_command_callback(self, msg):
        self.vel_l = msg.vel_l
        self.vel_r = msg.vel_r

        can_msg = CanMessage()

        can_msg.nodeid = arb.Wrist
        can_msg.msgtype = arb.wrist_command
        # vel_l/vel_r are float32 - CanMessage.data is int32[], one array
        # element per CAN payload byte, so pack to bytes and expand to a
        # list of ints (a bare `bytes`/struct.pack result gets reinterpreted
        # as int32 words on assignment, not one element per byte - see
        # INCOMPLETE_TASKS.md's "Suggestions" section)
        can_msg.data = list(struct.pack('<ff', self.vel_l, self.vel_r))

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

        if node == arb.Wrist:
            if msgtype == arb.sensor_data:
                self.quad_1 = data[0]
                self.quad_2 = data[1]
                self.acs_1 = data[2]
                self.acs_2 = data[3]
                self.up_check = [int(bit) for bit in f"{data[4]:04b}"]
        
                wrist_data = WristEncoders()
                wrist_data.quad_1 = self.quad_1
                wrist_data.quad_2 = self.quad_2
                wrist_data.acs_1 = self.acs_1
                wrist_data.acs_2 = self.acs_2
                wrist_data.up_check = self.up_check

                self.wrist_encoders.publish(wrist_data)

        
def main(args = None):
    rclpy.init(args=args)
    node = WristCan()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



