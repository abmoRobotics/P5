#include <mutex>
#include <vector>

class Encoder
{
private:
    float Velocity = 8.0; // km per hour
    float Velocity1;
    float VelocityMS;
    float timesetRobot;
    float DistVehicle = 4.0; //Distance in m from camera to robot
    float DistPoint_old = 0;
    float DistPoint = 0;
    float tSample_old = 0;
    float tSample;
    float tSampleP;
    float tClock;
    clock_t clickClock = 0;
    clock_t clickSample = 0;
    int round;

public:
    std::mutex MutexP;
    float POSY;
    float POSX;
    float TimeDetected;
    float TimeSet;
    float CrackDet;
      
    void GetVelocity();
    std::vector<std::vector<float>> Encoding(float, float, float, float, float);
    void GetDistPoint();
};