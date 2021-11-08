#include <webots/Robot.hpp>
#include <webots/Motor.hpp>
#include <webots/PositionSensor.hpp>
#include <math.h>
class Controller
{
private:
    
    
    void ForwardKinematics(float theta, float thetad);
    float square(float input);
    float deg2rad(float angle);
    float getLpos();
    float getRpos();
    void waitForrobotToreachPos(float LeftAngle, float RightAngle);
    void InverseKinematics(float x, float y, bool PosCheck);
    void line(float x0, float y0);
    webots::Motor *MotorR;
    webots::Motor *MotorL;
    webots::PositionSensor *PosL;
    webots::PositionSensor *PosR;
    float xCoord{};
    float yCoord{}; 
public:
    Controller(/* args */);
    void LinearMove(float x, float y);
    void FastMove(float x, float y);
   // ~Controller();
    
    webots::Robot *robot;
};

// Controller::Controller(/* args */)
// {
//     Robot *robot = new Robot();

//     Motor *motorR = robot->getMotor("MotorR");
//     Motor *motorL = robot->getMotor("MotorL");

//     PositionSensor *posR = robot->getPositionSensor("PosR");
//     PositionSensor *posL = robot->getPositionSensor("PosL");
// }

// Controller::~Controller()
// {
// }