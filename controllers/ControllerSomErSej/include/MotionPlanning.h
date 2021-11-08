


class MotionPlanning
{
private:
float a[2][5];

float DataPoints[3][3];
float theta = 0;
float theta_d = 0;
float theta_dd = 0;

void InitiateTestData();



public:
void ComputeA();
void GetPosition(float time);
void GetVelocity(float time);
void GetAcceleration(float time);


};