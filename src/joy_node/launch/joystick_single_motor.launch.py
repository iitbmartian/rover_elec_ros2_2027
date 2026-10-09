"""Joystick direct-velocity test with a SINGLE BLDC (ODrive) attached.

Drives one of shoulder / elbow from the joystick over CAN, through can_controller
(no odrive python lib). Only this ODrive is initialised and streamed to; the other
ODrive and the linear base get no traffic unless include_base:=true.

Usage (after `colcon build --packages-select joy_node && source install/setup.bash`):

  ros2 launch joy_node joystick_single_motor.launch.py                       # shoulder (node 6)
  ros2 launch joy_node joystick_single_motor.launch.py motor:=elbow          # elbow (node 7)
  ros2 launch joy_node joystick_single_motor.launch.py motor:=shoulder node_id:=0
                                                    # bench ODrive still at CAN node id 0
  ros2 launch joy_node joystick_single_motor.launch.py motor:=elbow axis:=2  # use joystick axis 2
  ros2 launch joy_node joystick_single_motor.launch.py include_base:=true    # also drive the base
  ros2 launch joy_node joystick_single_motor.launch.py idle_on_exit:=false   # see safety notes

Arguments:
  motor           'shoulder' (ODrive node 6) or 'elbow' (node 7). Default shoulder.
  node_id         Override the CAN node id of that ODrive (default -1 = use the YAML id).
  axis            Override the joystick axis for that motor (default -2 = use the YAML).
  include_base    'true' also streams the linear base (node 8). Default false.
  idle_on_exit    'true' sets the axis idle when this node shuts down; 'false' leaves it in
                  closed loop at zero velocity. Use false for a gravity-loaded joint, or it
                  can drop. Default true.
  config_file     Mapping yaml (default: installed joy_node/config/joystick_mapping.yaml,
                  source src/joy_node/config/joystick_mapping.yaml). max_vel for the joint is
                  in motor turns/s: lower it before the first test.
  joy_device_id   Joystick index for the `joy` driver (default 0).

Behaviour: after launch the node resends clear-errors / velocity mode / closed loop to the
ODrive until its heartbeat reports closed loop with no error, then streams Set_Input_Vel at
the configured rate while the deadman button is held. Joy silence or releasing the deadman
sends zero velocity. If no heartbeat arrives within 3 s it warns (check wiring, bitrate, node id).

Hardware checklist:
  * can_controller currently opens `vcan0` (hardcoded in can_controller.py). For real
    hardware you must temporarily change `channel` there to `can0` (it will become a
    launch parameter later).
  * Bring the interface up at the ODrive's configured baud rate (ODrive default is
    250000; check can.config.baud_rate):
        sudo ip link set can0 up type can bitrate 250000
        ip -details link show can0
  * `candump can0` should show heartbeats (0x0C1 for node 6, 0x0E1 for node 7).
  * The ODrive needs its CAN node id set (6 shoulder / 7 elbow, or use node_id:=), a
    ready encoder, and vel_limit above max_vel.
  * Do NOT run odrive_can, arm_ik, base_can, or arm_brakes alongside this. Engaged
    physical brakes will hold the joint.
  * For a dry run without hardware use vcan0 and `candump vcan0`.
"""
from typing import List

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    motor = LaunchConfiguration('motor')
    include_base = LaunchConfiguration('include_base')

    # ['<motor>'] or ['<motor>', 'base']
    joints = PythonExpression(["['", motor, "'] + (['base'] if '", include_base, "'.lower() == 'true' else [])"])

    return LaunchDescription([
        DeclareLaunchArgument('motor', default_value='shoulder',
                              description="'shoulder' (node 6) or 'elbow' (node 7)"),
        DeclareLaunchArgument('node_id', default_value='-1', description='override ODrive CAN node id'),
        DeclareLaunchArgument('axis', default_value='-2', description='override joystick axis'),
        DeclareLaunchArgument('include_base', default_value='false'),
        DeclareLaunchArgument('idle_on_exit', default_value='true'),
        DeclareLaunchArgument('config_file', default_value='',
                              description='Mapping yaml; empty = installed joy_node/config/joystick_mapping.yaml'),
        DeclareLaunchArgument('joy_device_id', default_value='0'),

        Node(package='joy', executable='joy_node', name='joy',
             parameters=[{'device_id': ParameterValue(LaunchConfiguration('joy_device_id'), value_type=int)}]),
        Node(package='can_controller', executable='can_controller'),
        Node(package='joy_node', executable='joy_velocity',
             parameters=[{
                 'config_file': LaunchConfiguration('config_file'),
                 'joints': ParameterValue(joints, value_type=List[str]),
                 'node_id_override': ParameterValue(LaunchConfiguration('node_id'), value_type=int),
                 'axis_override': ParameterValue(LaunchConfiguration('axis'), value_type=int),
                 'idle_on_exit': ParameterValue(LaunchConfiguration('idle_on_exit'), value_type=bool),
             }]),
    ])
