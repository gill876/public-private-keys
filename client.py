#!/usr/bin/env python3
from socket import *
import sys
import nacl.utils
from nacl.public import PrivateKey, Box

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

client_secretKey = PrivateKey.generate()

message = "hello world!"

clientSocket.send(message.encode())

fromServer = clientSocket.recv(1024).decode('utf-8')

print(fromServer)
clientSocket.close()