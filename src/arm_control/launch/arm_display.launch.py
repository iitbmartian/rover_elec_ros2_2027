import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    urdf_path = os.path.join(
        get_package_share_directory('arm_urdf_files'), 'urdf', 'robot.urdf')
    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    rviz_config_path = os.path.join(
        get_package_share_directory('arm_control'), 'rviz', 'arm_display.rviz')

    use_gui = LaunchConfiguration('use_gui')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_gui', default_value='false',
            description=(
                'true: drive joints by hand with joint_state_publisher_gui sliders '
                '(no arm_ik needed). false: mirror the live arm_position_commands '
                'topic via joint_state_bridge.')),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            condition=IfCondition(use_gui),
        ),
        Node(
            package='arm_control',
            executable='joint_state_bridge',
            condition=UnlessCondition(use_gui),
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config_path],
        ),
    ])
