# Node ID
RPI = 0
FR = 1
FL = 2
BR = 3
BL = 4

# Message Types
explicit_quad = 0b00000
explicit_magn = 0b00001
explicit_imu = 0b00010
explicit_acs = 0b00011
drive_quad = 0b00100
drive_acs = 0b00101
explicit_pwm = 0b00110
drive_pwm = 0b00111
explicit_dirn = 0b01000
drive_dirn = 0b01001
status = 0b01010
heartbeat = 0b11111

def make_arbitration_id(node, msg):
    # node should be 6 bit, msg should be 5 bit, arbid is 11 bit
    return (node << 5 | msg)

def decode_id(arb_id):
    # node is 6 bits, msg is 5 bits, input should be an 11 bit arbid
    node = (arb_id >> 5) & 0b00111111
    msg = arb_id & 0b00011111
    return (node, msg)


"""
setting up vcan for testing:
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
ip link show vcan0 {to check whether its up}
"""
