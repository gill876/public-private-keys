#!/usr/bin/env python3
from nacl.public import PrivateKey, Box, PublicKey
import pickle

def genKey():
    """Generates PrivateKey object using PyNaCl"""
    #Generate secret private key that should not be shared or uploaded
    privateKey = PrivateKey.generate()
    return privateKey

def saveKey(filename):
    """Saves PrivateKey object into a byte file of '.key' extention 
    param:filename-> str
    eg: saveKey("private_key")
    return None"""
    with open((filename + '.key'), 'wb') as private_key_file:
        private_key = genKey()
        pickle.dump(private_key, private_key_file)

def loadKey(filename):
    """Returns PrivateKey object from a byte file of '.key' extention 
    param:filename-> str
    eg: loadKey("private_key")
    return PrivateKey object"""
    with open((filename + '.key'), 'rb') as private_key_file:
        private_key = pickle.load(private_key_file)
        return private_key