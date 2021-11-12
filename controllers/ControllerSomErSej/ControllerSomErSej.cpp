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
#include "include/MotionPlanning.h"

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
    std::vector<std::vector<float>> Goals;


// Marie Alternation
void Simulation(){ //Udnytte positioner og tiden beregnet i encoderen
  Controller RobotController;
  MotionPlanning Motion;

  while(RobotController.robot->step(16) != -1){


///Old shit
    MutexP.lock();
    //MotionPlanning tilgår goals vektor
    Motion.Tester(Goals);

    //Motion.ComputeA(Goals);
    MutexP.unlock();


    RobotController.FastMove(-0.4, 1.2);
    
    MutexP.lock();

    if (POSX and POSY != 0)
    {
          RobotController.LinearMove(POSX , POSY);
    }
    ///^^^Old shit. 


  MotionPlanning MotionPlanner;
  MotionPlanner.InitiateTestData();
  MotionPlanner.ComputeA();
  while(RobotController.robot->step(16) != -1){
    MutexP.lock();
    double time = RobotController.robot->getTime();
    float timeVar = time-(int)time;

    //std::cout << timeVar << std::endl;

    float* PositionToMove = MotionPlanner.GetPosition(timeVar);

    // std::cout << PositionToMove[0] << ", " << PositionToMove[1] << std::endl;

    RobotController.FastMove(PositionToMove[0], PositionToMove[1], false);

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
            //Define goals vector by encoder function
          Goals = { EncodeMsg.Encoding(POSX, POSY, TimeDetected, TimeSet, CrackDetection) };
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
