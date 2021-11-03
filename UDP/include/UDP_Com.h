#include "json.h"
#include <stdlib.h>

#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>

class UDP_Com
{
private:
    nlohmann::json Message;
    std::string JSON_Message;
    int Server_sockfd, Client_sockfd;
    struct sockaddr_in servaddr, cliaddr;
    #define PORT 8080
    #define MAXLINE 1024

    void EncodeMessage(); //Genererer string ud fra Message.
    void DecodeMessage(std::string JSON_message); //Genererer Message ud fra string
    bool debug = false;

public:
    UDP_Com()
    {
        Message =
        {
            {"Position", 
                {
                    {"X", 0.00}, 
                    {"Y", 0.00} 
                }
            },
            {"Velocity",
                {  
                    {"X", 0.00}, 
                    {"Y", 0.00} 
                }
            },
            {"Acceleration",
                { 
                    {"X", 0.00}, 
                    {"Y", 0.00} 
                }
            },
            {"BitumenFlow", 0} 
        }; 

        
    }

    //konstant flow af positioner fra generede trajectory, fartøj hastighed og om den position er crack eller ej (bitumenflow)
    void UpdatePosition(float posx, float posy);
    void UpdateVelocity(float velx, float vely);
    void UpdateAcceleration(float accx, float accy);
    void UpdateBitumenFlow(int BitFlow);
    float *ExtractPosition();
    float *ExtractVelocity();
    float *ExtractAcceleration();
    int ExtractBitumenFlow();
    
    void InitiateServer();      //Initiate Server to enable use of the ReceiveMessage() function
    void InitiateClient();      //Initiate Client to enable use of the SendMessage() function
    void SendMessage();         //Send message to Server. Remember to InitiateClient()!
    void ReceiveMessage();      //ReceiveMessage from Client. Remember to InitiateServer()!
    void PrintMessage();        //Prints Message at its current state
    void ToggleDebug(bool status);  //Enables/Disables printing of Debug information

    std::string convertToString(char* a, int size);

    

};
