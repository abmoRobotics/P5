// File:          Controller.cpp
// Date:
// Description:
// Author:
// Modifications:

// You may need to add webots include files such as
// <webots/DistanceSensor.hpp>, <webots/Motor.hpp>, etc.
// and/or to add some other includes
#include </usr/local/webots/include/controller/cpp/webots/Robot.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Motor.hpp>
//#include <webots/PositionSensor.hpp>
#include <math.h>
#include <iostream>
#include <UDP_Com.h>

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>
// All the webots classes are defined in the "webots" namespace
using namespace webots;
float AngleRightActuator;
float AngleLeftActuator;
float AngleRightActuatorCompensated;
float AngleLeftActuatorCompensated;
#define TIME_STEP 32*35
float deg2rad(float angle)
{
  return (angle * M_PI/180);
}

float square(float input)
{
  return (input * input);
}

void ForwardKinematics(float theta, float thetad)
{
  float L0 = 0.4;
  float L1 = 1.0;
  float L2 = 1.2;
  float L3 = L2;
  float L4 = L1;

  float c = sqrt(square(L0) + square(L1) - 2 * L0 * L1 * cos(theta));
  float A = acos((square(c) + square(L1) - square(L0))/(2 * c * L1));
  float B = deg2rad(180) - theta - A;
  float thetadd = thetad - B;
  float cd = sqrt(square(L4) + square(c) - 2 * L4 * c * cos(thetadd));
  float Ad = acos((square(cd) + square(c) - square(L4))/(2 * cd * c));
  float thetaddd = Ad + A;
  float theta3 = deg2rad(180) - thetadd - Ad;
  float A3 = acos((square(L2) + square(cd) - square(L3))/(2 * cd * L2));
  float A4 = A + thetaddd;

  //step 2
  float a = sqrt(square(L1) + square(L2) - 2 * L1 * L2 * cos(A3));
  float B2 = acos((square(a) + square(L2) - square(L1))/(2 * a * L2));
  float C = deg2rad(180) - A4 - B;
  float thetadddd = theta - c;
  float x = cos(theta) * a;
  float y = sqrt(square(x) + square(a));
  std::cout << "X: " << x << ", y: " << y << std::endl;
}

void line()
{
  float L0 = 0.4;
  int linelenght {};
}

void InverseKinematics(float x, float y)
{
  float L0 = 0.4;
  float L1 = 1.0;
  float L2 = 1.2;
  float L3 = L2;
  float L4 = L1;
  float LeftAngle {};
  float RightAngle {};
  x += L0/2;
  y += 0.60;
  if(x >= 0)
  {
    LeftAngle = abs(atan(y/x));
  }
  if(x < 0)
  {
    LeftAngle = M_PI - abs(atan(y/x));
  }
  
  float d = sqrt((x * x) + (y * y));
  
  float alpha = acos(((d*d) + (L1 * L1) - (L2 * L2))/(2 * d * L1));
  
  AngleLeftActuator = alpha + LeftAngle;
  AngleLeftActuatorCompensated = AngleLeftActuator - (90*M_PI/180);

  if(x > L0)
  {
    RightAngle = M_PI - abs(atan(y/(x - L0)));
  }
  else if(x <= L0)
  {
   RightAngle = atan(y/(L0 - x));
  }
  float dodd = sqrt(((L0 - x) * (L0 - x)) + (y * y));

  float alphaodd = acos(((dodd * dodd) + (L4 * L4) - (L3 * L3))/(2 * dodd * L4));

  AngleRightActuator = alphaodd + RightAngle;

  AngleRightActuatorCompensated = (AngleRightActuator * (-1)) + (90*M_PI/180);

}

// This is the main program of your controller.
// It creates an instance of your Robot instance, launches its
// function(s) and destroys it at the end of the execution.
// Note that only one instance of Robot should be created in
// a controller program.
// The arguments of the main function can be specified by the
// "controllerArgs" field of the Robot node
int main(int argc, char **argv) {
  // create the Robot instance.
  Robot *robot = new Robot();
  
  Motor *motorR = robot->getMotor("MotorR");
  Motor *motorL = robot->getMotor("MotorL");
  
  //___________ FRA EMIL OG MARIE ____________
  printf("Server virker\n");

  int pid = fork();

  if (pid == -1) {
      perror("fork");
      exit(EXIT_FAILURE);
  } else if (pid == 0) {
    //PARENT PROCCESS
    while (robot->step(32) != -1){
      std::cout << "Main loo" << std::endl;
      //InverseKinematics(POSX, POSY); 
      motorR->setPosition(AngleRightActuatorCompensated);
      motorL->setPosition(AngleLeftActuatorCompensated);
    }
  } else {
    //CHILD PROCESS
    UDP_Com UDP;
    UDP.InitiateServer();
    UDP.ToggleDebug(true);
    int rounds = 0;
    //InverseKinematics(POSX, POSY);
    while (1){
      UDP.ReceiveMessage();
      UDP.PrintMessage();
      float *vel = UDP.ExtractVelocity();
      // POSX+=vel[0];
      // POSY+=vel[1];
      
      
      // std::cout << POSX << std::endl;
      rounds++;
      std::cout << "Rounds in loop: " << rounds << std::endl;
    }
      
  }
     

  // Enter here exit cleanup code.

  delete robot;
  return 0;
}
