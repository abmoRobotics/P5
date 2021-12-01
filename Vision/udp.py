import socket
import json



def SendUDP(x, y, detected, timeset, crack):
    serverAddressPort = ("127.0.0.1", 20001)
    bufferSize = 1024
    Data = {"Position": {"X": x, "Y": y}, "Time": {"Detected": detected, "TimeSet": timeset}, "Crack": {"DetectionIndex": crack}}

    data = json.dumps(Data)

    # # Create a UDP socket on client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # # Send to server using created UDP socket
    UDPClientSocket.sendto(data, serverAddressPort)

    