#include "include/MotionPlanning.h"
#include <math.h>
#include <UDP_Com.h>




float* MotionPlanning::GetPosition(float t){
    static float Position[2];
    Position[0] = a[0][0] + a[0][1]*t + a[0][2]*(t*t) + a[0][3]*(t*t*t);
    Position[1] = a[1][0] + a[1][1]*t + a[1][2]*(t*t) + a[1][3]*(t*t*t);
    return Position;
}

float* MotionPlanning::GetVelocity(float t){
    static float Velocity[2];
    Velocity[0] = a[0][1] + 2*a[0][2]*t + 3*a[0][3]*(t*t);
    Velocity[1] = a[1][1] + 2*a[1][2]*t + 3*a[1][3]*(t*t);
    return Velocity;
}

float* MotionPlanning::GetAcceleration(float t){
    static float Acceleration[2];
    Acceleration[0] = 2*a[0][2] + 6*a[0][3]*t;
    Acceleration[1] = 2*a[1][2] + 6*a[1][3]*t;
    return Acceleration;
}

void MotionPlanning::InitiateTestData(){
    DataPoints[0][0] = 0.4; //X0
    DataPoints[0][1] = 1.2; //Y0
    DataPoints[0][2] = 0; //T0
    
    DataPoints[1][0] = 0.4; //X1
    DataPoints[1][1] = 2.0; //Y1
    DataPoints[1][2] = 1; //T1

    DataPoints[2][0] = -0.4;
    DataPoints[2][1] = 2.0;
    DataPoints[2][2] = 2;
}

void MotionPlanning::ComputeA(){
    
    float t = (DataPoints[0][2]-DataPoints[1][2]);
    float t_third = t*t*t;
    
    // define x
    a[0][0] = DataPoints[0][0];
    a[0][2] = 0;
    a[0][3] = a[0][2]/(3 * t);
    a[0][1] = ((a[0][3] * t_third) + DataPoints[0][0] - DataPoints[1][0] ) / (t);
     
    // define y
    a[1][0] = DataPoints[0][1];
    a[1][2] = 0;
    a[1][3] = a[1][2]/(3 * t);
    a[1][1] = ((a[1][3] * t_third) + DataPoints[0][1] - DataPoints[1][1] ) / (t);
     

}