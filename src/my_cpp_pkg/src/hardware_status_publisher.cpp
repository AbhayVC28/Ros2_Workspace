#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/msg/hardware_status.hpp" 
using namespace std::chrono_literals;

class hardware_status_publisher_node : public rclcpp::Node
{
    public:
        hardware_status_publisher_node() : Node("hardware_status_publisher")
        {
            publisher_ = this->create_publisher<my_robot_interfaces::msg::HardwareStatus>("Hardware_status",10);
            timer_=this->create_wall_timer(0.5s, std::bind(&hardware_status_publisher_node::callback_data,this));
            RCLCPP_INFO(this->get_logger(),"The Hardware Status is being published");
        }
        

    private:

        void callback_data()
        {
             auto msg = my_robot_interfaces::msg::HardwareStatus();
             msg.are_motors_ready = false;
             msg.debug_message = "Hello it worked";
             msg.temperature = 45;
             publisher_->publish(msg);
            
        }
        rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
    
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<hardware_status_publisher_node>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
