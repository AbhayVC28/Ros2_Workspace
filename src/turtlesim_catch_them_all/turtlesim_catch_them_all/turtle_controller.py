#!/usr/bin/env python3 
import rclpy
import math
from rclpy.node import Node
from my_robot_interfaces.msg import TurtleSim
from turtlesim.srv import Kill
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class turtle_controller_node(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.create_subscription(TurtleSim,"/Alive_turtle",self.Loc_append,10)
        self.create_subscription(Pose,"/turtle1/pose",self.Pose_eval,10)
        self.publisher_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.client_=self.create_client(Kill,"/kill")
        self.create_timer(0.1, self.control_loop)
        self.list=[]
        self.current_target=None
        self.px=0.0
        self.py=0.0
        self.pt=0.0
        

    def Kill_turtle(self, name: str):
        req=Kill.Request()
        req.name=name 
        future = self.client_.call_async(req)
        future.add_done_callback(self.callback_done)  
         

    def Pose_eval(self,msgs: Pose):
            self.px=msgs.x
            self.py=msgs.y
            self.pt=msgs.theta

    def Loc_append(self,msg: TurtleSim):
        self.list.append((msg.x,msg.y,msg.theta,msg.name))

    def control_loop(self):
        if self.current_target is not None:
            self.list.append(self.current_target)
            self.current_target=None
        if len(self.list)>0:
            closest_index=0
            min_dist=float('inf')
            for i,target in enumerate(self.list):
                t_x,t_y,t_theta,t_nam=target
                dist_to_target=math.sqrt((t_x-self.px)**2+(t_y-self.py)**2)
                if dist_to_target< min_dist:
                    min_dist=dist_to_target
                    closest_index=i
            self.current_target=self.list.pop(closest_index)
        else:
            self.publisher_.publish(Twist())
            return
        del_x = self.current_target[0]-self.px
        del_y = self.current_target[1]-self.py
        
        dist=math.sqrt(del_x**2+del_y**2)
        T_msg=Twist()
        if dist<0.5:
            self.publisher_.publish(Twist())
            self.Kill_turtle(self.current_target[3])
            self.current_target=None
        else:
            d_theta=math.atan2(del_y,del_x)
            del_t = d_theta-self.pt
            del_t=math.atan2(math.sin(del_t),math.cos(del_t))
            T_msg.linear.x=min(2.0*dist,2.0)
            T_msg.angular.z=6.0*del_t
            self.publisher_.publish(T_msg)

    def callback_done(self, future):
        self.get_logger().info("Killed")        

def main(args = None):
    rclpy.init(args=args)
    node =  turtle_controller_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()
