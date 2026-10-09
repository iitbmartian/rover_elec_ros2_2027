import os
import yaml
from ament_index_python.packages import get_package_share_directory


def default_config_path():
    return os.path.join(get_package_share_directory('joy_node'), 'config', 'joystick_mapping.yaml')


def load_mapping(path=''):
    with open(path or default_config_path()) as f:
        return yaml.safe_load(f)


def axis_value(msg, index, sign=1.0, deadzone=0.0):
    """Joy axis with sign and deadzone; 0.0 if disabled (-1) or out of range."""
    if index < 0 or index >= len(msg.axes):
        return 0.0
    v = msg.axes[index]
    return 0.0 if abs(v) < deadzone else sign * v
