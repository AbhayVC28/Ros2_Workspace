#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::placeholders;

class Add_two_ints_serv_node : public rclcpp::Node
{
    public:
        Add_two_ints_serv_node() : Node("Add_two_ints_server")
        {
            server_=this->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", std::bind(&Add_two_ints_serv_node::callback_f,this,_1,_2));
            RCLCPP_INFO(this->get_logger(),"The server has started");
        }
        
    private:
        rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server_;
        
        void callback_f(const example_interfaces::srv::AddTwoInts::Request::SharedPtr request,
                        const example_interfaces::srv::AddTwoInts::Response::SharedPtr response)
                        {
                            response->sum = request->a + request->b;
                            RCLCPP_INFO(this->get_logger(), "%d + %d = %d", (int)request->a, (int)request->b, (int)response->sum);
                        }
    
};
int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<Add_two_ints_serv_node>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0 ;
}