#include "include/MotionPlanning.h"
#include <math.h>
#include <UDP_Com.h>
#include <iostream>
#include <vector>


void MotionPlanning::Tester(std::vector<std::vector<float>> GoalsVector){
    //Test to see if goals can be send between 
            for (size_t i = 0; i < GoalsVector.size(); i++) //four iterations
        {
              std::cout << "Timeset for robot in MotionPlanning: " << GoalsVector[0][2] << ".  Pos x: " << GoalsVector[0][0] << std::endl;
        }
       
}

float* MotionPlanning::GetPosition(float t){
    static float Position[2];
    Position[0] = a[0][0] + (a[0][1]*t) + (a[0][2]*(t*t)) + (a[0][3]*(t*t*t));
    Position[1] = a[1][0] + (a[1][1]*t) + (a[1][2]*(t*t)) + (a[1][3]*(t*t*t));
    return Position;
}

float* MotionPlanning::GetVelocity(float t){
    static float Velocity[2];
    Velocity[0] = a[0][1] + (2*a[0][2]*t) + (3*a[0][3]*(t*t));
    Velocity[1] = a[1][1] + (2*a[1][2]*t) + (3*a[1][3]*(t*t));
    return Velocity;
}

float* MotionPlanning::GetAcceleration(float t){
    static float Acceleration[2];
    Acceleration[0] = (2*a[0][2]) + (6*a[0][3]*t);
    Acceleration[1] = (2*a[1][2]) + (6*a[1][3]*t);
    return Acceleration;
}

void MotionPlanning::InitiateTestData(){
    DP[0][0] = 0.8; //X0
    DP[0][1] = 1.0; //Y0
    DP[0][2] = 0; //T0
    
    DP[1][0] = -0.8; //X1
    DP[1][1] = 1.0; //Y1
    DP[1][2] = 1; //T1

    DP[2][0] = 5;
    DP[2][1] = -3;
    DP[2][2] = 2;
}

float MotionPlanning::CalculateDesiredVelocity(float x1, float y1, float x2, float y2, float x3, float y3, float t1, float t2, char coor){
    
    
    float Xdif = x2 - x1;
    float Ydif = y2 - y1;
    float distance = sqrt(Xdif*Xdif + Ydif*Ydif);
    float timeDif = t2 - t1;
    float DesiredVelocity = distance/timeDif;
    
    float DesiredDirX = x3 - x1;
    float DesiredDirY = y3 - y1;
    float DesiredDirLength = sqrt((DesiredDirX*DesiredDirX) + (DesiredDirY*DesiredDirY));

    DesiredDirX = DesiredDirX/DesiredDirLength;
    DesiredDirY = DesiredDirY/DesiredDirLength;
    if (coor == 'x')
    {
        DesiredVelocity = DesiredVelocity * DesiredDirX;
    } else if (coor == 'y')
    {
        DesiredVelocity = DesiredVelocity * DesiredDirY;
    }
    
    return DesiredVelocity;
}

