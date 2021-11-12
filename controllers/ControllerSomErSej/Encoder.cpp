#include "include/Encoder.h"
#include <UDP_Com.h>
#include "include/MotionPlanning.h"
#include <iostream>
#include <vector>
#include <ctime>

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>
#include <thread>
#include <mutex>

std::vector<std::vector<float>> MotionVec;

    

// Alter message from coordinates of two time stamps to coordinates with one time stamp
std::vector<std::vector<float>> Encoder::Encoding(float posx, float posy, float timedetected, float timeset, float crackDet){
    GetVelocity();
    //GetDistPoint();
    MotionVec.clear();


      //Initial timestamp. This assumes zero acceleration
    float TimeVanTravel = DistVehicle/VelocityMS; //Seconds from vision position to robot position
    timesetRobot = timeset + TimeVanTravel; //Change timestamp for point for the CURRENT velocity. 
    clickClock = clock(); //Time in this instance
    std::cout << "Initial time set" << timesetRobot << std::endl;


      //Predict timestamp of point until being the next point to generate trajectory on.
    while (DistVehicle > DistPoint){ //loop until the point has travelled the van distance
      GetDistPoint();
      TimeVanTravel = DistVehicle/VelocityMS;
      timesetRobot = timeset + TimeVanTravel;
    }
    
    std::vector<float> stallVec = {posx, posy, timesetRobot, crackDet}; //coordinates, final timestamp, and crack detected 
    MotionVec.push_back(stallVec);  
    std::cout << "final time set" << timesetRobot << std::endl;

    return MotionVec;
   
}

void Encoder::GetDistPoint(){//Track point in the y axis
    clock_t clickSample = clock();
    tSample = ((float)clickSample)/CLOCKS_PER_SEC;
    tClock = ((float)clickClock)/CLOCKS_PER_SEC;
    
    tSampleP = tSample - tClock; //current sample time
    tSample_old = tSampleP - tSample_old; //get time for sample 
    GetVelocity();
    DistPoint_old = tSample_old * VelocityMS; //get distance for specific sample
    DistPoint = DistPoint + DistPoint_old; //add all sampled distances together
}


void Encoder::GetVelocity(){
    //Do sketchy shit in webots
    //Webots_encoder = Velocity: 

    int i = 1;
      if (i == 1){
        Velocity1 = Velocity; //+ round;
        VelocityMS = Velocity1 * 0.27778; //Convertion from km/h to m/s
            //round++;
            i--;
      }

}

