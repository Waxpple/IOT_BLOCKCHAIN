#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 22:23:51 2020

@author: ethan
"""
import blockchain
class eobject():
    def __init__(self):
        #init
        self.chain= blockchain.MinimalChain()
        
    #job method - broadcast data and encrypt data by using target public key
    def job(self,subject_list,target,data):
        self.subject_public_key = subject_list[target].chain.get_public_key()
        if(self.subject_public_key != subject_list[target].chain.get_block(0)[1]):
            print(target,' is fake!')
        self.data = self.subject_public_key.encrypt(data.encode('utf-8'),32)
        for i in subject_list:
            subject_list[i].chain.add_block(self.data)

    