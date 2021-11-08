#include "include/Encoder.h"
#include <UDP_Com.h>
#include <iostream>

//Til multithreading
#include <sys/wait.h>
#include <unistd.h>
#include <thread>
#include <mutex>

void Encoder::Communication(){ //This function communicates throught the UDP_Com object with other software
  //CHILD PROCESS
  UDP_Com UDP;
  UDP.InitiateServer();
  UDP.ToggleDebug(true);
  int rounds = 0;
  while (1){
    UDP.ReceiveMessage();
    UDP.PrintMessage();
    // float *vel = UDP.ExtractVelocity();
    // MutexP.lock();
    // POSX+=vel[0];
    // POSY+=vel[1];
    // MutexP.unlock();
    rounds++;
  }
}

// int main(){
//     printf("Server virker\n");

        

//     //std::thread WeBotsController (Simulation, std::ref(*robot), std::ref(*motorL), std::ref(*motorR));
//     //std::thread CommunicationHandler (Communication);

//     //WeBotsController.join();
//     //CommunicationHandler.join();
//     std::cout << "Syncronization of Threads Complete" << std::endl;
// }