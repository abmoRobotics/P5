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

    std::mutex MutexP;
    float POSY;
    float POSX;
    float TimeDetected;
    float TimeSet;
    float CrackDetection;


// Marie Alternation
void Simulation(){ //Udnytte positioner og tiden beregnet i encoderen
  Controller RobotController;
  while(RobotController.robot->step(16) != -1){
    RobotController.FastMove(-0.4, 1.2);
    
    MutexP.lock();
    if (POSX and POSY != 0)
    {
          RobotController.LinearMove(POSX , POSY);
    }
    

    // RobotController.LinearMove(0.4, 2.0);
    
    // RobotController.LinearMove(-0.4, 2.0);
    // RobotController.LinearMove(-0.4, 1.1);
    MutexP.unlock();

  };

delete RobotController.robot;

}

void Communication(){ // Udlede positioner og tider fra vision
 
  Encoder EncodeMsg;
    //CHILD PROCESS
  
  UDP_Com UDP;
  UDP.InitiateServer();
  //UDP.ToggleDebug(true);
  int rounds = 0;
  while (1){
    UDP.ReceiveMessage();
    UDP.PrintMessage();
    float *pos = UDP.ExtractPosition();
    float *time = UDP.ExtractTime();
    float *crackDet = UDP.ExtractCrackDet();
    MutexP.lock();
    POSX = pos[0];
    POSY = pos[1];   
    TimeDetected = time[0];
    TimeSet = time[1];
    CrackDetection = crackDet[0];

    EncodeMsg.Encoding(POSX, POSY, TimeDetected, TimeSet, CrackDetection);
    MutexP.unlock();
    rounds++;
    
  }
}


int main(int argc, char **argv)
{

  std::thread WeBotsController (Simulation);
  std::thread CommunicationHandler (Communication);

  WeBotsController.join();
  CommunicationHandler.join();
  std::cout << "Syncronization of Threads Complete" << std::endl;
  
}
