//This is a simple example and you may want to add more error handling and more robustness to your final code.
//C++ is a compiled language meaning your program's source code must be translated (compiled) before it can be run on your computer. On windowns machines you may experiment with Visual Studio Code and MSYS2.
//You can build the sample code with the folliwing steps on a Windows machine.
//build: g++ -o colaa-read .\colaa-read.cpp -lwsock32
//execute: .\colaa-read.exe


#include <iostream>
#include <WinSock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

int main()
{
    // Initialize Winsock
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0) {
        std::cout << "WSAStartup failed: " << result << std::endl;
        return 1;
    }

    // Create a socket
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        std::cout << "socket failed: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return 1;
    }

    // Prepare the sockaddr_in structure
    sockaddr_in servAddr;
    servAddr.sin_family = AF_INET;
    servAddr.sin_port = htons(2111);
    servAddr.sin_addr.S_un.S_addr = inet_addr("192.168.136.1");

    // Connect to server
    result = connect(sock, (sockaddr*)&servAddr, sizeof(servAddr));
    if (result == SOCKET_ERROR) {
        std::cout << "connect failed: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Build request string
    std::string s = "sRN LocationName";
    const char length = s.length();
    char* sendBuf = new char[length + 2];
    sendBuf[0] = (char) 0x02; //attach STX
    strcpy((sendBuf+1), s.c_str());
    sendBuf[length+1] = (char) 0x03; //attach ETX
    
    std::cout << "Request: ";
    for (int i = 0; i < (length+2); i++)
    {
        std::cout << sendBuf[i]; //print request
    }
    std::cout << "\n";

    // Send request string
    result = send(sock, sendBuf, strlen(sendBuf), 0);
    if (result == SOCKET_ERROR) {
        std::cout << "send failed: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Receive the response
    char recvBuf[1024];
    result = recv(sock, recvBuf, 1024, 0);
    if (result > 0) {
        std::cout << "Response: " << std::string(recvBuf, result) << std::endl;
    }
    else if (result == 0) {
        std::cout << "Connection closed" << std::endl;
    }
    else {
        std::cout << "recv failed: " << WSAGetLastError() << std::endl;
    }

    // Cleanup
    closesocket(sock);
    WSACleanup();
    return 0;
}