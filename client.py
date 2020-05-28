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

clientSocket = None
client_box = None
send_publicKey = None
privateKey = None
publicKey = None
server_publicKey = None
server_pubObj = None

def connectServer(serverHost='0.0.0.0', serverPort=5687):
    global clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverHost, serverPort))

def getKeys(key_name='client_key'):
    global privateKey
    global publicKey

    if os.path.exists((key_name + '.key')):
        privateKey = loadKey(key_name)
        publicKey = privateKey.public_key
    else:
        saveKey(key_name)
        getKeys(key_name)

def initServerConnect():
    global clientSocket
    global publicKey
    global send_publicKey
    global server_publicKey
    global server_pubObj

    clientSocket.send("sending client key".encode()) #SEND
    fromServer = clientSocket.recv(1024).decode('utf-8')
    if fromServer == "send client key":
        #get public key in bytes
        send_publicKey = publicKey.__bytes__()

        #sends over public key
        clientSocket.send(send_publicKey) #SEND
        print("sent client public key")

        #receives public key from server in bytes
        server_publicKey = clientSocket.recv(1024) #RECEIVE
        #create public key object from server
        server_pubObj = PublicKey(server_publicKey)
        print("received server public key")
    else:
        print("public key was not sent")
        print("server: ", fromServer)


def createBox():
    global client_box
    global privateKey
    global server_pubObj

    #create client box
    client_box = Box(privateKey, server_pubObj)

def sendMessage(message="hello world"):
    global client_box
    global clientSocket

    encrypted = client_box.encrypt(bytes(message,'utf-8'))

    #send encrypted message
    clientSocket.send(encrypted) #SEND
    print("sent encrypted message")

def main():
    global clientSocket
    try: 
        connectServer()
        getKeys()
        initServerConnect()
        createBox()
        while True:
            message = input("Enter message to send to the server: ")
            if message == "exit(0)":
                print("closing client")
                sendMessage(message)
                break

            sendMessage(message)
            print("message sent to server")

            response = clientSocket.recv(1024) #RECEIVE
            response = client_box.decrypt(response)
            print("server: ", response.decode('utf-8'))

    except Exception as e:
        print("something went wrong:")
        print(e)
    finally:
        clientSocket.close()
        print("closed connection")

if __name__ == "__main__":
    main()