void MotionPlanning::ComputeA(){

    //Calculate desired velocities in X and Y directions.    
    float velX = CalculateDesiredVelocity(DP[0][0], DP[0][1], DP[1][0],DP[1][1],DP[2][0], DP[2][1], DP[0][2], DP[1][2], 'x');
    float velY = CalculateDesiredVelocity(DP[0][0], DP[0][1], DP[1][0],DP[1][1],DP[2][0], DP[2][1], DP[0][2], DP[1][2], 'y');

    float velXi = LastVel[0];
    float velYi = LastVel[1];
    
    // define x
    a[0][0] = (DP[0][0]*(DP[1][2]*DP[1][2]*DP[1][2]) - DP[1][0]*(DP[0][2]*DP[0][2]*DP[0][2]) - velX*(DP[1][2]*DP[1][2])*(DP[0][2]*DP[0][2]) + velXi*(DP[1][2]*DP[1][2])*(DP[0][2]*DP[0][2]) + 3*DP[1][0]*DP[1][2]*(DP[0][2]*DP[0][2]) - 3*DP[0][0]*(DP[1][2]*DP[1][2])*DP[0][2] + velX*DP[1][2]*(DP[0][2]*DP[0][2]*DP[0][2]) - velXi*(DP[1][2]*DP[1][2]*DP[1][2])*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2])));
    a[0][1] = (velXi*(DP[1][2]*DP[1][2]*DP[1][2]) - velX*(DP[0][2]*DP[0][2]*DP[0][2]) - 6*DP[1][0]*DP[1][2]*DP[0][2] + 6*DP[0][0]*DP[1][2]*DP[0][2] - velX*DP[1][2]*(DP[0][2]*DP[0][2]) + 2*velX*(DP[1][2]*DP[1][2])*DP[0][2] - 2*velXi*DP[1][2]*(DP[0][2]*DP[0][2]) + velXi*(DP[1][2]*DP[1][2])*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2])));
    a[0][2] = (3*DP[1][0]*DP[1][2] - 3*DP[0][0]*DP[1][2] + 3*DP[1][0]*DP[0][2] - 3*DP[0][0]*DP[0][2] - velX*(DP[1][2]*DP[1][2]) - 2*velXi*(DP[1][2]*DP[1][2]) + 2*velX*(DP[0][2]*DP[0][2]) + velXi*(DP[0][2]*DP[0][2]) - velX*DP[1][2]*DP[0][2] + velXi*DP[1][2]*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2])));
    a[0][3] = -(2*DP[1][0] - 2*DP[0][0] - velX*DP[1][2] - velXi*DP[1][2] + velX*DP[0][2] + velXi*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2])));

    if (debug){
        std::cout << "X formula: " << a[0][0] << " + " << a[0][1] << "*t + " << a[0][2] << "*t² + " << a[0][3] << "*t³" << std::endl;
    }    

    // define y
    a[1][0] = (DP[0][1]*(DP[1][2]*DP[1][2]*DP[1][2]) - DP[1][1]*(DP[0][2]*DP[0][2]*DP[0][2]) - velY*(DP[1][2]*DP[1][2])*(DP[0][2]*DP[0][2]) + velYi*(DP[1][2]*DP[1][2])*(DP[0][2]*DP[0][2]) + 3*DP[1][1]*DP[1][2]*(DP[0][2]*DP[0][2]) - 3*DP[0][1]*(DP[1][2]*DP[1][2])*DP[0][2] + velY*DP[1][2]*(DP[0][2]*DP[0][2]*DP[0][2]) - velYi*(DP[1][2]*DP[1][2]*DP[1][2])*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2]))); 
    a[1][1] = (velYi*(DP[1][2]*DP[1][2]*DP[1][2]) - velY*(DP[0][2]*DP[0][2]*DP[0][2]) - 6*DP[1][1]*DP[1][2]*DP[0][2] + 6*DP[0][1]*DP[1][2]*DP[0][2] - velY*DP[1][2]*(DP[0][2]*DP[0][2]) + 2*velY*(DP[1][2]*DP[1][2])*DP[0][2] - 2*velYi*DP[1][2]*(DP[0][2]*DP[0][2]) + velYi*(DP[1][2]*DP[1][2])*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2])));
    a[1][2] = (3*DP[1][1]*DP[1][2] - 3*DP[0][1]*DP[1][2] + 3*DP[1][1]*DP[0][2] - 3*DP[0][1]*DP[0][2] - velY*(DP[1][2]*DP[1][2]) - 2*velYi*(DP[1][2]*DP[1][2]) + 2*velY*(DP[0][2]*DP[0][2]) + velYi*(DP[0][2]*DP[0][2]) - velY*DP[1][2]*DP[0][2] + velYi*DP[1][2]*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2])));
    a[1][3] = -(2*DP[1][1] - 2*DP[0][1] - velY*DP[1][2] - velYi*DP[1][2] + velY*DP[0][2] + velYi*DP[0][2])/((DP[1][2] - DP[0][2])*((DP[1][2]*DP[1][2]) - 2*DP[1][2]*DP[0][2] + (DP[0][2]*DP[0][2])));   
    
    if (debug){
        std::cout << "Y formula: " << a[1][0] << " + " << a[1][1] << "*t + " << a[1][2] << "*t² + " << a[1][3] << "*t³" << std::endl;
    }

    LastVel[0] = velX;
    LastVel[1] = velY;
}