import rclpy
from rclpy.node import Node
from general_interfaces.msg import ArmBrake

import threading
import time
import odrive

# TODOS:
# 1. Nothing publishes arm_brake_commands yet - need some brake controller / policy node.
# 2. Figure out how to control the arm brakes- just engage when movement is finished?

# Each brake is handled completely independently: brake 1 (shoulder ODrive) and brake 2 (elbow
# ODrive) each have their own serial number parameter and their own connection thread. A missing
# or disconnected ODrive never blocks the other one; brake1/brake2 in ArmBrake only ever act on
# their own ODrive. A command that arrives before an ODrive is connected is remembered and applied
# as soon as that ODrive connects. An empty serial disables that brake.

BRAKE_NAMES = ('brake 1 (shoulder)', 'brake 2 (elbow)')


class ArmBrakes(Node):
    def __init__(self):
        super().__init__('Arm_Brakes')

        self.declare_parameter('serial_1', '261832805677')
        self.declare_parameter('serial_2', '')  # TODO: second ODrive's serial number
        self.declare_parameter('interface', 'can:can0')
        self.declare_parameter('brake_gpio', 9)
        self.declare_parameter('connect_timeout', 1.0)  # s, per find_sync attempt
        self.declare_parameter('retry_period', 1.0)     # s, between failed attempts

        self.serials = [self.get_parameter('serial_1').value, self.get_parameter('serial_2').value]
        self.interface = self.get_parameter('interface').value
        self.brake_gpio = self.get_parameter('brake_gpio').value
        self.connect_timeout = self.get_parameter('connect_timeout').value
        self.retry_period = self.get_parameter('retry_period').value

        self.odrv = [None, None]        # connected ODrive objects
        self.desired = [None, None]     # last requested state per brake (None = nothing requested yet)
        self.locks = [threading.Lock(), threading.Lock()]

        self.arm_brake_commands = self.create_subscription(ArmBrake, 'arm_brake_commands', self.brake_engage_callback, 10)

        for i in range(2):
            if not self.serials[i]:
                self.get_logger().warning(f"{BRAKE_NAMES[i]}: no serial number set, this brake is disabled")
                continue
            threading.Thread(target=self.connect_loop, args=(i,), daemon=True).start()

    def connect_loop(self, i):
        while rclpy.ok():
            try:
                odrv = odrive.find_sync(self.serials[i], interfaces=[self.interface], timeout=self.connect_timeout)
            except TimeoutError:
                self.get_logger().info(f"{BRAKE_NAMES[i]}: ODrive {self.serials[i]} not found yet, retrying",
                                       throttle_duration_sec=10.0)
                time.sleep(self.retry_period)
                continue
            except Exception as e:
                self.get_logger().error(f"{BRAKE_NAMES[i]}: error connecting to ODrive {self.serials[i]}: {e}")
                time.sleep(self.retry_period)
                continue

            with self.locks[i]:
                self.odrv[i] = odrv
                self.get_logger().info(f"{BRAKE_NAMES[i]}: ODrive {self.serials[i]} connected")
                if self.desired[i] is not None:
                    self.apply(i, self.desired[i])
            return

    def apply(self, i, engaged):
        # caller holds self.locks[i]
        try:
            self.odrv[i].set_gpio(self.brake_gpio, engaged)
        except Exception as e:
            self.get_logger().error(f"{BRAKE_NAMES[i]}: failed to set brake: {e}")

    def brake_engage_callback(self, msg):
        for i, engaged in enumerate((msg.brake1, msg.brake2)):
            with self.locks[i]:
                self.desired[i] = engaged
                if self.odrv[i] is not None:
                    self.apply(i, engaged)


def main(args = None):
    rclpy.init(args=args)
    node = ArmBrakes()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
