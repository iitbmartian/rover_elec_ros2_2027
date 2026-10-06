import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('rover_mobility')
    default_params = os.path.join(pkg_share, 'config', 'params.yaml')
    launch_dir = os.path.join(pkg_share, 'launch')

    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=default_params,
        description='Full path to params.yaml (mobility_node + tune_pid keys)'
    )
    # PID calibration is opt-in, not part of normal driving - see
    # mobility_node.py's "PID calibration" docstring section. Launch it
    # separately when you actually need to (re)tune:
    #   ros2 launch rover_mobility tune_pid.launch.py
    # or pass launch_tuner:=true here to start both together.
    launch_tuner_arg = DeclareLaunchArgument(
        'launch_tuner',
        default_value='false',
        description='Set to true to also start tune_pid alongside mobility_node'
    )

    mobility_node = Node(
        package='rover_mobility',
        executable='mobility_node',   # must match entry_points in setup.py
        name='mobility_node',          # must match the key in params.yaml
        output='screen',
        parameters=[LaunchConfiguration('params_file')],
    )

    tuner_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'tune_pid.launch.py')
        ),
        launch_arguments={'params_file': LaunchConfiguration('params_file')}.items(),
        condition=IfCondition(LaunchConfiguration('launch_tuner')),
    )

    return LaunchDescription([
        params_file_arg,
        launch_tuner_arg,
        mobility_node,
        tuner_launch,
    ])
