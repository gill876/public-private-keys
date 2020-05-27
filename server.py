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

HOST = ''
PORT = 5687

#generate private and public keys
privateKey = PrivateKey.generate()
publicKey = privateKey.public_key

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print("Connection from: ", addr)

    #receives public key from client in bytes
    fromClient = conn.recv(1024) #RECEIVE

    print("received public key")

    #create public key object from client
    client_pubKey = PublicKey(fromClient)

    #get public key in bytes
    send_publicKey = publicKey.__bytes__()

    #create server box
    server_box = Box(privateKey, client_pubKey)

    #sends over public key
    conn.send(send_publicKey) #SEND
    print("sent public key")

    #receive encrypted message
    encrypted = conn.recv(1024) #RECEIVE
    print("received encrypted message")

    message = server_box.decrypt(encrypted)
    print(message.decode('utf-8'))

    conn.close()
    print("closed connection")