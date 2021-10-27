#include "json.h"

class UDP_Com
{
private:
    nlohmann::json Message;
    std::string JSON_Message;
    #define PORT 8080

    void EncodeMessage(); //Genererer string ud fra Message.
    void DecodeMessage(std::string JSON_message); //Genererer Message ud fra string

public:
    //konstant flow af positioner fra generede trajectory, fartøj hastighed og om den position er crack eller ej (bitumenflow)
    void UpdateMessage(float posx, float posy, float velx, float vely, float accx, float accy, int bitflow); //Updater json Message med ny data
    void SendMessage();   //Send besked til client
    void ReceiveMessage(std::string port);      //Modtag besked fra server

};
