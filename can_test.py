import rclpy
from rclpy.node import Node

import can
import time

channel = "can0"
interface = "socketcan"

class CAN_Test(Node):
    def __init__(self):
        super().__init__('CAN_Test')
        timer_period = 1e-1
        self.bus = can.interface.Bus(channel = channel, interface = interface)

        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        message = can.Message(arbitration_id=0b00000000000, is_extended_id=False, data=[0x00])
        try:
            self.bus.send(message)
            self.get_logger().info("transmission successful")
        except can.CanError: self.get_logger().error("can is fucking up")

    def destroy_node(self):
        self.get_logger().info("shutting down node")
        self.bus.shutdown()
        super().destroy_node()

def main(args = None):
    rclpy.init(args=args)
    node = CAN_Test()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()