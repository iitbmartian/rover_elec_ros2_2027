import rclpy
from rclpy.node import Node
from can_interfaces.msg import CanMessage
from can_interfaces.msg import BLDCPositionCommand
import can_controller.arbitration_id as arb

import threading
import struct
import time
import math

# heartbeat (0x001) -> 7 bytes of useful stuff -> bytes 0-3 => Axis_Error (0 = no error)
#                                       byte 4 => Axis_State (e.g. 8 = closed loop control)
#                                       byte 5 => Procedure_Result (0 = success)
#                                       byte 6 => Trajectory_Done_Flag (0=false, 1=true)

AXIS_STATE_CLOSED_LOOP_CONTROL = 8
PROCEDURE_RESULT_SUCCESS = 0

# Set_Controller_Mode values (payload '<II' control_mode, input_mode)
CONTROL_MODE_VELOCITY = 2
CONTROL_MODE_POSITION = 3
INPUT_MODE_PASSTHROUGH = 1

# BLDCPositionCommand is in joint radians / rad-s. The ODrives work in motor turns, so every
# outgoing value is converted with:
#   motor_turns = direction * joint_rad * gear_ratio / (2*pi) + zero_offset_turns
# gear_ratio = motor turns per joint turn (shoulder 100:1, elbow 50:1). zero_offset/direction
# assume ODrive position 0 == URDF joint 0 with the same positive direction until calibrated.

