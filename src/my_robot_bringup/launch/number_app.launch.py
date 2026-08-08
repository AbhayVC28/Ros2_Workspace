from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld=LaunchDescription()
    param_config = os.path.join(get_package_share_directory("my_robot_bringup"),"config","number_app.yaml")

    number_publisher=Node(
        package="my_fun_pkg",
        executable="number_publisher",
        namespace="/abc",
        name="My_number_publisher",
        remappings=[("number","my_number")],
        parameters=[param_config]
        # parameters=[{"number": 12}, {"timer_period: 1.2"}]
    )
    number_counter=Node(
        package="fun2_pkg",
        executable="number_counter",
        namespace="/abc",
        name="My_number_counter",
        remappings=[("number","my_number"),("number_count","my_number_count")]
    )

    ld.add_action(number_publisher)
    ld.add_action(number_counter)
    return ld
