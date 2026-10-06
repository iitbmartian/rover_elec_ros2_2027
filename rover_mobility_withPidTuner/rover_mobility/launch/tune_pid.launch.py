import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # TODO: replace with your actual package name
    pkg_share = get_package_share_directory('rover_mobility')
    default_params = os.path.join(pkg_share, 'config', 'params.yaml')

    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=default_params,
        description='Full path to the params.yaml for tune_pid'
    )

    node = Node(
        package='rover_mobility',   # <-- your package name
        executable='tune_pid',      # <-- must match entry_points in setup.py
        name='tune_pid',            # <-- must match the key in params.yaml
        output='screen',
        parameters=[LaunchConfiguration('params_file')],
    )

    return LaunchDescription([
        params_file_arg,
        node,
    ])
