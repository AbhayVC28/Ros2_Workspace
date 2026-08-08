#!/usr/bin/env python3 
import rclpy
import random
from rclpy.node import Node
from my_robot_interfaces.msg import TurtleSim
from turtlesim.srv import Spawn

class Turtle_spawner_node(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.publisher_= self.create_publisher(TurtleSim,"/Alive_turtle",10)
        self.client_=self.create_client(Spawn,"/spawn")
        self.counter_=1
        self.timer_=self.create_timer(1.0,self.Turtle_Random)
        

    def Turtle_Random(self):
            if not self.client_.wait_for_service(timeout_sec=1.0):
                self.get_logger().warn("Waiting for /spawn service...")
                return
            request=Spawn.Request()
            request.x= random.uniform(1.0,10.0) 
            request.y= random.uniform(1.0,10.0) 
            request.theta= random.uniform(0.0,6.28)
            request.name= f'turtle_rand_{self.counter_}'
            self.counter_+=1
            self.new=request
            future=self.client_.call_async(request)
            future.add_done_callback(self.callback_spawn)

    def callback_spawn(self,future):
        response=future.result()
        self.Turtle_loc_pub()

    def Turtle_loc_pub(self):
        msg=TurtleSim()
        msg.x=self.new.x
        msg.y=self.new.y
        msg.theta=self.new.theta
        msg.name=self.new.name

        self.publisher_.publish(msg)

def main(args = None):
    rclpy.init(args=args)
    node =  Turtle_spawner_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()
