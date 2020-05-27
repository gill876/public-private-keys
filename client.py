from socket import *
import sys

args = sys.argv

#######
# Future addition of optional arguments to enter custom port and ip
#######
if len(args) == 2:
    pass
if len(args) == 3:
    pass

serverHost = '0.0.0.0'
serverPort = 5687

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

clientSocket.send("hello world!".encode())

clientSocket.close()