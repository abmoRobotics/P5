#pragma once
#include <mutex>
#include <vector>
#include <math.h>
#include "include/Point.h"
#include <UDP_Com.h>
// #include "include/MotionPlanning.h"
#include <iostream>
#include <vector>
#include <ctime>
#include </usr/local/webots/include/controller/cpp/webots/Display.hpp>

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>
#include <thread>
#include <mutex>


class Encoder
{
private:

    float Velocity = 4.444; // Velocity for robot movement, m/s
    float DistVehicle = 0.6857; //Distance in m from camera origo to robot origo
    float Xoffset = 0.5; //The X offset from camera origo to robot kinematic origo.
    double tStart = 0;
    int round;
    bool SealingInitiated = false;
    float startThreshold = 0.5;

    // Camera specifications
    float CameraMountHeight = 1.75; //Meters
    float focallength = 12;
    int ResX = 320;
    int ResY = 480;
    float SensorXSize = 11.34;
    float SensorYSize = 7.13;

    // Parameterer på målene på robotten. Specificeres som nogle "Standardmål" her, men kan (og bør) specificeres af setMeasurements() funktionen!
    float L0 = 0.25;    //Distancen imellem motorerne
    float L1 = 0.6;     //Længden på det første led.
    float L2 = 0.725;   //Længden på det andet led.
    float ActuatorLimit = 2.61799388; //150deg. Ydergrænsen som armene kan køre til. Målt fra "mid-plane".
    
public:

    std::vector<Point> Goals;
    std::vector<Point> GoalsHistory;
    
    bool debug = false;

    bool checkWorkspace(Point point, float margin, double time);
    bool beyondThreshold(Point point, float threshold, double time);
    std::vector<Point> getGoalsForTrajectoryPlanning(double time);
    Point PresentPosition(Point point, double time);
    double YAtTime(Point point, double t);
    double timeAtY(Point point, float y); // The time at which a point will be y meters behind origo of the robot.
    double getVelocity();
    float* ConvertPixToMeter(int X, int Y); //Returnerer meterværdier på et enkelt punkt, konverteret fra pixelværdier.
    void addGoal(Point goal);
    double timeDelta(int goal);
    void setMeasurements(float dist, float length1, float length2);
    void visualizePoints(webots::Display *display, double time, float* robotPos);
    int* getDisplayCoordinates(Point point, double time);

};