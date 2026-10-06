import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from can_interfaces.msg import BLDCPositionCommand
from can_interfaces.msg import BasePositionCommand
from general_interfaces.msg import MasterWristCommand

joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
publish_rate = 30  # Hz

# Todo:
# - Add working wrist position display from vels :(

class JointStateBridge(Node):
    def __init__(self):
        super().__init__('joint_state_bridge')

        self.positions = [0.0] * len(joint_names)

        self.arm_position_sub = self.create_subscription(BLDCPositionCommand, 'arm_position_commands', self.arm_position_callback, 10)
        self.base_velocity_sub = self.create_subscription(BasePositionCommand, 'base_commands', self.base_velocity_callback, 10)
        self.wrist_vels_sub = self.create_subscription(MasterWristCommand, 'master_wrist_commands', self.wrist_vels_callback, 10)

        self.joint_state_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(1.0 / publish_rate, self.publish_joint_states)

    def arm_position_callback(self, msg: BLDCPositionCommand):
        self.positions[1] = msg.pos1  # joint_2, shoulder
        self.positions[2] = msg.pos2  # joint_3, elbow

    def base_velocity_callback(self, msg: BasePositionCommand):
        self.positions[0] = msg.position  # joint_1, base

    def wrist_vels_callback(self, msg: MasterWristCommand):
        pass

    def publish_joint_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = joint_names
        msg.position = self.positions
        self.joint_state_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = JointStateBridge()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
