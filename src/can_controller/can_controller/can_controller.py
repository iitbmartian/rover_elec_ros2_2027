import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from can_interfaces.msg import CanMessage
import can_controller.arbitration_id as arb

import can
import threading
import queue
import time

bit_rate = 500000

# (msgtype -> node ids) of heartbeat replies routed to the dedicated 'heartbeat_replies' topic.
# Keyed by node too, since msgtype values overlap between node families (e.g. ODrive msgtype 6).
# Add an entry here when another subsystem gets a handshake.
HEARTBEAT_REPLIES = {
    arb.mobility_heartbeated: {arb.FR, arb.FL, arb.BR, arb.BL},
}

channel = "vcan0"
interface = "socketcan"

# TODOS:
# note -> im always assuming that data on the can bus is little endian
# this node is agnpstic of everything except the can bus now
# 1. The bus status thing doesn't really work I need to find a better way to do that.
# 2. Maybe we don't wanna have a buffer full of stale messages.

class CAN_Controller(Node):
    def __init__(self):
        super().__init__('CAN_Controller')
        while True:
            try: 
                self.bus = can.interface.Bus(channel=channel, interface=interface)
                self.get_logger().info("initialized CAN node")
                break
            except can.CanError: 
                self.get_logger().error("unable to start CAN")

        self.publisher_debug = self.create_publisher(Bool, 'bus_status', 10)
        self.can_bus = self.create_subscription(CanMessage, 'can_bus_to_controller', self.can_bus_callback, 10)
        self.can_received = self.create_publisher(CanMessage, 'can_messages_received', 10)
        # heartbeat replies bypass the shared RX topic so they never queue behind bulk traffic
        self.heartbeat_received = self.create_publisher(CanMessage, 'heartbeat_replies', 50)

        self.can_queue = queue.PriorityQueue()
        self.queue_counter = 0
        self.tx_thread = threading.Thread(target=self.can_from_queue, daemon=True)
        self.tx_thread.start()
        self.rx_thread = threading.Thread(target=self.can_receiver, daemon=True)
        self.rx_thread.start()

    def can_bus_callback(self, msg: CanMessage):
        nodeid = msg.nodeid
        msgtype = msg.msgtype
        data = msg.data

        self.transmit_message(nodeid, msgtype, data)

    def transmit_message(self, node, msg_type, data, priority = 5):
        arbid = arb.make_arbitration_id(node, msg_type)
        message = can.Message(arbitration_id = arbid, is_extended_id = False, data = [i & 0xFF for i in data])

        self.queue_counter += 1
        self.can_queue.put((priority, self.queue_counter, message))

    def can_from_queue(self):
        while rclpy.ok():
            priority, counter_no, message = self.can_queue.get()
            debug = Bool()

            try:
                self.bus.send(message)
                debug.data = True
                self.publisher_debug.publish(debug)
                # self.get_logger().info(f"transmitted message {list(message.data)} on arb id {message.arbitration_id}")

            except can.CanError: 
                debug.data = False
                self.publisher_debug.publish(debug)
                self.get_logger().error(f"can fucking up. can't transmit message {list(message.data)} on arb id {message.arbitration_id}")

            finally: self.can_queue.task_done()

    def can_receiver(self):
        for msg in self.bus:
            node, msgtype = arb.decode_id(msg.arbitration_id)
            data = list(msg.data)

            # data_int = int.from_bytes(msg.data[0:4], byteorder='little', signed=True)

            can_message = CanMessage()

            can_message.nodeid = node
            can_message.msgtype = msgtype
            can_message.data = data

            if node in HEARTBEAT_REPLIES.get(msgtype, ()):
                self.heartbeat_received.publish(can_message)
            else:
                self.can_received.publish(can_message)

    def destroy_node(self):
        self.bus.shutdown()
        super().destroy_node()

def main(args = None):
    rclpy.init(args=args)
    node = CAN_Controller()

    try: rclpy.spin(node)
    except KeyboardInterrupt: pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()