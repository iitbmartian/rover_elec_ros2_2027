import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from general_interfaces.msg import MasterArmCommand
from general_interfaces.msg import MasterWristCommand

axis_z = 3
axis_forward_back = 1
axis_left_right = 0
axis_wrist_roll = 5
axis_wrist_pitch = 6

forward_sign = 1.0
right_sign = 1.0
z_sign = 1.0

deadzone = 0.05
max_xyz_vel = 0.1  # m/s
max_wrist_vel = 0.1 # rad/s


def apply_deadzone(value):
    return 0.0 if abs(value) < deadzone else value


class JoyTranslator(Node):
    def __init__(self):
        super().__init__('joy_translator')

        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.arm_cmd_pub = self.create_publisher(MasterArmCommand, 'master_arm_command', 10)
        self.wrist_cmd_pub = self.create_publisher(MasterWristCommand, 'master_wrist_commands', 10)

    def joy_callback(self, msg: Joy):
        forward = apply_deadzone(msg.axes[axis_forward_back])
        right = apply_deadzone(msg.axes[axis_left_right])
        z_vel = apply_deadzone(msg.axes[axis_z])
        roll = apply_deadzone(msg.axes[axis_wrist_roll])
        pitch = apply_deadzone(msg.axes[axis_wrist_pitch])

        cmd_arm = MasterArmCommand()
        cmd_arm.pos_vel = False
        cmd_arm.x = forward_sign * forward * max_xyz_vel
        cmd_arm.y = right_sign * right * max_xyz_vel
        cmd_arm.z = z_sign * z_vel * max_xyz_vel

        # self.get_logger().info(str(cmd_arm))
        self.arm_cmd_pub.publish(cmd_arm)

        cmd_wrist = MasterWristCommand()
        cmd_wrist.pos_vel = False
        cmd_wrist.roll = roll * max_wrist_vel
        cmd_wrist.pitch = pitch * max_wrist_vel

        self.wrist_cmd_pub.publish(cmd_wrist)



def main(args=None):
    rclpy.init(args=args)
    node = JoyTranslator()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
