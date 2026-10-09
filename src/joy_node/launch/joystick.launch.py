from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    mode = LaunchConfiguration('mode')
    config_file = LaunchConfiguration('config_file')
    ik = IfCondition(PythonExpression(["'", mode, "' == 'ik'"]))
    velocity = IfCondition(PythonExpression(["'", mode, "' == 'velocity'"]))

    return LaunchDescription([
        DeclareLaunchArgument('mode', default_value='ik', description="'ik' (end-effector velocity) or 'velocity' (direct joint velocity)"),
        DeclareLaunchArgument('config_file', default_value='', description='Mapping yaml; empty = installed joy_node/config/joystick_mapping.yaml'),
        DeclareLaunchArgument('joy_device_id', default_value='0'),

        Node(package='joy', executable='joy_node', name='joy', parameters=[{'device_id': ParameterValue(LaunchConfiguration('joy_device_id'), value_type=int)}]),
        Node(package='can_controller', executable='can_controller'),

        # IK mode: joy -> master_arm_command -> arm_ik -> odrive_can / base_can
        Node(package='joy_node', executable='joy_translator', condition=ik,
             parameters=[{'config_file': config_file}]),
        Node(package='arm_control', executable='arm_ik', condition=ik),
        Node(package='can_controller', executable='odrive_can', condition=ik),
        Node(package='can_controller', executable='base_can', condition=ik),

        # Direct velocity mode: joy -> CAN. odrive_can/arm_ik must NOT run (they force position mode).
        Node(package='joy_node', executable='joy_velocity', condition=velocity,
             parameters=[{'config_file': config_file}]),
    ])
