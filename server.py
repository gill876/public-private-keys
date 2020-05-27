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

HOST = ''
PORT = 5687

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print("Connection from: ", addr)

    fromClient = conn.recv(1024).decode('utf-8')

    print(fromClient)
    message = "hello there!"
    conn.send(message.encode())

    conn.close()