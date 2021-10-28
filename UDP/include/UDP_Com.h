#include "json.h"

class UDP_Com
{
private:
    nlohmann::json Message;
    std::string JSON_Message;
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
    void SendMessage();         //Send besked til client
    void ReceiveMessage();      //Modtag besked fra server
    void PrintMessage();        //Prints Message at its current state
    void ToggleDebug(bool status);  //Enables/Disables printing of Debug information

    std::string convertToString(char* a, int size);

    

};
