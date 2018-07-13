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

if not os.path.exists("AM"):
		os.makedirs("AM")
		print("FOLDER "+str("AM")+" created!")

tempfile = open('/home/pi/pyscript/AM/temp.log', 'a')

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

tsautosave = 0

# ts = timestamp - brukes for timer-baserte funksjoner. Grapfing, ftp, backup
# 24, 168, 730, 8765

try:
	tsplot24 = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-temp.png")
except:
	tsplot24 = 0

try:
	tsplot168 = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-temp-168.png")
except:
	tsplot168 = 0

try:
	tsplot730 = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-temp-730.png")
except:
	tsplot730 = 0

try:
	tsplot8765 = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-temp-8765.png")
except:
	tsplot8765 = 0

# Set #2 for luftfuktighet

try:
	tsplot24l = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-luft.png")
except:
	tsplot24l = 0

try:
	tsplot168l = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-luft-168.png")
except:
	tsplot168l = 0

try:
	tsplot730l = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-luft-730.png")
except:
	tsplot730l = 0

try:
	tsplot8765l = os.path.getmtime("/home/pi/pyscript/temp/urdal/AM-luft-8765.png")
except:
	tsplot8765l = 0



# Max diff
xdiff24   = 600
xdiff168  = xdiff24*(168/24)
xdiff730  = xdiff168*(730/168)
xdiff8765 = xdiff730*(8765/730)

print("13.07.2018: TODO - hente fra sread.py")
print("Plotting intervals:")
print("24 hour chart: "+str(xdiff24))
print("168 hour chart: "+str(xdiff168))
print("730 hour chart: "+str(xdiff730))
print("8765 hour chart: "+str(xdiff8765))

while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	
	current = int(time.time())

	d = datetime.now().isoformat()
	# print(d)
	# print(humidity)
	# print(temperature)
	
	s = d+" "+str(temperature)+" "+str(humidity)+"%"
	tempfile.write(s+"\n")
	tempfile.flush()
	print(s)
	
	# 25.06.2018: Det virker med 0.01, men det er veldig unødvendig
	# sleep(5)
	
	savediff = current-tsautosave
	if (savediff >= 3600):
		tempfile.close()
		sleep(1)
		print(Style.BRIGHT+"Autosaved temp.log for sensor AM")
		sleep(1)
		tempfile = open("/home/pi/pyscript/AM/temp.log", 'a')
		tsautosave = current

	sleep(3)

print("read-dht.py is sompleted? Re-run it if needed")
s = input('--> ')
print(s)
