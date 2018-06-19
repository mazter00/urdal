#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' devtty.py
Used for finding the avaible port on Raspberry pi for Aurdino connection
It often changes when plugging in and out
'''

'''
v0.001 08.05.2018 Initial code
'''


import os

os.system("ls /dev/ttyAC* > devtty.txt << EOF")
print("Avaible port(s) written to devtty.txt, check it out!")
print("Cat'ing is as follows:")
os.system("cat devtty.txt")
