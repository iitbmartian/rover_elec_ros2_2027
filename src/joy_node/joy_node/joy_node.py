import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy

class JoyNode(Node):
    def __init__(self):
        super().__init__('joy_node')

        self.joystick_sub = self.create_subscription(Joy, '/joy', self.joystick_callback, 10) 

    def joystick_callback(self, joystick):
        self.get_logger().info(str(joystick))


def main(args = None):
    rclpy.init(args=args)
    node = JoyNode()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



# [INFO] [1788972975.291048683] [joy_node]: sensor_msgs.msg.Joy(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1788972975, nanosec=289499674), frame_id='joy'), axes=[-0.0, -0.0, -0.0, -0.0, 0.0, 0.0], buttons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# [INFO] [1788972975.342416056] [joy_node]: sensor_msgs.msg.Joy(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1788972975, nanosec=340907010), frame_id='joy'), axes=[-0.0, -0.0, -0.0, -0.0, 0.0, 0.0], buttons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# [INFO] [1788972975.393162570] [joy_node]: sensor_msgs.msg.Joy(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1788972975, nanosec=391672470), frame_id='joy'), axes=[-0.0, -0.0, -0.0, -0.0, 0.0, 0.0], buttons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# [INFO] [1788972975.493423360] [joy_node]: sensor_msgs.msg.Joy(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1788972975, nanosec=491963076), frame_id='joy'), axes=[-0.0, -0.0, -0.0, -0.0, 0.0, 0.0], buttons=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
