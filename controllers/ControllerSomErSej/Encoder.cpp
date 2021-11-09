#include "include/Encoder.h"
#include <UDP_Com.h>
#include "include/MotionPlanning.h"
#include <iostream>
#include <vector>

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>
#include <thread>
#include <mutex>

#define COL = 3

std::vector<std::vector<float>> MotionVec;


// Alter message from coordinates of two time stamps to coordinates with one time stamp
void Encoder::Encoding(float posx, float posy, float timedetected, float timeset, float crackDet){

    MotionPlanning Motion;

    float TimeVanTravel = DistVehicle/Velocity; //Seconds from vision position to robot position
    timeset = timeset;// + TimeVanTravel; //Change timestamp for point
    
      //____________  FOR EMIL _____________//
    //Push points into vector and call MotionPlanning.
    std::vector<float> stallVec = {posx, posy, timeset, crackDet}; //coordinates, final timestamp, and crack detected if !=0
    MotionVec.push_back(stallVec);

    //Motion.ComputeA(MotionVec);
    
}

void GetVelocity(){
    //Do sketchy shit in webots
    //Webots_encoder = Velocity:    
    float Velocity = Velocity * 0.27778; //Convertion from km/h to m/s
}