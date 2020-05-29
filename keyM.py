#!/usr/bin/env python3
from nacl.public import PrivateKey, Box, PublicKey


def genKey():
    """Generates PrivateKey object using PyNaCl"""
    #Generate secret private key that should not be shared or uploaded
    privateKey = PrivateKey.generate()
    return privateKey

def saveKey(filename):
    """Saves PrivateKey object into a byte file of '.pttk' extention 
    param:filename-> str
    eg: saveKey("private_key")
    return None"""
    with open((filename + '.pttk'), 'wb') as private_key_file:
        private_key = genKey()
        
        to_file_private_key = private_key.__bytes__()
        private_key_file.write(to_file_private_key)

def loadKey(filename):
    """Returns PrivateKey object from a byte file of '.pttk' extention 
    param:filename-> str
    eg: loadKey("private_key")
    return PrivateKey object"""
    with open((filename + '.pttk'), 'rb') as private_key_file:
        private_key = private_key_file.read()

        private_keyObj = PrivateKey(private_key)
        return private_keyObj