#!/usr/bin/env python3
from socket import *
import sys
import nacl.utils
from nacl.public import PrivateKey, Box, PublicKey

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

#generate private and public keys
privateKey = PrivateKey.generate()
publicKey = privateKey.public_key

#get public key in bytes
send_publicKey = publicKey.__bytes__()

#sends over public key
clientSocket.send(send_publicKey) #SEND
print("sent public key")

#receives public key from server in bytes
fromServer = clientSocket.recv(1024) #RECEIVE
print("received public key")

#create public key object from server
server_pubKey = PublicKey(fromServer)

#create client box
client_box = Box(privateKey, server_pubKey)

message = "hello world"

encrypted = client_box.encrypt(bytes(message,'utf-8'))

#send encrypted message
clientSocket.send(encrypted) #SEND
print("sent encrypted message")

clientSocket.close()
print("closed connection")