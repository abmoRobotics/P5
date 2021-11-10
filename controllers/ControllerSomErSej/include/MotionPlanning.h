class MotionPlanning
{
private:

float a[2][5];
float DP[3][3];
float LastVel[2];
bool debug = false;

float CalculateDesiredVelocity(float x1, float y1, float x2, float y2, float x3, float y3, float t1, float t2, char coor);

public:

//Constructor
MotionPlanning(){
    LastVel[0] = 0;
    LastVel[1] = 0;
}


void InitiateTestData();
void ComputeA();
float* GetPosition(float t);
float* GetVelocity(float t);
float* GetAcceleration(float t);

};