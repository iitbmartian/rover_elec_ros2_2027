import rclpy
from rclpy.node import Node
from general_interfaces.msg import ArmBrake

import threading
import time
import odrive
from odrive.enums import AxisState
from odrive.utils import request_state, dump_errors

# 1. Subscribe to some arm brake controller
# 2. Figure out how to control the arm brakes- just engage when movement is finished?

class ArmBrakes(Node):
    def __init__(self):
        super().__init__('Arm_Brakes')

        while True:
            try:
                self.odrv_1, self.odrv_2 = odrive.find_sync(["261832805677", "0"], interfaces=["can:can0"], timeout = 0.1)
                self.get_logger().info("odrives connected succesfully to brake controller node")
                break
            except TimeoutError:
                time.sleep(1)

        self.brake_1_engaged = 0
        self.brake_2_engaged = 0

        self.arm_brake_commands = self.create_subscription(ArmBrake, 'arm_brake_commands', self.brake_engage_callback, 10)

    def brake_engage_callback(self, msg):
        self.odrv_1.set_gpio(9, msg.brake1)
        self.odrv_2.set_gpio(9, msg.brake2)        

def main(args = None):
    rclpy.init(args=args)
    node = ArmBrakes()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

