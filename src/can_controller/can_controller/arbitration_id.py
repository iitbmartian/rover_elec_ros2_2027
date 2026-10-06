# Non ODrive Nodes

# TODOS:
# - Combine explicit and drive pwm into one message
# - sync ids with saiki stm setup
# - mobility limit switches


# Node ID
RPI = 0
FR = 1
FL = 2
BR = 3
BL = 4
Wrist = 5

# Message Types for mobility

motor_data = 0b00000 #exp quad, dr quad, exp curr, dr curr ---- 0 
sensor_data = 0b00001 #magnetic encoder and status, imu and status ---- 1
mobility_heartbeat = 0b00010 # send to saiki :)
mobility_heartbeated = 0b00110 # what i get back from mobility node
mobility_sensor_check = 0b00011 

explicit_pwm = 0b00111 #msg includes dirn then pwm, both combined ---- 6
drive_pwm = 0b01000 #msg includes dirn then pwm, both combined ---- 7
start_node = 0b10100
limit_switch = 0b01010

# 0b0000010110

# Message Types for wrist

wrist_command = 0b00000
wrist_sensor_data = 0b00001
wrist_heartbeat = 0b00010




def make_arbitration_id(node, msg):
    # node should be 6 bit, msg should be 5 bit, arbid is 11 bit
    return (node << 5 | msg)

def decode_id(arb_id):
    # node is 6 bits, msg is 5 bits, input should be an 11 bit arbid
    node = (arb_id >> 5) & 0b00111111
    msg = arb_id & 0b00011111
    return (node, msg)

def cast_to_arbid(id):
    return (id & 0b11111111111)

"""
setting up vcan for testing:
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
ip link show vcan0 {to check whether its up}
"""

"""
0 2 0
0 4 0
0 6 0
0 8 0
"""


# ODrive Nodes
# Node ID
BLDC1 = 6
BLDC2 = 7

# Message Types
heartbeat_odr = 0b00001
estop = 0b00010
get_error = 0b00011
rxsdo = 0b00100 # read / access / write to anything from flat_endpoints.json
txsdo = 0b00101 # response to txsdo
address = 0b00110
set_axis_state = 0b00111
encoder_estimates = 0b01001
set_controller_mode = 0b01011
set_input_pos = 0b01100 # 0CC#0000000000000000
set_input_vel = 0b01101
set_input_torque = 0b01110
reboot = 0b10110

# Linear Base
Base = 8

base_vel_command = 0b00000
base_position_fb = 0b00001
base_heartbeat = 0b00010
base_heartbeated = 0b00011