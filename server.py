#!/usr/bin/env python3
from socket import *
import sys, os
from keyM import saveKey, loadKey
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
privateKey = None
publicKey = None

def getKeys(key_name='server_key'):
    global privateKey
    global publicKey

    if os.path.exists((key_name + '.key')):
        privateKey = loadKey(key_name)
        publicKey = privateKey.public_key
        print("**key retrieved")
    else:
        saveKey(key_name)
        print("**key generated")
        getKeys(key_name)

def main(listeners=1):
    global HOST
    global PORT
    global privateKey
    global publicKey

    getKeys()
    
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(listeners)
        conn, addr = s.accept()

        with conn:
            print("Connection from: ", addr)
            fromClient = conn.recv(1024).decode('utf-8') #RECEIVE
            if fromClient == "sending client key":
                conn.send("send client key".encode()) #SEND
                #receives public key from client in bytes
                fromClient = conn.recv(1024) #RECEIVE
                print("**received public key")

                #create public key object from client
                client_pubObj = PublicKey(fromClient)

                #get public key in bytes
                send_publicKey = publicKey.__bytes__()
                #sends over public key
                conn.send(send_publicKey) #SEND
                print("**sent public key")

                #create server box
                server_box = Box(privateKey, client_pubObj)

                while True:
                    #receive encrypted message
                    encrypted = conn.recv(1024) #RECEIVE
                    print("**received encrypted message")

                    message = server_box.decrypt(encrypted)
                    message = message.decode('utf-8')
                    if message == "exit(0)":
                        print("**client ended communication")
                        break

                    print("client: ", message)
                    message = message + " - read by server"
                    encrypted = server_box.encrypt(bytes(message,'utf-8'))
                    #send encrypted message
                    conn.send(encrypted) #SEND
            else:
                conn.send("error, please send client key".encode()) #SEND

        conn.close()
        print("**closed connection")

if __name__ == "__main__":
    main()