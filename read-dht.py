#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from time import sleep
import time
import os

# Fargelegging
from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)

print(os.getcwd())
tempfile = open('temp-dht.log', 'a')

os.chdir("Adafruit_Python_DHT")
print(os.getcwd())

os.chdir("examples")
print(os.getcwd())

import Adafruit_DHT
# sensor = Adafruit_DHT.DHT11
# (Virker, men kanskje ikke på humid) sensor = Adafruit_DHT.DHT22
sensor = Adafruit_DHT.AM2302
pin = 4

# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	
	d = datetime.now().isoformat()
	# print(d)
	# print(humidity)
	# print(temperature)
	
	s = d+" "+str(temperature)+" "+str(humidity)+"%"
	tempfile.write(s+"\n")
	print(s)
	
	# 25.06.2018: Det virker med 0.01, men det er veldig unødvendig
	# sleep(5)
	sleep(3)

