import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from can_interfaces.msg import DriveCommand
from can_interfaces.msg import MobilityData
import can_controller.arbitration_id as arb

import can
import time
import threading
import queue

bit_rate = 500000

channel = "vcan0"
interface = "socketcan"

# TODOS:
# 1. Do I want to zero the PWM at a certain point if drivecommands don't come for long enough?
# 2. I can probably make transmission more efficient by bundling the PWM and dirn values at least into one command since presumably those will 
#    always be sent together
# 3. Change the queueing system to not apply to current commands / state estimation stuff / etc. 
# 4. Add receiver code. -- added for encoder data from wheels

# Current way I am handling encoder data:
# Just maintaining arrays of most recently received values and publishing to encoder topic whenever
# any value changes- i.e. whenever I get new encoder data on the bus

class CAN_Controller(Node):
    def __init__(self):
        super().__init__('CAN_Controller')
              
        # array declarations and number of bits for all encoders 
        # order -> [FR, FL, BR, BL] (maintained subsequently also)
        
        self.explicit_quad_bits = 8
        self.explicit_magn_bits = 8
        self.explicit_imu_bits = 8
        self.explicit_acs_bits = 8
        self.drive_quad_bits = 8
        self.drive_acs_bits = 8

        # self.explicit_quad_vals = [[0]*self.explicit_quad_bits]*4
        # self.explicit_magn_vals = [[0]*self.explicit_magn_bits]*4
        # self.explicit_imu_vals = [[0]*self.explicit_imu_bits]*4
        # self.explicit_acs_vals = [[0]*self.explicit_acs_bits]*4
        # self.drive_quad_vals = [[0]*self.drive_quad_bits]*4
        # self.drive_acs_vals = [[0]*self.drive_acs_bits]*4

        self.explicit_quad_vals = [0]*4
        self.explicit_magn_vals = [0]*4
        self.explicit_imu_vals = [0]*4
        self.explicit_acs_vals = [0]*4
        self.drive_quad_vals = [0]*4
        self.drive_acs_vals = [0]*4

        # array declarations and number of bits for commands

        self.explicit_pwm_bits = 8
        self.drive_pwm_bits = 8
        self.explicit_dirn_bits = 8
        self.drive_dirn_bits = 8

        # self.explicit_pwm_vals = [[0]*self.explicit_pwm_bits]*4
        # self.drive_pwm_vals = [[0]*self.drive_pwm_bits]*4
        # self.explicit_dirn_vals = [[0]*self.explicit_dirn_bits]*4
        # self.drive_dirn_vals = [[0]*self.drive_dirn_bits]*4

        self.explicit_pwm_vals = [0]*4
        self.drive_pwm_vals = [0]*4
        self.explicit_dirn_vals = [0]*4
        self.drive_dirn_vals = [0]*4

        # self.statuscheck = [0]*4 # some sort of all ok check for each node

        while True:
            try: 
                self.bus = can.interface.Bus(channel=channel, interface=interface)
                self.get_logger().info("initialized CAN node")
                break
            except can.CanError: 
                self.get_logger().error("unable to start CAN")

        self.can_queue = queue.PriorityQueue()
        self.queue_counter = 0
        self.tx_thread = threading.Thread(target=self.can_from_queue, daemon=True)
        self.tx_thread.start()
        self.rx_thread = threading.Thread(target=self.can_receiver, daemon=True)
        self.rx_thread.start()

        self.drive_command = self.create_subscription(DriveCommand, 'drive_command', self.drive_command_callback, 10)
        self.encoder_data = self.create_publisher(MobilityData, 'encoder_data', 10)
        self.publisher_debug = self.create_publisher(Bool, 'bus_status', 10)

    def drive_command_callback(self, msg: DriveCommand):
        self.explicit_pwm_vals = list(msg.explicit_pwm)
        self.drive_pwm_vals = list(msg.drive_pwm)
        self.explicit_dirn_vals = list(msg.explicit_direction)
        self.drive_dirn_vals = list(msg.drive_direction)

        for i in range(4):
            self.transmit_message(i+1, arb.drive_pwm, self.drive_pwm_vals[i])
            self.transmit_message(i+1, arb.explicit_pwm, self.explicit_pwm_vals[i])
            self.transmit_message(i+1, arb.drive_dirn, self.drive_dirn_vals[i])
            self.transmit_message(i+1, arb.explicit_dirn, self.explicit_dirn_vals[i])

    def transmit_message(self, node, msg_type, data, priority = 5):
        arbid = arb.make_arbitration_id(node, msg_type)
        message = can.Message(arbitration_id = arbid, is_extended_id = False, data = [data & 0xFF])

        self.queue_counter += 1
        self.can_queue.put((priority, self.queue_counter, message))

    def destroy_node(self):
        self.bus.shutdown()
        super().destroy_node()

    def can_from_queue(self):
        while rclpy.ok():
            priority, counter_no, message = self.can_queue.get()

            try:
                self.bus.send(message)
                debug = Bool()
                debug.data = True
                self.publisher_debug.publish(debug)
                # self.get_logger().info(f"transmitted message {list(message.data)} on arb id {message.arbitration_id}")

            except can.CanError: self.get_logger().error(f"can't transmit message {list(message.data)} on arb id {message.arbitration_id}")
            finally: self.can_queue.task_done()

    def can_receiver(self):
        for msg in self.bus:
            node, msgtype = arb.decode_id(msg.arbitration_id)
            if(node in [1,2,3,4] and msgtype in [0,1,2,3,4,5]):
                BO = 'little'
                data_int = int.from_bytes(msg.data[0:4], byteorder='little', signed=True)
                if msgtype == 0:
                    self.explicit_quad_vals[node-1] = data_int
                if msgtype == 1:
                    self.explicit_magn_vals[node-1] = data_int
                if msgtype == 2:
                    self.explicit_imu_vals[node-1] = data_int   
                if msgtype == 3:
                    self.explicit_acs_vals[node-1] = data_int
                if msgtype == 4:
                    self.drive_quad_vals[node-1] = data_int
                if msgtype == 5:
                    self.drive_acs_vals[node-1] = data_int

                new_data = MobilityData()

                new_data.explicit_quad_fr = self.explicit_quad_vals[0]
                new_data.explicit_mag_fr = self.explicit_magn_vals[0]
                new_data.explicit_imu_fr = self.explicit_imu_vals[0]
                new_data.drive_quad_fr = self.drive_quad_vals[0]

                new_data.explicit_quad_fl = self.explicit_quad_vals[1]
                new_data.explicit_mag_fl = self.explicit_magn_vals[1]
                new_data.explicit_imu_fl = self.explicit_imu_vals[1]
                new_data.drive_quad_fl = self.drive_quad_vals[1]

                new_data.explicit_quad_br = self.explicit_quad_vals[2]
                new_data.explicit_mag_br = self.explicit_magn_vals[2]
                new_data.explicit_imu_br = self.explicit_imu_vals[2]
                new_data.drive_quad_br = self.drive_quad_vals[2]

                new_data.explicit_quad_bl = self.explicit_quad_vals[3]
                new_data.explicit_mag_bl = self.explicit_magn_vals[3]
                new_data.explicit_imu_bl = self.explicit_imu_vals[3]
                new_data.drive_quad_bl = self.drive_quad_vals[3]

                # The value goes from -128 to 127 looks like
            
                self.encoder_data.publish(new_data)
                self.get_logger().info(f"published new data {data_int} of type {msgtype} to node {node}")

def main(args = None):
    rclpy.init(args=args)
    node = CAN_Controller()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()