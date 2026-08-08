#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"
using namespace std::chrono_literals;
using namespace std::placeholders;

class add_two_ints_client_node : public rclcpp::Node
{
    public:
        add_two_ints_client_node() : Node("add_two_ints_client")
        {
            client_=this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");


        }
        void call_f(int a, int b)
        {
           while (rclcpp::ok() && not client_ ->wait_for_service(1s))
                {
                    RCLCPP_WARN(this->get_logger(),"waiting for the server");

                     }

        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a=a;
        request->b=b;
        
        client_->async_send_request(request, std::bind(&add_two_ints_client_node::callback_response,this,_1) );

            


        }
        
    private:
         rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
         void callback_response(rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future)
         {
            auto response = future.get();
            RCLCPP_INFO(this->get_logger()," Sum = %d",(int)response->sum);
         }

};
int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<add_two_ints_client_node>();
    node->call_f(10,2);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0 ;
}