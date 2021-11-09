#include "include/MotionPlanning.h"
#include <math.h>
#include <UDP_Com.h>



void MotionPlanning::InitiateTestData(){
    DataPoints[0][0] = 0; //X0
    DataPoints[0][1] = 0; //Y0
    DataPoints[0][2] = 0; //T0
    
    DataPoints[1][0] = 2; //X1
    DataPoints[1][1] = 1; //Y1
    DataPoints[1][2] = 1; //T1

    DataPoints[2][0] = 2;
    DataPoints[2][1] = 3;
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