class ODriveCan(Node):
    def __init__(self):
        super().__init__("ODrive_CAN")

        self.pos1 = 0
        self.pos2 = 0
        self.vel1 = 0
        self.vel2 = 0

        self.bldc1 = arb.BLDC1
        self.bldc2 = arb.BLDC2

        # 1 = bldc1 (shoulder), 2 = bldc2 (elbow). Default is both; set e.g. [1] to
        # bring up the pipeline with only one ODrive attached.
        self.declare_parameter('active_axes', [1, 2])

        active = set(self.get_parameter('active_axes').value)
        self.active = [1 in active, 2 in active]
        if not any(self.active):
            raise ValueError("active_axes must contain 1 and/or 2")

        self.declare_parameter('gear_ratios', [100.0, 50.0])       # [shoulder, elbow]
        self.declare_parameter('zero_offsets_turns', [0.0, 0.0])   # motor turns at joint 0
        self.declare_parameter('directions', [1.0, 1.0])           # +1 / -1
        self.gear_ratios = list(self.get_parameter('gear_ratios').value)
        self.zero_offsets = list(self.get_parameter('zero_offsets_turns').value)
        self.directions = list(self.get_parameter('directions').value)

        # control mode last sent to each ODrive (arm_initializer starts them in position mode)
        self.control_mode = [CONTROL_MODE_POSITION, CONTROL_MODE_POSITION]

        self.axis_error = [0, 0]
        self.axis_state = [0, 0]
        self.procedure_result = [0, 0]
        self.was_ready = [False, False]
        self.trigger_init_msg_once = [1,1]

        self.check_lock = threading.Lock()

        self.can_bus = self.create_publisher(CanMessage, 'can_bus_to_controller', 10)
        self.can_msg_received = self.create_subscription(CanMessage, 'can_messages_received', self.received_callback, 10)
        self.odrive_cmd_received = self.create_subscription(BLDCPositionCommand, 'arm_position_commands', self.arm_position_command, 10)

        self.arm_initializer = threading.Thread(target=self.arm_initializer, daemon=True)
        self.arm_initializer.start()

    def send_to_bus(self, nodeid, msgtype, data):
        can_message = CanMessage()
        can_message.nodeid = nodeid
        can_message.msgtype = msgtype
        can_message.data = data
        self.can_bus.publish(can_message)

    def axis_ready(self, i):
        return (self.axis_state[i] == AXIS_STATE_CLOSED_LOOP_CONTROL
                and self.axis_error[i] == 0
                and self.procedure_result[i] == PROCEDURE_RESULT_SUCCESS)

    def all_active_ready(self):
        return all(self.axis_ready(i) for i in range(2) if self.active[i])

    def joint_to_motor_turns(self, i, rad):
        return self.directions[i] * rad * self.gear_ratios[i] / (2 * math.pi) + self.zero_offsets[i]

    def joint_to_motor_turns_per_s(self, i, rad_s):
        return self.directions[i] * rad_s * self.gear_ratios[i] / (2 * math.pi)

    def set_control_mode(self, i, node, mode):
        # only sent when the commanded mode changes, so position <-> velocity switching is free
        if self.control_mode[i] != mode:
            self.send_to_bus(node, arb.set_controller_mode,
                             data=list(struct.pack('<II', mode, INPUT_MODE_PASSTHROUGH)))
            self.control_mode[i] = mode

    def arm_position_command(self, msg):
        with self.check_lock:
            if not self.all_active_ready():
                return

            self.pos1 = msg.pos1
            self.pos2 = msg.pos2
            self.vel1 = msg.vel1
            self.vel2 = msg.vel2

            for i, (node, pos, vel) in enumerate(((self.bldc1, self.pos1, self.vel1),
                                                  (self.bldc2, self.pos2, self.vel2))):
                if not self.active[i]:
                    continue
                vel_turns = self.joint_to_motor_turns_per_s(i, vel)

                if msg.pos_vel:
                    # position control: Set_Input_Pos '<fhh' = pos [turns], Vel_FF, Torque_FF.
                    # Vel_FF is int16 scaled by input_vel_scale (1000 -> 0.001 turns/s per LSB);
                    # placo gives no torque, so Torque_FF = 0.
                    self.set_control_mode(i, node, CONTROL_MODE_POSITION)
                    vel_ff = max(-32768, min(32767, round(vel_turns * 1000)))
                    self.send_to_bus(node, arb.set_input_pos,
                                     data=list(struct.pack('<fhh', self.joint_to_motor_turns(i, pos), vel_ff, 0)))
                else:
                    # velocity control (joystick): Set_Input_Vel '<ff' = vel [turns/s], Torque_FF
                    self.set_control_mode(i, node, CONTROL_MODE_VELOCITY)
                    self.send_to_bus(node, arb.set_input_vel,
                                     data=list(struct.pack('<ff', vel_turns, 0.0)))

    def arm_initializer(self):
        nodes = [n for n, a in zip((self.bldc1, self.bldc2), self.active) if a]

        # step 1. set to closed loop control
        for n in nodes:
            self.send_to_bus(n, arb.set_axis_state, data=list(struct.pack('<I',8)))

        # step 2. set to position control
        for n in nodes:
            self.send_to_bus(n, arb.set_controller_mode, data=list(struct.pack('<II', CONTROL_MODE_POSITION, INPUT_MODE_PASSTHROUGH)))

        # step 3. check if step 1 worked
        while True:
            with self.check_lock:
                if(self.active[0] and self.axis_ready(0) and self.trigger_init_msg_once[0]):
                    self.get_logger().info("bldc 1 initialized")
                    self.trigger_init_msg_once[0] = 0

                if(self.active[1] and self.axis_ready(1) and self.trigger_init_msg_once[1]):
                    self.get_logger().info("bldc 2 initialized")
                    self.trigger_init_msg_once[1] = 0

                if self.all_active_ready(): break

            time.sleep(0.1)

    def received_callback(self, msg: CanMessage):
        node = msg.nodeid
        msgtype = msg.msgtype
        data = msg.data

        for i, bldc_node in enumerate([self.bldc1, self.bldc2]):
            if not self.active[i]:
                continue
            if node == bldc_node and msgtype == arb.heartbeat_odr:
                # data = [4 bytes Axis_Error, 1 byte Axis_State,
                #         1 byte Procedure_Result, 1 byte Trajectory_Done_Flag]
                if len(data) < 6:
                    continue

                with self.check_lock:
                    self.axis_error[i] = (data[0] & 0xFF) | ((data[1] & 0xFF) << 8) | ((data[2] & 0xFF) << 16) | ((data[3] & 0xFF) << 24)
                    self.axis_state[i] = data[4]
                    self.procedure_result[i] = data[5]

                    ready_now = self.axis_ready(i)
                    if self.was_ready[i] and not ready_now:
                        self.get_logger().warning(
                            f"bldc {i+1} no longer ready: axis_state={self.axis_state[i]} "
                            f"axis_error={self.axis_error[i]} procedure_result={self.procedure_result[i]}")
                    self.was_ready[i] = ready_now
        
def main(args = None):
    rclpy.init(args=args)
    node = ODriveCan()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



