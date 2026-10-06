import rclpy
from rclpy.node import Node

from can_interfaces.msg import WristPositionCommand
from can_interfaces.msg import WristEncoders
from general_interfaces.msg import MasterWristCommand
from arm_control.pid import PID

g = 50

control_rate = 50  # Hz
control_dt = 1.0 / control_rate

kp_l, ki_l, kd_l = 1.0, 0.0, 0.0
kp_r, ki_r, kd_r = 1.0, 0.0, 0.0
output_limit = 100.0
integral_limit = 50.0


class WristController(Node):
    def __init__(self):
        super().__init__('wrist_controller')

        self.vel_l_sp = 0.0
        self.vel_r_sp = 0.0

        self.quad_1 = 0.0
        self.quad_2 = 0.0

        self.pid_l = PID(kp_l, ki_l, kd_l, control_dt, output_limit, integral_limit)
        self.pid_r = PID(kp_r, ki_r, kd_r, control_dt, output_limit, integral_limit)

        self.wrist_commands = self.create_publisher(WristPositionCommand, 'wrist_commands', 10)
        self.wrist_encoders = self.create_subscription(WristEncoders, 'wrist_encoders', self.wrist_encoder_callback, 10)
        self.wrist_master_commands = self.create_subscription(MasterWristCommand, 'master_wrist_commands', self.wrist_master_command_cb, 10)

        self.timer = self.create_timer(control_dt, self.control_loop)

    def get_LR_vels(self, vel_pitch, vel_roll):
        vel_l = (vel_pitch + vel_roll) * g
        vel_r = (vel_pitch - vel_roll) * g
        return vel_l, vel_r

    def wrist_master_command_cb(self, msg):
        if not msg.pos_vel:
            self.vel_l_sp, self.vel_r_sp = self.get_LR_vels(msg.pitch, msg.roll)

    def wrist_encoder_callback(self, msg):
        self.quad_1 = float(msg.quad_1)
        self.quad_2 = float(msg.quad_2)

    def control_loop(self):
        vel_l_out = self.pid_l.update(self.vel_l_sp, self.quad_1)
        vel_r_out = self.pid_r.update(self.vel_r_sp, self.quad_2)

        command = WristPositionCommand()
        command.vel_l = vel_l_out
        command.vel_r = vel_r_out
        self.wrist_commands.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = WristController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
