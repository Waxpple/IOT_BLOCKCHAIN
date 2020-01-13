#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 21:02:42 2020

@author: ethan
"""

import hashlib
import copy
import datetime
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import eobject
#create a broadcast dictionary
my_eobject={}

#assign role
chair = eobject.eobject()
couch = eobject.eobject()
fridge = eobject.eobject()
#store itself in broadcast
my_eobject['chair'] = chair
my_eobject['couch'] = couch
my_eobject['fridge'] = fridge

#chair send a data to couch
sent_data = "I am chair. I am sending data to couch!"
chair.job(my_eobject,'couch',sent_data)
print('This is what chair wants to send: ',sent_data)
print('=================================================')

#fridge want to read the data chair sent to couch
middle_attack = fridge.chain.decrypt(fridge.chain.get_block(1)[0])
print('This is what fridge gets: ',middle_attack)
print('=================================================')
#this is what couch get
result = couch.chain.decrypt(couch.chain.get_block(-1)[0]).decode("utf-8")
print('This is what couch gets: ',result)
print('=================================================')


#now we try to forged a fake block
fake_chair = eobject.eobject()
my_eobject['chair2'] = fake_chair

#we pretend send data to couch
sent_fake_data = 'I am chair. Hey! couch tell me the passcode!'
fake_chair.job(my_eobject,'couch',sent_fake_data)
print('This is what fake chair wants to send: ',sent_fake_data)
print('=================================================')
result_from_fake = couch.chain.decrypt(couch.chain.get_block(-1)[0]).decode("utf-8")
print('This is what couch gets: ',result_from_fake)
print('=================================================')
#couch send password back with chair public key
passcode = 'I LOVE PARIS'
couch.job(my_eobject,'chair',passcode)
print('This is what couch sends: ',passcode)
print('=================================================')
fake_chair_get_ans = fake_chair.chain.decrypt(fake_chair.chain.get_block(-1)[0])
print('This is what fake chair gets:',fake_chair_get_ans)
print('=================================================')
#only real chair can read passcode using its private key
chair_get_ans = chair.chain.decrypt(chair.chain.get_block(-1)[0])
print('Only chair can see this: ',chair_get_ans.decode('utf-8'))
print('=================================================')

#IF I want to know my blockchain is orignal not forgery
print('Is my data legit?',chair.chain.verify())

#I try to modify a block
chair.chain.add_fake_block('My bank account got 5000NT')
print('After add a customed block, is my data legit?',chair.chain.verify())