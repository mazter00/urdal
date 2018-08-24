#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.002 17.07.2018 Holiday Edition: Timers are added
'''

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

# Change back to the directory we started with (presumably)
os.chdir("/home/pi/pyscript/")


tsautosave = 0

from plotstats import plotstats
# plotstats printer ut, men returnerer xdiff24/168/730/8765

xdiff24,xdiff168,xdiff730,xdiff8765,tsplot24,tsplot168,tsplot730,tsplot8765,boolean = plotstats("AM")
print(xdiff24,xdiff168,xdiff730,xdiff8765,tsplot24,tsplot168,tsplot730,tsplot8765,boolean)

# Luft-fuktighet (xdiff er den samme, variabel overskrives bare

xdiff24,xdiff168,xdiff730,xdiff8765,tsplot24l,tsplot168l,tsplot730l,tsplot8765l,boolean = plotstats("AM-luft")
print("Variabler for LUFTFUKTIGHET:")
print(xdiff24,xdiff168,xdiff730,xdiff8765,tsplot24l,tsplot168l,tsplot730l,tsplot8765l,boolean)


sleep(15)

# ts = timestamp - brukes for timer-baserte funksjoner. Grapfing, ftp, backup
# 24, 168, 730, 8765


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
	
	diff24    = current-tsplot24
	diff168   = current-tsplot168
	diff730   = current-tsplot730
	diff8765  = current-tsplot8765
	
	diff24l   = current-tsplot24l
	diff168l  = current-tsplot168l
	diff730l  = current-tsplot730l
	diff8765l = current-tsplot8765l
	
	savediff = current-tsautosave
	if (savediff >= 3600):
		tempfile.close()
		sleep(2)
		print(Style.BRIGHT+"Autosaved AM/temp.log for sensor AM")
		sleep(2)
		tempfile = open("/home/pi/pyscript/AM/temp.log", 'a')
		tsautosave = current

	if (diff24 >= xdiff24):
		print(Style.BRIGHT+"Timestamp is over 10 minutes, runs plotting.py for DAY for sensor AM")
		tsplot24 = current
		sleep(10)
		os.system("python3 ./plotting.py -sensor AM")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-temp.png")

	if (diff168 >= xdiff168):
		print(Style.BRIGHT+"Timestamp is over X minutes, runs plotting.py for WEEK for sensor AM")
		tsplot168 = current
		sleep(20)
		os.system("python3 ./plotting.py -time 168 -sensor AM")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-temp-168.png")

	if (diff730 >= xdiff730):
		print(Style.BRIGHT+"Timestamp is over X minutes, runs plotting.py for MONTH for sensor AM")
		tsplot730 = current
		sleep(20)
		os.system("python3 ./plotting.py -time 730 -sensor AM")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-temp-730.png")

	if (diff8765 >= xdiff8765):
		print(Style.BRIGHT+"Timestamp is over X minutes, runs plotting.py for YEAR for sensor AM")
		tsplot8765 = current
		sleep(20)
		os.system("python3 ./plotting.py -time 8765 -sensor AM")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-temp-8765.png")

	if (diff24l >= xdiff24):
		print(Style.BRIGHT+"Timestamp is over 10 minutes, runs plotting.py for DAY for sensor AM plottype LUFT")
		tsplot24l = current
		sleep(10)
		os.system("python3 ./plotting.py -sensor AM -luft")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-luft.png")

	if (diff168l >= xdiff168):
		print(Style.BRIGHT+"Timestamp is over X minutes, runs plotting.py for WEEK for sensor AM plottype LUFT")
		tsplot168l = current
		sleep(20)
		os.system("python3 ./plotting.py -time 168 -sensor AM -luft")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-luft-168.png")

	if (diff730l >= xdiff730):
		print(Style.BRIGHT+"Timestamp is over X minutes, runs plotting.py for MONTH for sensor AM plottype LUFT")
		tsplot730l = current
		sleep(20)
		os.system("python3 ./plotting.py -time 730 -sensor AM -luft")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-luft-730.png")

	if (diff8765l >= xdiff8765):
		print(Style.BRIGHT+"Timestamp is over X minutes, runs plotting.py for YEAR for sensor AM plottype LUFT")
		tsplot8765l = current
		sleep(20)
		os.system("python3 ./plotting.py -time 8765 -sensor AM -luft")
		os.system("python3 ./ftp.py -upload /home/pi/pyscript/temp/urdal/AM-luft-8765.png")

	
	sleep(3)

print("read-dht.py is sompleted? Re-run it if needed")
s = input('--> ')
print(s)
