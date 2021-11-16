#include <vector>

class MotionPlanning
{
private:

    double a[2][5];
    float DP[3][4];
    double LastVel[2];
    bool debug = false;
    int numGoals = 0;

    double CalculateDesiredVelocity(double x1, double y1, double x2, double y2, double x3, double y3, double t1, double t2, char coor);

public:

    //Constructor
    MotionPlanning(){
        LastVel[0] = 0;
        LastVel[1] = 0;
    }

    void InitiateTestData();
    void ComputeA();
    void ComputeALinear();
    float* GetPosition(double t);
    float* GetVelocity(float t);
    float* GetAcceleration(float t);
    void Plan(std::vector<std::vector<float>>, double PresentTime);
};