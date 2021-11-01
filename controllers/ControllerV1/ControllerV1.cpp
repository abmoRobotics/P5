// File:          ControllerV1.cpp
// Date:
// Description:
// Author:
// Modifications:

// You may need to add webots include files such as
// <webots/DistanceSensor.hpp>, <webots/Motor.hpp>, etc.
// and/or to add some other includes
#include </usr/local/webots/include/controller/cpp/webots/Robot.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Motor.hpp>

#include <UDP_Com.h>
#include "include/shrimp_protocol.h"
#include <stdlib.h>
#include <string.h>
#include <sstream>
#include <iostream>

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>

// All the webots classes are defined in the "webots" namespace
using namespace webots;
using namespace std;

void SetVelocity(Motor RobotMotor/*, float *velocity*/){
  cout << "Velocity set\n" << endl;
  // double dValue(0.0);
  // dValue = static_cast<double>(velocity[0]);
  // cout << dValue << endl;
  
  RobotMotor.setVelocity(10.0);
}


int main() {
  Robot *robot = new Robot(); 
  Motor *motor = robot->getMotor("my_motor");


  printf("Server virker\n");

  int pid = fork();

  if (pid == -1) {
      perror("fork");
      exit(EXIT_FAILURE);
  } else if (pid == 0) {
    //PARENT PROCCESS
    while (robot->step(32) != -1){
      int a = 0;
    }
  } else {
    //CHILD PROCESS
    UDP_Com UDP;
    UDP.InitiateServer();
    UDP.ToggleDebug(true);
    int rounds = 0;
    while (1){
      UDP.ReceiveMessage();
      UDP.PrintMessage();
      float *vel = UDP.ExtractVelocity();
      //SetVelocity(*motor);
      // int a = 1;
      // if (a == 1){
      //   motor->setVelocity(1.0);
      //   a++;
      // }     
      
      std::cout << vel[0] << std::endl;
      rounds++;
      std::cout << "Rounds in loop: " << rounds << std::endl;
    }
      
  }

  delete robot;
  return 0;
}
