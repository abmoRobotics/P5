


class MotionPlanning
{
private:

float a[2][5];
float DataPoints[3][3];

public:
void InitiateTestData();
void ComputeA();
float* GetPosition(float t);
float* GetVelocity(float t);
float* GetAcceleration(float t);


};