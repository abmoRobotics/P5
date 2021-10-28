#include <stdlib.h>
#include <string.h>
#include <sstream>
#include <iostream>

#include "include/UDP_Com.h"


int main(int argc, char const *argv[])
{
    printf("Client started\n");

    UDP_Com TEST;
    //Call UpdateMessage with position, velocity, acceleration, and bitumen flow
    TEST.ToggleDebug(true);
    TEST.UpdatePosition(0.3, 0.3);
    TEST.SendMessage();

} 


