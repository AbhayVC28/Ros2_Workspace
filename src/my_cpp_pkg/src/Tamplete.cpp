#include "rclcpp/rclcpp.hpp"

class Name : public rclcpp::Node
{
    public:
        Name() : Node("cpp_test")
        {
        }
        
    private:
    
};
int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<Name>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0 ;
}