#include <stdlib.h>
#include <vector>
#include <bits/stdc++.h>

using namespace std;

#define ROW 10
#define COL 10

class Trajectory {
private:
// Driver program to test above functionx

	/* Description of the Grid-
	1--> The cell is not blocked
	0--> The cell is blocked */
    int grid[ROW][COL]
        = { { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
            { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
			{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 } };

    // Creating a shortcut for int, int pair type
    typedef pair<int, int> Pair;
    
    // Creating a shortcut for pair<int, pair<int, int>> type
    typedef pair<double, pair<int, int> > pPair;
    
    // A structure to hold the necessary parameters
    struct cell {
        // Row and Column index of its parent
        // Note that 0 <= i <= ROW-1 & 0 <= j <= COL-1
        int parent_i, parent_j;
        // f = g + h
        double f, g, h;
    };


    float VehicleVelocity;
    float PosX = 0;
    float PosY = 0;
    float VelX = 0;
    float VelY = 0;
    float AccX = 0;
    float AccY = 0;
    int BitumenFlow = 0;

public:
    void PosVectorGenerator();
    void ComputeCrackCost(vector<int> CrackVector);
    void ComputePath(stack<Pair> Path);
    void PathInterface();

    void setGoal(pair<int, int> dest, pair<int, int> src);

    //A* search algorithm
    bool isValid(int row, int col);
    bool isUnBlocked(int grid[][COL], int row, int col);
    bool isDestination(int row, int col, Pair dest);
    double calculateHValue(int row, int col, Pair dest);
    void tracePath(cell cellDetails[][COL], Pair dest);
    void aStarSearch(int grid[][COL], Pair src, Pair dest);

};