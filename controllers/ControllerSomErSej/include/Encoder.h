#include <mutex>

class Encoder
{
private:
    float Velocity = 8.0; // km per hour
    float DistVehicle = 4.0; //Distance in m from camera to robot

public:
    std::mutex MutexP;
    float POSY;
    float POSX;
    float TimeDetected;
    float TimeSet;
    float CrackDet;
      
    void GetVelocity();
    void Encoding(float, float, float, float, float);
};