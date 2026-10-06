import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from can_interfaces.msg import DriveCommand
from can_interfaces.msg import MobilityDataFL
from can_interfaces.msg import MobilityDataFR
from can_interfaces.msg import MobilityDataBL
from can_interfaces.msg import MobilityDataBR
from can_interfaces.msg import CanMessage
from std_msgs.msg import Int8MultiArray
import can_controller.arbitration_id as arb

import threading
import time
import random

# TODOS:
# 1. Do I want to zero the PWM at a certain point if drivecommands don't come for long enough?
# 3. Change the queueing system to not apply to current commands / state estimation stuff / etc. 
# 7. Publish current sensor values

# Current way I am handling encoder data:
# Just maintaining arrays of most recently received values and publishing to encoder topic whenever
# any value changes- i.e. whenever I get new encoder data on the bus

# Should move all publishers into one common thread publishing at fixed rate and only use the can receiver function to update values whenever they come.

# no need to use four diff message types for each encoder data topic

# send limit switch data on ls_fl, ls_fr, ... and it'll be two integers (0/1, 0/1)
# send sensor up data on sensor_check_fl, .. and it'll be two integers (mag, imu)
 
class MobilityCan(Node):
    def __init__(self):
        super().__init__("Mobility_CAN")

        # array declarations and number of bits for all encoders 
        # order -> [FR, FL, BR, BL] (maintained subsequently also)
        
        self.explicit_quad_bits = 8
        self.explicit_magn_bits = 8
        self.explicit_imu_bits = 8
        self.explicit_acs_bits = 8
        self.drive_quad_bits = 8
        self.drive_acs_bits = 8

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

        self.explicit_pwm_vals = [0]*4
        self.drive_pwm_vals = [0]*4
        self.explicit_dirn_vals = [0]*4
        self.drive_dirn_vals = [0]*4
        self.hb_reps = [0]*4
        self.statuscheck = [1]*4
        self.imu_check = [1]*4
        self.magn_check = [1]*4
        self.limswitch1 = [0]*4
        self.limswitch2 = [0]*4

        self.drive_command = self.create_subscription(DriveCommand, 'drive_command', self.drive_command_callback, 10)
        self.can_bus = self.create_publisher(CanMessage, 'can_bus_to_controller', 10)
        self.can_msg_received = self.create_subscription(CanMessage, 'can_messages_received', self.data_from_mobility, 10)
        # heartbeat replies arrive on their own topic and are handled in their own callback group,
        # so the (slow) encoder callback above can't delay or evict them
        self.hb_group = MutuallyExclusiveCallbackGroup()
        self.hb_sub = self.create_subscription(CanMessage, 'heartbeat_replies', self.heartbeat_reply_callback, 50, callback_group=self.hb_group)
        self.encoder_data_FL = self.create_publisher(MobilityDataFL, 'encoder_data_FL', 10)
        self.encoder_data_FR = self.create_publisher(MobilityDataFR, 'encoder_data_FR', 10)
        self.encoder_data_BL = self.create_publisher(MobilityDataBL, 'encoder_data_BL', 10)
        self.encoder_data_BR = self.create_publisher(MobilityDataBR, 'encoder_data_BR', 10)
        self.ls_fl = self.create_publisher(Int8MultiArray, 'ls_fl', 10)
        self.ls_fr = self.create_publisher(Int8MultiArray, 'ls_fr', 10)
        self.ls_bl = self.create_publisher(Int8MultiArray, 'ls_bl', 10)
        self.ls_br = self.create_publisher(Int8MultiArray, 'ls_br', 10)
        self.sensor_check_fl = self.create_publisher(Int8MultiArray, 'sensor_check_fl', 10)
        self.sensor_check_fr = self.create_publisher(Int8MultiArray, 'sensor_check_fr', 10)
        self.sensor_check_bl = self.create_publisher(Int8MultiArray, 'sensor_check_bl', 10)
        self.sensor_check_br = self.create_publisher(Int8MultiArray, 'sensor_check_br', 10)

        self.heartbeat_thread = threading.Thread(target=self.heartbeater, daemon=True)
        self.heartbeat_thread.start()
        self.publisher_thread = threading.Thread(target=self.pubthread, daemon=True)
        self.publisher_thread.start()

    def drive_command_callback(self, msg: DriveCommand):
        # assuming that first byte is dirn and second byte is pwm
        self.explicit_pwm_vals = list(msg.explicit_pwm)
        self.drive_pwm_vals = list(msg.drive_pwm)
        self.explicit_dirn_vals = list(msg.explicit_direction)
        self.drive_dirn_vals = list(msg.drive_direction)

        nodes = [arb.FR, arb.FL, arb.BR, arb.BL]
        for i in range(4):
            self.send_to_bus(nodes[i], arb.drive_pwm, [self.drive_dirn_vals[i],self.drive_pwm_vals[i]])
            self.send_to_bus(nodes[i], arb.explicit_pwm, [self.explicit_dirn_vals[i],self.explicit_pwm_vals[i]])

    def send_to_bus(self, nodeid, msgtype, data):
        can_message = CanMessage()
        can_message.nodeid = nodeid
        can_message.msgtype = msgtype
        can_message.data = data

        self.can_bus.publish(can_message)

    def heartbeater(self):
        while rclpy.ok():
            a = random.randint(0,252)
            b = random.randint(0,252)
            c = a+b

            nodes = [arb.FR, arb.FL, arb.BR, arb.BL]
            self.hb_reps = [-1]*4  # clear so a stale reply can't be mistaken for a fresh one
            for i in range(4): self.send_to_bus(nodes[i], arb.mobility_heartbeat, [a+i,b+i])

            time.sleep(0.1)
            for i in range(4):
                if(self.hb_reps[i] != c + 2*i): 
                    self.statuscheck[i] = 0
                    self.get_logger().info(f"Node {nodes[i]} may be screwed")
                else: self.statuscheck[i] = 1


    def heartbeat_reply_callback(self, msg: CanMessage):
        nodes = [arb.FR, arb.FL, arb.BR, arb.BL]
        if msg.msgtype == arb.mobility_heartbeated and msg.nodeid in nodes:
            data = bytes(x & 0xFF for x in msg.data)
            self.hb_reps[nodes.index(msg.nodeid)] = int.from_bytes(data[0:2], byteorder='little', signed=False)

    def data_from_mobility(self, msg: CanMessage):
        node = msg.nodeid
        msgtype = msg.msgtype
        # msg.data is array('i') (int32[]); bytes()/int.from_bytes on it would read
        # 4 raw bytes per element, so convert to real bytes (one byte per element) first.
        data = bytes(x & 0xFF for x in msg.data)

        # data_int = int.from_bytes(bytes(data[0:4]), byteorder='little', signed=True)
        nodes = [arb.FR, arb.FL, arb.BR, arb.BL]
        msgtypes = [arb.motor_data, arb.sensor_data, arb.mobility_sensor_check, arb.limit_switch]

        if(node in nodes and msgtype in msgtypes):
            if msgtype == arb.sensor_data or msgtype == arb.motor_data:
                if msgtype == arb.motor_data:
                    for i in range(4):
                        if(node == nodes[i]):
                            self.explicit_quad_vals[i] = int.from_bytes(data[0:2], byteorder='little', signed=True)
                            self.drive_quad_vals[i] = int.from_bytes(data[2:4], byteorder='little', signed=True)
                            self.explicit_acs_vals[i] = int.from_bytes(data[4:6], byteorder='little', signed=True)
                            self.drive_acs_vals[i] = int.from_bytes(data[6:8], byteorder='little', signed=True)

                if msgtype == arb.sensor_data:
                    for i in range(4):
                        if(node == nodes[i]):
                            self.explicit_magn_vals[i] = int.from_bytes(data[0:2], byteorder='little', signed=True)
                            self.imu_check[i] = data[2]
                            self.explicit_imu_vals[i] = int.from_bytes(data[3:5], byteorder='little', signed=True)
                            self.magn_check[i] = data[5]

            elif msgtype == arb.limit_switch:
                for i in range(4):
                    if(node == nodes[i]):
                        self.limswitch1[i] = data[0]
                        self.limswitch2[i] = data[1]

                        ls_msg = Int8MultiArray()
                        ls_msg.data = [self.limswitch1[i], self.limswitch2[i]]

                        if i==0: self.ls_fr.publish(ls_msg)
                        elif i==1: self.ls_fl.publish(ls_msg)
                        elif i==2: self.ls_br.publish(ls_msg)
                        elif i==3: self.ls_bl.publish(ls_msg)

            # comment this line out it'll just spam
            # self.get_logger().info(f"received new data {data} of type {msgtype} from node {node}")
    
    def pubthread(self):
        while rclpy.ok():
            new_data_FL = MobilityDataFL()
            new_data_FR = MobilityDataFR()
            new_data_BL = MobilityDataBL()
            new_data_BR = MobilityDataBR()

            sens_check_FL = Int8MultiArray()
            sens_check_FR = Int8MultiArray()
            sens_check_BL = Int8MultiArray()
            sens_check_BR = Int8MultiArray()

            sens_check_FR.data = [self.magn_check[0], self.imu_check[0]]
            sens_check_FL.data = [self.magn_check[1], self.imu_check[1]]
            sens_check_BR.data = [self.magn_check[2], self.imu_check[2]]
            sens_check_BL.data = [self.magn_check[3], self.imu_check[3]]
            
            new_data_FR.explicit_quad_fr = self.explicit_quad_vals[0]
            new_data_FR.explicit_mag_fr = self.explicit_magn_vals[0]
            new_data_FR.explicit_imu_fr = self.explicit_imu_vals[0]
            new_data_FR.drive_quad_fr = self.drive_quad_vals[0]

            new_data_FL.explicit_quad_fl = self.explicit_quad_vals[1]
            new_data_FL.explicit_mag_fl = self.explicit_magn_vals[1]
            new_data_FL.explicit_imu_fl = self.explicit_imu_vals[1]
            new_data_FL.drive_quad_fl = self.drive_quad_vals[1]

            new_data_BR.explicit_quad_br = self.explicit_quad_vals[2]
            new_data_BR.explicit_mag_br = self.explicit_magn_vals[2]
            new_data_BR.explicit_imu_br = self.explicit_imu_vals[2]
            new_data_BR.drive_quad_br = self.drive_quad_vals[2]

            new_data_BL.explicit_quad_bl = self.explicit_quad_vals[3]
            new_data_BL.explicit_mag_bl = self.explicit_magn_vals[3]
            new_data_BL.explicit_imu_bl = self.explicit_imu_vals[3]
            new_data_BL.drive_quad_bl = self.drive_quad_vals[3]

            # The value goes from -128 to 127 looks like (for one 8 bit signed message on the bus)
        
            self.encoder_data_FL.publish(new_data_FL)
            self.encoder_data_FR.publish(new_data_FR)
            self.encoder_data_BL.publish(new_data_BL)
            self.encoder_data_BR.publish(new_data_BR)

            self.sensor_check_fr.publish(sens_check_FR)
            self.sensor_check_fl.publish(sens_check_FL)
            self.sensor_check_br.publish(sens_check_BR)
            self.sensor_check_bl.publish(sens_check_BL)

            time.sleep(0.05)


def main(args = None):
    rclpy.init(args=args)
    node = MobilityCan()

    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try: executor.spin()
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



