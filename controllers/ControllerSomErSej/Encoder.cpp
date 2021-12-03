#include "include/Encoder.h"
//std::vector<std::vector<float>> MotionVec;

// Returns the appropriate goals for trajectory planning.
std::vector<Point> Encoder::getGoalsForTrajectoryPlanning(double time){
    
  std::vector<Point> TrajectoryGoals; //coordinates, final timestamp, and crack detected  
    
  int size = Goals.size();
  if (size > 2){
    if (SealingInitiated == false && beyondThreshold(PresentPosition(Goals.at(0), time),startThreshold, time) == false){ // If sealing not initiated, and first point is not beyond threshold
      Point goal = Goals.at(0);                       //Set goal to first point
      goal.goalT = timeAtY(goal,startThreshold);      //Edit time to be the time at which it will arrive
      goal.y = YAtTime(goal, goal.goalT);      
      TrajectoryGoals.push_back(goal);         //Send goal
      
    } else if (SealingInitiated == false && beyondThreshold(PresentPosition(Goals.at(0), time),0.5 == true, time)){ // If sealing not initiated, and first point is beyond threshold
      SealingInitiated = true;
    } 
      
    if (SealingInitiated == true){

      double timeItr = time;
      for (size_t i = 0; i < 3; i++)
      {
        Point goal = Goals.at(i);
        timeItr+=timeDelta(i);
        goal.goalT = timeItr;
        goal.y = YAtTime(Goals.at(i), goal.goalT);
        TrajectoryGoals.push_back(goal);
      }
      
      if(checkWorkspace(PresentPosition(Goals.at(2), time),0.01, time) == false){
        SealingInitiated = false;
      }

      Goals.erase(Goals.begin());

    }
  }
    
  if (size == 2){

    double timeItr = time;
      for (size_t i = 0; i < 2; i++)
      {
        Point goal = Goals.at(i);
        timeItr+=timeDelta(i);
        goal.goalT = timeItr;
        goal.y = YAtTime(Goals.at(i), goal.goalT);
        TrajectoryGoals.push_back(goal);
      }
    
      Goals.erase(Goals.begin());

  } else if (size == 1){
    double timeItr = time;
    
      for (size_t i = 0; i < 1; i++)
      {
        Point goal = Goals.at(i);
        timeItr+=timeDelta(i);
        goal.goalT = timeItr;
        goal.y = YAtTime(Goals.at(i), goal.goalT);
        TrajectoryGoals.push_back(goal);
      }
    
      Goals.erase(Goals.begin());
  }

  return TrajectoryGoals;
  
}

double Encoder::timeAtY(Point point, float y){
  double tAty = point.frameT+(point.y + y + DistVehicle)/getVelocity(); // The time at which the point was found + The time it takes to get to y.
  return tAty;
}

double Encoder::YAtTime(Point point, double t){
  double y = point.y-((t-point.frameT)*getVelocity());
  return y;
}

//Returns true if a point is within the workspace, by a margin.
bool Encoder::checkWorkspace(Point point, float margin, double time){

  float ButtomBorder = -(cos(ActuatorLimit)*L1) - L2 - margin;
  float part1 = L1+L2;
  float part2 = 0.5-(L0/2);
  float topBorder = -sqrt((part1*part1) - (part2*part2)) + margin ;

  std::cout << "ButtomBorder:" << ButtomBorder-DistVehicle << " TopBorder:" << topBorder-DistVehicle << " Point:'" << point.x << "," << point.y << "'" << std::endl;

  if(point.x < (1 - margin) && point.x > (0 + margin) && point.y > topBorder-DistVehicle && point.y < ButtomBorder-DistVehicle){
    return true;
  } else {
    if(debug){
      std::cout << "Goal is outside workspace" << std::endl;
    }
    return false;
  }
}

//Returns true if a point is beyond the treshold
bool Encoder::beyondThreshold(Point point, float threshold, double time){
  // If point is beyond specified threshold, return true;
  if (point.y < -DistVehicle - startThreshold){
    if (debug){
      std::cout << "Goal is beyond threshold" << std::endl;
    }
    return true;
  } else {
    return false;
  }
}

//Returnerer aktuel pposition i camera workspace.
Point Encoder::PresentPosition(Point point, double time){ 
  //return delta tid * hastighed - her beregner vi hvor meget framen har rykket sig ift. det tidspunkt billedet er taget.
  Point NewY = point;
  double timePassed = time - point.frameT;
  NewY.y = point.y - (timePassed*getVelocity());

  return NewY;
}

double Encoder::getVelocity(){
    //Do sketchy shit in webots
    //Webots_encoder = Velocity: 
    return 0.3; // m/s = 8km/h
}

//Returns the timedifference between goal i and i-1. If goal = 0, then timeDelta returns 0;
double Encoder::timeDelta(int goal){
  double time = 0;

  if (goal > 0 && Goals.size() > 1){
    float xDif = Goals.at(goal-1).x - Goals.at(goal).x;
    float yDif = Goals.at(goal-1).y - Goals.at(goal).y; 
    double distance = sqrt((xDif*xDif) + (yDif * yDif));

    time = distance/Velocity;
  }
  
  return time;
}

//add goal to goalsvector. Takes in goal with xy in camera pixel values!
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

  float Xmeter = sin(fovY/2)*2*CameraMountHeight;
  float Ymeter = sin(fovX/2)*2*CameraMountHeight;

  PosXY[0] = (X*(Xmeter/ResX));
  PosXY[1] = (Y*(Ymeter/ResY));

  // std::cout << "ConvertPixToMeter: X:" << PosXY[0] << " Y:" << PosXY[1] << std::endl;
  return PosXY;
}

void Encoder::setMeasurements(float dist, float length1, float length2){
  L0 = dist;
  L1 = length1;
  L2 = length2;
}
