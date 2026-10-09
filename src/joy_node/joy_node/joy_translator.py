import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from general_interfaces.msg import MasterArmCommand
from general_interfaces.msg import MasterWristCommand
from joy_node.mapping import load_mapping, axis_value

class JoyTranslator(Node):
    def __init__(self):
        super().__init__('joy_translator')

        self.declare_parameter('config_file', '')
        self.cfg = load_mapping(self.get_parameter('config_file').value)['ik_mode']

        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.arm_cmd_pub = self.create_publisher(MasterArmCommand, 'master_arm_command', 10)
        self.wrist_cmd_pub = self.create_publisher(MasterWristCommand, 'master_wrist_commands', 10)

    def joy_callback(self, msg: Joy):
        c = self.cfg
        dz = c['deadzone']
        forward = axis_value(msg, c['axis_forward_back'], deadzone=dz)
        right = axis_value(msg, c['axis_left_right'], deadzone=dz)
        z_vel = axis_value(msg, c['axis_z'], deadzone=dz)
        roll = axis_value(msg, c['axis_wrist_roll'], deadzone=dz)
        pitch = axis_value(msg, c['axis_wrist_pitch'], deadzone=dz)
        max_xyz_vel = c['max_xyz_vel']
        max_wrist_vel = c['max_wrist_vel']
        forward_sign, right_sign, z_sign = c['forward_sign'], c['right_sign'], c['z_sign']

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
