from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld=LaunchDescription()
    param_config = os.path.join(get_package_share_directory("my_robot_bringup"),"config","robot.yaml")

    robot_news_station_glskard=Node(
        package="my_py_pkg",
        executable="robot_news_station",
        name="robot_news_station_glskard",
        parameters=[param_config]
    )

    robot_news_station_bb8=Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_bb8",
            parameters=[param_config]
        )

    robot_news_station_daneel=Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_daneel",
            parameters=[param_config]
        )

    robot_news_station_jander=Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_jander",
            parameters=[param_config]
        )

    robot_news_station_c3po=Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_c3po",
            parameters=[param_config]
        )

    
    smartphone=Node(
        package="my_cpp_pkg",
        executable="smartphone",
    )

    ld.add_action(robot_news_station_c3po)
    ld.add_action(robot_news_station_jander)
    ld.add_action(robot_news_station_bb8)
    ld.add_action(robot_news_station_daneel)
    ld.add_action(robot_news_station_glskard)
    ld.add_action(smartphone)
    return ld
