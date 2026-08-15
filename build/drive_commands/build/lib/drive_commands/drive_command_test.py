import rclpy
from rclpy.node import Node
from can_interfaces.msg import DriveCommand

class DriveCommandTest(Node):
    def __init__(self):
        super().__init__('DriveCommandTest')

        timer_period = 1
        self.drive_command_msg = DriveCommand()
        self.i = 1
        self.set_message()

        self.drive_command_pub = self.create_publisher(DriveCommand, 'drive_command', 10)
        self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        if(self.i + 3 >= 256): self.i = 1
        self.set_message()
        self.drive_command_pub.publish(self.drive_command_msg)
        self.get_logger().info("incremented i")
        self.i += 1

    def set_message(self):
        self.drive_command_msg.drive_pwm = [self.i, self.i+1, self.i+2, self.i+3]
        self.drive_command_msg.drive_direction = [True, True, False, False]
        self.drive_command_msg.explicit_pwm = list(reversed([self.i, self.i+1, self.i+2, self.i+3]))
        self.drive_command_msg.explicit_direction = list(reversed([True, True, False, False]))

def main(args = None):
    rclpy.init(args=args)
    node = DriveCommandTest() 

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()