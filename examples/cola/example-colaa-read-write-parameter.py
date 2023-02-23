# This is a simple example and you may want to add more error handling and more robustness to your final code.

import socket

ip = "192.168.0.1"
port = 2111
STX = "\x02"
ETX = "\x03"

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connection to hostname on the port.
client_socket.connect((ip, port))

# LogIn sensor with password "81BE23AA"
cola_command = "sMN SetAccessMode 4 81BE23AA"
message = STX + cola_command + ETX
print("Request: " + message)
message = message.encode('ascii')
client_socket.sendall(message)
data = client_socket.recv(1024)
print("Response: " + data.decode('ascii'))

# write Location name to "Testsensor"
cola_command = "sWN LocationName +10 Testsensor"
message = STX + cola_command + ETX
print("Request: " + message)
message = message.encode('ascii')
client_socket.sendall(message)
data = client_socket.recv(1024)
print("Response: " + data.decode('ascii'))

# LogOut sensor
cola_command = "sMN Run"
message = STX + cola_command + ETX
print("Request: " + message)
message = message.encode('ascii')
client_socket.sendall(message)
data = client_socket.recv(1024)
print("Response: " + data.decode('ascii'))

# read location name
cola_command = "sRN LocationName"
message = STX + cola_command + ETX
print("Request: " + message)
message = message.encode('ascii')
client_socket.sendall(message)
data = client_socket.recv(1024)
print("Response: " + data.decode('ascii'))

client_socket.close()
