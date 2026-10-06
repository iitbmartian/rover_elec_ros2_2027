import rclpy
from rclpy.node import Node
from general_interfaces.msg import MasterArmCommand
from can_interfaces.msg import BLDCPositionCommand
from can_interfaces.msg import BasePositionCommand
from std_msgs.msg import Float32

import placo
import numpy as np
import os
from ament_index_python.packages import get_package_share_directory

# only the joystick control is implemented

class Arm_IK(Node):
    def __init__(self):
        super().__init__('Arm_IK')

        package_share_dir = get_package_share_directory('arm_urdf_files')
        self.urdf_path = os.path.join(package_share_dir, 'urdf', 'robot.urdf')

        self.max_base_vel = 0.1      # m/s, joint_1
        self.max_shoulder_vel = 0.5  # rad/s, joint_2
        self.max_elbow_vel = 0.5     # rad/s, joint_3
        self.control_rate = 40 # Hz
        self.dt = 1.0 / self.control_rate

        self.arm = placo.RobotWrapper(self.urdf_path, placo.Flags.ignore_collisions)
        self.arm.update_kinematics()

        self.arm.set_velocity_limit("joint_1", self.max_base_vel)
        self.arm.set_velocity_limit("joint_2", self.max_shoulder_vel)
        self.arm.set_velocity_limit("joint_3", self.max_elbow_vel)

        # joint limits from robot.urdf, used for manual clamping below.
        # joint_1 = rail, joint_2 = shoulder, joint_3 = elbow
        self.joint_limits = {
            "joint_1": (0.0, 0.5),
            "joint_2": (-3.1416, 0.0),
            "joint_3": (-3.0, 3.0),
        }

        self.solver = placo.KinematicsSolver(self.arm)
        self.solver.mask_fbase(True)
        self.solver.dt = self.dt
        
        self.solver.enable_joint_limits(False)
        self.solver.enable_velocity_limits(True)

        ee_pos_now = self.arm.get_T_world_frame("link_5")[:3, 3]
        self.position_task = self.solver.add_position_task("link_5", ee_pos_now)
        self.position_task.configure("ee_position", "soft", 1.0)

        self.target_world = ee_pos_now.copy()
        self.get_logger().info(str(ee_pos_now))
        self.velocity_ff = np.zeros(3)

        self.arm_cmd_sub = self.create_subscription(MasterArmCommand, 'master_arm_command', self.command_callback, 10)
        self.arm_position_command = self.create_publisher(BLDCPositionCommand, 'arm_position_commands', 10)
        self.base_velocity_command = self.create_publisher(BasePositionCommand, 'base_commands', 10)

        self.timer = self.create_timer(self.dt, self.control_loop)

    def command_callback(self, msg):
        x = msg.x 
        y = msg.y 
        z = msg.z 

        if msg.pos_vel:
            self.target_world = np.array([x,y,z])
            self.velocity_ff = np.zeros(3)
            self.get_logger().info("new position command for arm")
        else:
            self.velocity_ff = np.array([x,y,z])
            self.get_logger().info("new velocity command for arm")

    def control_loop(self):
        if np.any(self.velocity_ff):
            self.target_world = self.target_world + self.velocity_ff * self.dt

        self.position_task.target_world = self.target_world
        self.position_task.dtarget_world = self.velocity_ff

        self.arm.update_kinematics()

        self.get_logger().info(
            f"Current: {self.arm.get_T_world_frame('link_5')[:3, 3]}, "
            f"Target: {self.target_world}, "
            f"Velocity FF: {self.velocity_ff}"
        )   
        self.solver.solve(True)

        rail_vel = self.arm.get_joint_velocity("joint_1")
        shoulder = self.arm.get_joint("joint_2")
        elbow = self.arm.get_joint("joint_3")
        shoulder_vel = self.arm.get_joint_velocity("joint_2")
        elbow_vel = self.arm.get_joint_velocity("joint_3")

        shoulder = np.clip(shoulder, *self.joint_limits["joint_2"])
        elbow = np.clip(elbow, *self.joint_limits["joint_3"])

        out_BLDC = BLDCPositionCommand()
        out_BLDC.pos1 = shoulder
        out_BLDC.pos2 = elbow
        out_BLDC.vel1 = shoulder_vel
        out_BLDC.vel2 = elbow_vel

        self.arm_position_command.publish(out_BLDC)

        out_base = BasePositionCommand()    
        out_base.velocity = self.arm.get_joint_velocity("joint_1")
        out_base.position = self.arm.get_joint("joint_1")
        self.base_velocity_command.publish(out_base)

def main(args=None):
    rclpy.init(args=args)
    node = Arm_IK()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()


        



