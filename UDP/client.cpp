#include <stdlib.h>
#include <string.h>
#include <sstream>
#include <iostream>

#include "include/UDP_Com.h"


int main(int argc, char const *argv[])
{
    printf("Client started\n");

    UDP_Com TEST;
    TEST.UpdateMessage(0.1,0.1,0.1,0.1,0.1,0.1,0);

} 


