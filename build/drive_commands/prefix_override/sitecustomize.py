import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ritvik/Documents/MRT_ROS_WS/install/drive_commands'
