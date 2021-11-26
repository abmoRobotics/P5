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

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>
#include <thread>
#include <mutex>


class Encoder
{
private:

    float Velocity = 4.444; // Velocity for robot movement, m/s
    float DistVehicle = 2.0; //Distance in m from camera origo to robot origo
    double tStart = 0;
    int round;
    bool debug = false;
    bool SealingInitiated = false;
    float startThreshold = 0.5;

    // Camera specifications
    float CameraMountHeight = 1.6; //Meters
    float focallength = 12;
    int ResX = 1936;
    int ResY = 1216;
    float SensorXSize = 11.34;
    float SensorYSize = 7.13;
    
public:

    std::vector<Point> Goals;

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

};