#include "include/UDP_Com.h"
#include <iostream>
#include <string.h>
#include <sstream>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>


void UDP_Com::EncodeMessage(){
    UDP_Com::JSON_Message = Message.dump(3);
}

void UDP_Com::DecodeMessage(std::string JSON_message){
    Message = nlohmann::json::parse(JSON_message);
}

//konstant flow af positioner fra generede trajectory, fartøj hastighed og om den position er crack eller ej (bitumenflow)
void UDP_Com::UpdateMessage(float posx, float posy, float velx, float vely, float accx, float accy, int bitflow){ //Updater json Message med ny data
    Message =
    {
        {"Position", 
            {
                {"X", posx}, 
                {"Y", posy} 
            }
        },
        {"Velocity",
            {  
                {"X", velx}, 
                {"Y", vely} 
            }
        },
        {"Acceleration",
            { 
                {"X", accx}, 
                {"Y", accy} 
            }
        },
        {"BitumenFlow", bitflow} 
    }; 

    EncodeMessage();
    
    std::cout << JSON_Message << std::endl;
    
} 

void UDP_Com::SendMessage(){  //Send besked til server

    int sock = 0;
    struct sockaddr_in serv_addr;
    // char *hello;
    char Message[] = "0";
    strcpy(Message,JSON_Message.c_str());

    char buffer[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary form
    if(inet_pton(AF_INET, "172.20.66.65", &serv_addr.sin_addr)<=0) 
    {
        printf("\nInvalid address/ Address not supported \n");
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
    }
    send(sock , Message , strlen(Message) , 0 );
    printf("Message sent\n");


}

void UDP_Com::ReceiveMessage(std::string port){  //Modtag besked fra client

}
