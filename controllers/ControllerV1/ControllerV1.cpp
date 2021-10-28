// File:          ControllerV1.cpp
// Date:
// Description:
// Author:
// Modifications:

// You may need to add webots include files such as
// <webots/DistanceSensor.hpp>, <webots/Motor.hpp>, etc.
// and/or to add some other includes
#include <webots/Robot.hpp>

//#include "UDP/include/UDP_Com.h"
#include <stdlib.h>
#include <string.h>
#include <sstream>
#include <iostream>

// All the webots classes are defined in the "webots" namespace
using namespace webots;

int main() {
  Robot *robot = new Robot();

    printf("Server virker\n");

    // UDP_Com TEST;

    // TEST.ReceiveMessage();
  while (robot->step(32) != -1)
    std::cout << "Made it, Houston!" << std::endl;


  delete robot;
  return 0;
}
