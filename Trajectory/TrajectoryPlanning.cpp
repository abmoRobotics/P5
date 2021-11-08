#include "include/planning.h"




int main(){
    Trajectory Traj;
    //Traj.PosVectorGenerator();

    //setGoal(destination, source)
    //source skal være ift. end-effektoren på vores robot.
	Traj.setGoal({1, 6}, {5,5});

    vector<vector<int>> CrackVec{
        {1, 40},
        {10, 41},
        {8, 42}
    };

	return (0);
}