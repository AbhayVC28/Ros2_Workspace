#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"
#include <string>

using namespace std::chrono_literals;

class Robot_news_station_node : public rclcpp::Node
{
    public:
        Robot_news_station_node() : Node("Robot_news_station")
        {
            this->declare_parameter("name","Megatron");
            name = this->get_parameter("name").as_string();
            publisher_ = this ->create_publisher<example_interfaces::msg::String>("Robot_news",10);
            timer_= this->create_wall_timer(0.5s, std::bind(&Robot_news_station_node::publishNews, this)); 
            RCLCPP_INFO(this->get_logger(), "Robot tower has been activated");        }
        
    private:

        void publishNews()
        {
            auto msg = example_interfaces::msg::String();
            msg.data="Hi this is " + this->name + " from the Robot News Tower!" ;
            publisher_->publish(msg);
        }    

        rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_ ;
        rclcpp::TimerBase::SharedPtr timer_; 
        std::string name ;
};
int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<Robot_news_station_node>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0 ;
}