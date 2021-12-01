// #include <webots/Robot.hpp>
// #include <webots/Motor.hpp>
// #include <webots/PositionSensor.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Robot.hpp>
#include </usr/local/webots/include/controller/cpp/webots/Motor.hpp>
#include </usr/local/webots/include/controller/cpp/webots/PositionSensor.hpp>
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

  int iteration = 0;
  double ptime = 0;
  
  while(RobotController.robot->step(4) != -1){

    double time = RobotController.robot->getTime();
    
    // Encoder.updateTime(time);

    MutexP.lock();  
    
    // // Encoder.UpdateGoals(&Goals);

    // if (Goals.size() > 0)
    // {
    //   if (time > )
    //     {
    //       Motion.Plan(, time);
    //       ptime = (double)Goals.at(0).at(2);
    //       Motion.EraseOldPoints(&Goals, time);
    //       iteration+=1;
    //     }
    // 
    // }
    MutexP.unlock();

    std::cout << (double)clock() << " " << time << std::endl;

    float* PositionToMove = Motion.GetPosition(time-ptime);

    // std::cout << "X:" << PositionToMove[0] << " Y:" << PositionToMove[1] << " Iteration:" << iteration << " Time:" << time-ptime << std::endl;

    RobotController.FastMove(PositionToMove[0], PositionToMove[1], false);
    

  }

delete RobotController.robot;

}

void Communication(){ // Udlede positioner og tider fra vision
//CHILD PROCESS

UDP_Com UDP;
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


  float mha = 0.123456789123456789123456789123456789123456789123456789L;

  std::cout << sizeof(mha) << " " << mha << std::endl;


  // File pointer
  std::fstream fin;
  std::string filename = "/home/emil/Documents/TestPoints.txt";
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
  std::string line, data, temp;
  std::stringstream s;
  double t = 0;
  float px, py, XS, YS;
  bool runOnce = 0;
  while (std::getline(fin, line)) {

      tempdata.clear();
      // read an entire row and store it in a string variable 'line'
      s.clear();
      s.str(line);

      // read every column data of a row and store it in a string variable, 'data'
    while (getline(s, data, ',')) {
      // add all the column data of a row to a vector
      tempdata.push_back(data);
            
    }

    std::vector<float> tempVector;

    //Billede er 480 x 320;
    float x = (std::stoi(tempdata.at(0))*0.002083333)*2 - 0.1;
    float y = (std::stoi(tempdata.at(1))*0.003125)*0.5 + 0.6;
    if (!runOnce)
    {
      px = x;
      py = y;
      runOnce = true;
    }

    XS = x - px;
    YS = y - py;
    
    float s = 0;
    px = x;
    py = y;

    if (tempdata.at(2).at(0) == 'T')
    {
      s = 1;
    }

    if (s == 1)
    {
      t+=1*sqrt((XS*XS)+(YS*YS))*0.2;
    } else{
      t+=2*sqrt((XS*XS)+(YS*YS));
    }
    
    tempVector.push_back(x);
    tempVector.push_back(y);
    tempVector.push_back(t);
    tempVector.push_back(s);

    // Goals.push_back(tempVector);

  }
  fin.close();

  // std::cout << Goals.size() << " Goals loaded!" << std::endl;

  std::thread WeBotsController (Simulation);
  std::thread CommunicationHandler (Communication);

  Point point;
  point.x = 0.49;
  point.y = -0.5;

  std::cout << "InsideWorkspace()= " << Encoder.checkWorkspace(point, 0, 0) << std::endl;

  WeBotsController.join();
  CommunicationHandler.join();
  std::cout << "Syncronization of Threads Complete" << std::endl;
  
} 
        