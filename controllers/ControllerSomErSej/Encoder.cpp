#include "include/Encoder.h"
//std::vector<std::vector<float>> MotionVec;

// Alter message from coordinates of two time stamps to coordinates with one time stamp
std::vector<Point> Encoder::getGoalsForTrajectoryPlanning(double time){
    
  std::vector<Point> TrajectoryGoals; //coordinates, final timestamp, and crack detected  
    
  int size = Goals.size();
  if (size > 2){
    if (SealingInitiated == false && beyondThreshold(PresentPosition(Goals.at(0), time),startThreshold) == false){ // If sealing not initiated, and first point is not beyond threshold
      Point goal = Goals.at(0);                       //Set goal to first point
      goal.goalT = timeAtY(goal,startThreshold);      //Edit time to be the time at which it will arrive
      TrajectoryGoals.push_back(Goals.at(0));         //Send goal
    } else if (SealingInitiated == false && beyondThreshold(PresentPosition(Goals.at(0), time),0.5 == true)){ // If sealing not initiated, and first point is beyond threshold
      SealingInitiated = true;
    } 
      
    if (SealingInitiated == true){
        
      for (size_t i = 0; i < 3; i++)
      {
        Goals.at(i).goalT = time + timeDelta(i);
        Goals.at(i).y = YAtTime(Goals.at(i), Goals.at(i).goalT);
        TrajectoryGoals.push_back(Goals.at(i));
      }
    
      Goals.erase(Goals.begin());

      if(checkWorkspace(PresentPosition(Goals.at(2), time),0.5) == false){
        SealingInitiated = false;
      }
    }
  }
    
  if (size == 2){

    for (size_t i = 0; i < 2; i++)
    {
      Goals.at(i).goalT = time + timeDelta(i);
      Goals.at(i).y = YAtTime(Goals.at(i), Goals.at(i).goalT);
      TrajectoryGoals.push_back(Goals.at(i));
    }

    Goals.erase(Goals.begin());

  } else if (size == 1){
    Goals.at(0).goalT = time + timeDelta(0);
    Goals.at(0).y = YAtTime(Goals.at(0), Goals.at(0).goalT);
    TrajectoryGoals.push_back(Goals.at(0));

    Goals.erase(Goals.begin());
  }

  return Goals;
   
  
}

double Encoder::timeAtY(Point point, float y){
  double tAty = point.frameT+(point.y + y + DistVehicle)/getVelocity(); // The time at which the point was found + The time it takes to get to y.
  return tAty;
}

double Encoder::YAtTime(Point point, double t){
  double y = point.y-(t-point.frameT)*getVelocity();
  return y;
}

bool Encoder::checkWorkspace(Point point, float margin, double time){
  // If point is within workspace, return true;
  return 0;
}

bool Encoder::beyondThreshold(Point point, float threshold, double time){
  // If point is beyond specified threshold, return true;
  return 0;
}

Point Encoder::PresentPosition(Point point, double time){ 
  //return delta tid * hastighed - her beregner vi hvor meget framen har rykket sig ift. det tidspunkt billedet er taget.
  Point NewY;
  double timePassed = time - point.frameT;
  NewY.y = point.y - (timePassed*getVelocity());

  return NewY;
}

double Encoder::getVelocity(){
    //Do sketchy shit in webots
    //Webots_encoder = Velocity: 
    return 2.22222; // 8 m/s
}

//Returns the timedifference between goal i and i-1. If goal = 0, then timeDelta returns 0;
double Encoder::timeDelta(int goal){
  double time = 0;

  if (goal > 0){
    float xDif = Goals.at(goal-1).x - Goals.at(goal).x;
    float yDif = Goals.at(goal-1).y - Goals.at(goal).y; 
    double distance = sqrt((xDif*xDif) + (yDif * yDif));

    time = distance/Velocity;
  }
  
  return time;
}

void Encoder::addGoal(Point goal){
  Point PushGoal = goal;
  float* pos = ConvertPixToMeter(goal.x, goal.y);
  PushGoal.x = pos[0];
  PushGoal.y = pos[1];
  
  Goals.push_back(PushGoal);
}

float* Encoder::ConvertPixToMeter(int X, int Y){
  float *PosXY = new float[2];
  
  float fovX = 2 * atan(SensorXSize / (2*focallength));// * 57.2957; for degrees
  float fovY = 2 * atan(SensorYSize / (2*focallength));// * 57.2957; for degrees

  float Ymeter = sin(fovX/2)*2*CameraMountHeight;
  float Xmeter = sin(fovY/2)*2*CameraMountHeight;

  PosXY[0] = (Xmeter/2) + (X*(Xmeter/ResX));
  PosXY[1] = (Ymeter/2) + (Y*(Ymeter/ResY));
  return PosXY;
}

