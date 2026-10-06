import rclpy
from rclpy.node import Node
from can_interfaces.msg import CanMessage
from can_interfaces.msg import BLDCPositionCommand
import can_controller.arbitration_id as arb

import can
import threading
import struct
import time

# ODrive S1 heartbeat frames (7 bytes):
#   bytes 0-3: Axis_Error (uint32 bitfield, 0 = no error)
#   byte  4:   Axis_State (uint8, 8 = CLOSED_LOOP_CONTROL)
#   byte  5:   Procedure_Result (uint8, 0 = SUCCESS)
#   byte  6:   Trajectory_Done_Flag (uint8)
AXIS_STATE_CLOSED_LOOP_CONTROL = 8
PROCEDURE_RESULT_SUCCESS = 0

class ODriveCan(Node):
    def __init__(self):
        super().__init__("ODrive_CAN")

        self.pos1 = 0
        self.pos2 = 0
        self.vel1 = 0
        self.vel2 = 0

        self.bldc1 = arb.BLDC1
        self.bldc2 = arb.BLDC2

        # per-axis heartbeat state, refreshed on every heartbeat (not latched)
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

    def arm_position_command(self, msg):
        with self.check_lock:
            if self.axis_ready(0) and self.axis_ready(1):
                self.pos1 = msg.pos1
                self.pos2 = msg.pos2
                self.vel1 = msg.vel1
                self.vel2 = msg.vel2

                # Vel_FF/Torque_FF are int16, scaled by input_vel_scale/
                # input_torque_scale (default 1000, i.e. 0.001 rev/s and
                # 0.001 Nm per LSB). placo has no torque output, so
                # Torque_FF stays zero; Vel_FF reuses placo's rad/s value
                # as-is (best-guess units, same deferred-units call as pos1/pos2).
                vel1_ff = max(-32768, min(32767, round(self.vel1 * 1000)))
                vel2_ff = max(-32768, min(32767, round(self.vel2 * 1000)))

                self.send_to_bus(self.bldc1, arb.set_input_pos, data=list(struct.pack('<fhh',self.pos1,vel1_ff,0)))
                self.send_to_bus(self.bldc2, arb.set_input_pos, data=list(struct.pack('<fhh',self.pos2,vel2_ff,0)))

    def arm_initializer(self):
        # step 1. set to closed loop control
        self.send_to_bus(self.bldc1, arb.set_axis_state, data=list(struct.pack('<I',8)))
        self.send_to_bus(self.bldc2, arb.set_axis_state, data=list(struct.pack('<I',8)))

        # step 2. set to position control
        self.send_to_bus(self.bldc1, arb.set_controller_mode, data=list(struct.pack('<II',3,1)))
        self.send_to_bus(self.bldc2, arb.set_controller_mode, data=list(struct.pack('<II',3,1)))

        # step 3. check if step 1 worked
        while True:
            with self.check_lock:
                if(self.axis_ready(0) and self.trigger_init_msg_once[0]):
                    self.get_logger().info("bldc 1 initialized")
                    self.trigger_init_msg_once[0] = 0

                if(self.axis_ready(1) and self.trigger_init_msg_once[1]):
                    self.get_logger().info("bldc 2 initialized")
                    self.trigger_init_msg_once[1] = 0

                if(self.axis_ready(0) and self.axis_ready(1)): break

            time.sleep(0.1)

    def received_callback(self, msg: CanMessage):
        node = msg.nodeid
        msgtype = msg.msgtype
        data = msg.data

        for i, bldc_node in enumerate([self.bldc1, self.bldc2]):
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



