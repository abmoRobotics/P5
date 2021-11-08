// #include <webots/Robot.hpp>
// #include <webots/Motor.hpp>
// #include <webots/PositionSensor.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Robot.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Motor.hpp>
#include </usr/local/webots/include/controller/cpp/webots/PositionSensor.hpp>
#include <math.h>
#include <vector>
#include <iostream>
#include <UDP_Com.h>
#include "include/Controller.h"
#include "include/Encoder.h"

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>
#include <thread>
#include <mutex>

// Marie Alternation
// void Simulation(Robot Robert){
//   while (Robert.step(32) != -1){
//     RobotController.LinearMove(0.4, 1.2);
//     RobotController.LinearMove(0.4, 2.0);
    
//     RobotController.LinearMove(-0.4, 2.0);
//     RobotController.LinearMove(-0.4, 1.1);

//   }
// }

// void Communication(){
//   std::cout << "Child process" << std::endl;
// }


// This is the main program of your controller.
// It creates an instance of your Robot instance, launches its
// function(s) and destroys it at the end of the execution.
// Note that only one instance of Robot should be created in
// a controller program.
// The arguments of the main function can be specified by the
// "controllerArgs" field of the Robot node
int main(int argc, char **argv)
{


  Controller RobotController;

  
  
  // std::thread WeBotsController (Simulation, std::ref(*robot));
  // std::thread CommunicationHandler (Communication);

  // WeBotsController.join();
  // CommunicationHandler.join();
  // std::cout << "Syncronization of Threads Complete" << std::endl;
  



  // get the time step of the current world.
  //int timeStep = (int)robot->getBasicTimeStep();

  // You should insert a getDevice-like function in order to get the
  // instance of a device of the robot. Something like:

  // Main loop:
  // - perform simulation steps until Webots is stopping the controller
  // Read the sensors:
  // Enter here functions to read sensor data, like:

  // Process sensor data here.
  
   RobotController.FastMove(-0.4, 1.2);
  while (1)
  {
  
    RobotController.LinearMove(0.4, 1.2);
    RobotController.LinearMove(0.4, 2.0);
    
    RobotController.LinearMove(-0.4, 2.0);
    RobotController.LinearMove(-0.4, 1.1);
  
    //line(1.0, 0.5);

    //ForwardKinematics(posL->getValue(), posR->getValue());

    //ForwardKinematics(AngleLeftActuator, AngleRightActuator);

    //std::cout << "Actual value: " << posL->getValue() + (90*M_PI/180) << ", " << (posR->getValue() * (-1)) + (90*M_PI/180) << std::endl;

    //std::cout << "Calculated value: " << AngleLeftActuator << ", " << AngleRightActuator << std::endl;
    //std::cout << AngleLeftActuatorCompensated << ", " << AngleRightActuatorCompensated << std::endl;
  };

  // Enter here exit cleanup code.

  delete RobotController.robot;
  return 0;
}
