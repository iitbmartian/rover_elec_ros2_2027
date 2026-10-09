import struct
import time

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Joy
from can_interfaces.msg import CanMessage

import can_controller.arbitration_id as arb
from joy_node.mapping import load_mapping, axis_value

ODRIVE_VELOCITY_CONTROL = 2
ODRIVE_PASSTHROUGH = 1
AXIS_IDLE = 1
AXIS_CLOSED_LOOP = 8


class JoyVelocity(Node):
    def __init__(self):
        super().__init__('joy_velocity')

        self.declare_parameter('config_file', '')
        cfg = load_mapping(self.get_parameter('config_file').value)
        self.general = cfg['general']
        self.joints = cfg['velocity_mode']

        # which joints to drive (default all); lets us test with a single ODrive attached
        self.declare_parameter('joints', ['shoulder', 'elbow', 'base'])
        self.declare_parameter('node_id_override', -1)
        self.declare_parameter('axis_override', -2)
        self.declare_parameter('idle_on_exit', True)
        self.enabled = list(self.get_parameter('joints').value)
        for name in self.enabled:
            if name not in self.joints:
                raise ValueError(f"unknown joint '{name}', expected shoulder/elbow/base")
        self.idle_on_exit = self.get_parameter('idle_on_exit').value
        self.odrive_joints = [j for j in ('shoulder', 'elbow') if j in self.enabled]

        node_override = self.get_parameter('node_id_override').value
        axis_override = self.get_parameter('axis_override').value
        if node_override >= 0 or axis_override != -2:
            if len(self.odrive_joints) != 1:
                raise ValueError('node_id_override/axis_override need exactly one of shoulder/elbow enabled')
            j = self.joints[self.odrive_joints[0]]
            if node_override >= 0:
                j['node_id'] = node_override
            if axis_override != -2:
                j['axis'] = axis_override

        self.odrive_nodes = [self.joints[j]['node_id'] for j in self.odrive_joints]
        self.base_node = self.joints['base']['node_id'] if 'base' in self.enabled else None
        self.start_time = time.monotonic()
        self.last_heartbeat = {}
        self.last_warn = 0.0

        self.can_pub = self.create_publisher(CanMessage, 'can_bus_to_controller', 10)
        self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.create_subscription(CanMessage, 'can_messages_received', self.can_callback, 10)

        self.ready = {n: False for n in self.odrive_nodes}
        self.last_joy_time = 0.0
        self.deadman_held = False
        self.cmd = {name: 0.0 for name in self.enabled}

        self.create_timer(1.0 / self.general['rate_hz'], self.timer_callback)
        self.create_timer(0.5, self.init_callback)

    def send(self, nodeid, msgtype, payload=b''):
        msg = CanMessage()
        msg.nodeid = nodeid
        msg.msgtype = msgtype
        msg.data = list(payload)  # int32[], one element per byte
        self.can_pub.publish(msg)

    def init_callback(self):
        """Resend until heartbeats confirm closed loop (early sends can be lost before discovery)."""
        now = time.monotonic()
        for n in self.odrive_nodes:
            if self.ready[n]:
                continue
            if n not in self.last_heartbeat and now - self.start_time > 3.0:
                self.get_logger().warning(
                    f'no heartbeat from ODrive node {n}: check wiring, CAN bitrate, node id and that the bus is up',
                    throttle_duration_sec=3.0)
            self.send(n, arb.clear_errors, struct.pack('<B', 0))
            self.send(n, arb.set_controller_mode, struct.pack('<II', ODRIVE_VELOCITY_CONTROL, ODRIVE_PASSTHROUGH))
            self.send(n, arb.set_axis_state, struct.pack('<I', AXIS_CLOSED_LOOP))

    def can_callback(self, msg: CanMessage):
        if msg.msgtype != arb.heartbeat_odr or msg.nodeid not in self.ready or len(msg.data) < 7:
            return
        data = bytes(x & 0xFF for x in msg.data)
        error, state, result, _ = struct.unpack('<IBBB', data[:7])
        ok = state == AXIS_CLOSED_LOOP and error == 0
        if ok and not self.ready[msg.nodeid]:
            self.get_logger().info(f'ODrive node {msg.nodeid} in closed loop (velocity mode)')
        self.last_heartbeat[msg.nodeid] = time.monotonic()
        if not ok:
            self.get_logger().info(
                f'ODrive node {msg.nodeid} not ready: axis_state={state} axis_error={error:#x} '
                f'procedure_result={result}', throttle_duration_sec=2.0)
        self.ready[msg.nodeid] = ok

    def joy_callback(self, msg: Joy):
        self.last_joy_time = time.monotonic()
        db = self.general['deadman_button']
        self.deadman_held = db < 0 or (db < len(msg.buttons) and msg.buttons[db] == 1)
        for name in self.cmd:
            j = self.joints[name]
            self.cmd[name] = j['max_vel'] * axis_value(msg, j['axis'], j['sign'], j['deadzone'])

    def timer_callback(self):
        active = (self.deadman_held and
                  time.monotonic() - self.last_joy_time < self.general['joy_timeout_s'])
        cmd = self.cmd if active else {name: 0.0 for name in self.cmd}

        # stream only once every enabled ODrive is in closed loop (never move one joint alone)
        if not all(self.ready.values()):
            return
        for name in self.odrive_joints:
            self.send(self.joints[name]['node_id'], arb.set_input_vel, struct.pack('<ff', cmd[name], 0.0))
        if self.base_node is not None:
            self.send(self.base_node, arb.base_vel_command, struct.pack('<f', cmd['base']))

    def shutdown(self):
        for _ in range(3):
            for n in self.odrive_nodes:
                self.send(n, arb.set_input_vel, struct.pack('<ff', 0.0, 0.0))
            if self.base_node is not None:
                self.send(self.base_node, arb.base_vel_command, struct.pack('<f', 0.0))
            time.sleep(0.02)
        if self.idle_on_exit:
            for n in self.odrive_nodes:
                self.send(n, arb.set_axis_state, struct.pack('<I', AXIS_IDLE))


def main(args=None):
    rclpy.init(args=args)
    node = JoyVelocity()

    try: rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException): pass

    try: node.shutdown()
    except Exception: pass
    node.destroy_node()
    if rclpy.ok(): rclpy.shutdown()

if __name__ == "__main__":
    main()
