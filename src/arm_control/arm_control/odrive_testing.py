import rclpy
from rclpy.node import Node
from can_interfaces.msg import BLDCPositionCommand

class ODriveTest(Node):
    def __init__(self):
        super().__init__('ODriveTest')
        self.timer = self.create_timer(1, self.timer_cb)

        self.v1 = 0.25
        self.v2 = 0.75

        self.position_publish = self.create_publisher(BLDCPositionCommand, 'arm_position_commands', 10)

    def timer_cb(self):
        posCmd = BLDCPositionCommand()
        posCmd.pos1 = self.v1
        posCmd.pos2 = self.v2

        self.v1 = 1-self.v1
        self.v2 = 1-self.v2

        self.position_publish.publish(posCmd)
        self.get_logger().info(f'published {self.v1}')
        self.get_logger().info(f'published {self.v2}')

def main(args = None):
    rclpy.init(args=args)
    node = ODriveTest()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



