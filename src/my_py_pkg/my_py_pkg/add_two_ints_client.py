#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class Add_two_ints_client_node(Node):
    def __init__(self):
        super().__init__("Add_two_ints_client")
        self.client_=self.create_client(AddTwoInts,"add_two_ints")

    def call_add_int(self,a,b):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("waiting for the server...")
        request=AddTwoInts.Request()
        request.a=a
        request.b=b
        x=request
        future=self.client_.call_async(request)
        future.add_done_callback(lambda f: self.callback_call_add_two_ints(f,x))

    def callback_call_add_two_ints(self, future, x):
        response=future.result()
        self.get_logger().info(str(x.a) + " + " + str(x.b) + " = " + str(response.sum))
        rclpy.shutdown()


def main(args = None):
    rclpy.init(args=args)
    node =  Add_two_ints_client_node()
    node.call_add_int(3,8)
    rclpy.spin(node)
    if rclpy.ok():
        rclpy.shutdown()
if __name__=="__main__":
    main()
