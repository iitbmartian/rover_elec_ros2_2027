import threading

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

# Stand-in for a real joystick while no hardware is attached. Type two
# numbers separated by a space and hit enter to set the left stick's
# left/right and forward/back axes, e.g.:
#   0.5 0      (half right)
#   0 -1       (full back)
#   0 0        (centered / stop)
# Publishes continuously at publish_rate, same as a real joystick driver
# would, so joy_translator.py behaves the same with this as with real
# hardware later.
#
# axes/buttons match the shape actually logged by joy_node.py off a real
# controller (8 axes, 11 buttons; axes[2]/axes[5] - the triggers - rest at
# 1.0, not 0.0):
#   axes=[-0.0, -0.0, 1.0, -0.0, -0.0, 1.0, 0.0, 0.0]
#   buttons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Only axes[0] (left/right) and axes[1] (forward/back) - the two
# joy_translator.py currently reads - are driven from stdin; the rest stay
# at their real-controller rest values so the message shape matches
# hardware even though this fakes only the left stick.

publish_rate = 20  # Hz

rest_axes = [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
num_buttons = 11


class DummyJoy(Node):
    def __init__(self):
        super().__init__('dummy_joy')

        self.axes = list(rest_axes)  # [left/right, forward/back, ...rest]
        self.lock = threading.Lock()

        self.joy_pub = self.create_publisher(Joy, 'joy', 10)
        self.timer = self.create_timer(1.0 / publish_rate, self.publish_joy)

        self.input_thread = threading.Thread(target=self.read_stdin, daemon=True)
        self.input_thread.start()

        print("dummy_joy: type 'left_right forward_back' (each -1 to 1) and press enter, e.g. '0 1'")

    def read_stdin(self):
        while True:
            try:
                line = input().strip()
            except EOFError:
                print("dummy_joy: stdin closed, no more input will be read (still publishing last axes)")
                return
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                print("dummy_joy: expected two numbers, e.g. '0.5 -1'")
                continue
            try:
                left_right, forward_back = (max(-1.0, min(1.0, float(p))) for p in parts)
            except ValueError:
                print("dummy_joy: could not parse numbers")
                continue
            with self.lock:
                self.axes[0] = left_right
                self.axes[1] = forward_back

    def publish_joy(self):
        msg = Joy()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'joy'
        with self.lock:
            msg.axes = list(self.axes)
        msg.buttons = [0] * num_buttons
        self.joy_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DummyJoy()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
