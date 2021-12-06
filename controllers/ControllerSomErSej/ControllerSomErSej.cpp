// #include <webots/Robot.hpp>
// #include <webots/Motor.hpp>
// #include <webots/PositionSensor.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Robot.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Motor.hpp>
#include </usr/local/webots/include/controller/cpp/webots/PositionSensor.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Display.hpp>
// #include </usr/local/webots/include/controller/cpp/webots/Shape.hpp>
#include <math.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
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

Encoder Encoder;

// Marie Alternation
void Simulation(){ //Udnytte positioner og tiden beregnet i encoderen

  Controller RobotController;
  MotionPlanning Motion;
  Encoder.setMeasurements(RobotController.L0, RobotController.L1, RobotController.L2);
  webots::Display CrackDisplay("CrackDisplay");

  Encoder.visualizePoints(&CrackDisplay);

  Motion.debug = false;
  Encoder.debug = false;

  int iteration = 0;
  double ptime = 0;
  std::vector<Point> goals;
  RobotController.FastMove(0.1, 1, false);

  while(RobotController.robot->step(1) != -1){

    double time = RobotController.robot->getTime();

    if(goals.size() > 1){
      if( goals.at(1).goalT < time){
        MutexP.lock();  
          goals = Encoder.getGoalsForTrajectoryPlanning(time);
        MutexP.unlock();
        Motion.Plan(goals, time);
        ptime = (double)goals.at(0).goalT;
        iteration+=1;
      }
    } else if(goals.size() == 1){
        ptime = (double)goals.at(0).goalT;
        MutexP.lock();  
          goals = Encoder.getGoalsForTrajectoryPlanning(time);
        MutexP.unlock();
        Motion.Plan(goals, time);
        iteration+=1;
    } else {
      MutexP.lock();  
        goals = Encoder.getGoalsForTrajectoryPlanning(time);
      MutexP.unlock();
    }
    
    float* PositionToMove = Motion.GetPosition(time-ptime);

    float movex = -PositionToMove[0] + 0.375;
    float movey = -PositionToMove[1] - 1.490;

    std::cout << "X:" << PositionToMove[0] << " Y:" << PositionToMove[1] << " Iteration:" << iteration << " Time:" << time-ptime << " goals size:" << goals.size() << std::endl;
 
    RobotController.FastMove(movex, movey, false);
    RobotController.robot->getMotor("MotorL")->enableTorqueFeedback(1);
    std::cout << "Left motor Torque: " << RobotController.robot->getMotor("MotorL")->getTorqueFeedback() << std::endl;
    

  }

delete RobotController.robot;

}

void Communication(){ // Udlede positioner og tider fra vision
//CHILD PROCESS

UDP_Com UDP;

 // File pointer
  std::fstream fin;
  std::string filename = "/home/emil/Documents/TestPoints3.txt";
  // Open an existing file
  std::cout << "Loading file: " << filename << std::endl;
  fin.open(filename, std::ios::in);
  if (!fin.is_open())
  {
      std::cout << "File: " << filename << " not opened. Check filename" << std::endl;
      system("pause");
      exit(1);
  }
  std::vector<std::string> tempdata;
  std::string line;
  std::stringstream s;
  double t = 0;
  while (std::getline(fin, line)) {
    
    if(line.size() > 2){

    UDP.DecodeMessage(line);

    int *pos = UDP.ExtractPosition();
    float *time = UDP.ExtractTime();
    float *crackDet = UDP.ExtractCrackDet();
    Point goal;
    goal.x = pos[0];
    goal.y = pos[1];   
    goal.frameT = time[0];
    goal.shift = crackDet[0];
      MutexP.lock();
        Encoder.addGoal(goal);
      MutexP.unlock();
    }
  }
  fin.close();

UDP.InitiateServer();
//UDP.ToggleDebug(true);

int rounds = 0;
while (1){
  UDP.ReceiveMessage();
  // UDP.PrintMessage();
  int *pos = UDP.ExtractPosition();
  float *time = UDP.ExtractTime();
  float *crackDet = UDP.ExtractCrackDet();
  Point goal;
  goal.x = pos[0];
  goal.y = pos[1];   
  goal.frameT = time[0];
  goal.shift = crackDet[0];
    MutexP.lock();
      Encoder.addGoal(goal);
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
        