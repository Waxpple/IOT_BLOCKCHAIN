#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 22:21:49 2020

@author: ethan
"""
import hashlib
import copy
import datetime
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

class MinimalBlock():
    def __init__(self, unique_id,index, timestamp, data, previous_hash):
        self.unique_id = unique_id
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()
    
    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.unique_id).encode('utf-8'))
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()
class MinimalChain():
    def __init__(self): # initialize when creating a chain
        self.unique_id = id(self)
        self.random_generator = Random.new().read
        self.key = RSA.generate(1024, self.random_generator) #generate public and private keys
        self.publickey = self.key.publickey()
        self.blocks = [self.get_genesis_block()]
        
    def get_genesis_block(self): 
        return MinimalBlock(0,
                            self.unique_id,
                            datetime.datetime.utcnow(), 
                            'This is my public key', 
                            self.publickey)
    
    def add_block(self, data):
        self.blocks.append(MinimalBlock(self.unique_id,
                                        len(self.blocks),
                                        datetime.datetime.utcnow(), 
                                        data, 
                                        self.blocks[len(self.blocks)-1].hash))
    def add_fake_block(self,data):
        self.blocks.append(MinimalBlock(self.unique_id,
                                        len(self.blocks),
                                        datetime.datetime.utcnow(), 
                                        data, 
                                        self.blocks[0].hash
        ))
    def get_chain_size(self): # exclude genesis block
        return len(self.blocks)-1
    
    def verify(self, verbose=True): 
        flag = True
        for i in range(1,len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                if verbose:
                    print(f'Wrong block index at block {i}.')
            if self.blocks[i-1].hash != self.blocks[i].previous_hash:
                flag = False
                if verbose:
                    print(f'Wrong previous hash at block {i}.')
            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False
                if verbose:
                    print(f'Wrong hash at block {i}.')
            if self.blocks[i-1].timestamp >= self.blocks[i].timestamp:
                flag = False
                if verbose:
                    print(f'Backdating at block {i}.')
        return flag
    
    def fork(self, head='latest'):
        if head in ['latest', 'whole', 'all']:
            return copy.deepcopy(self) # deepcopy since they are mutable
        else:
            c = copy.deepcopy(self)
            c.blocks = c.blocks[0:head+1]
            return c
    
    def get_root(self, chain_2):
        min_chain_size = min(self.get_chain_size(), chain_2.get_chain_size())
        for i in range(1,min_chain_size+1):
            if self.blocks[i] != chain_2.blocks[i]:
                return self.fork(i-1)
        return self.fork(min_chain_size)
    def get_prev_trans(self):
        return self.blocks[-1].data
    def get_block(self,block_index):
        return [self.blocks[block_index].data,self.blocks[block_index].previous_hash]
    def get_public_key(self):
        return self.publickey
    def decrypt(self,text):
        #for demo, real case should be private method
        return self.key.decrypt(text)