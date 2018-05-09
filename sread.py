#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.008 09.05.2018 - Now autosaves temp.log once per hour
v0.007 08.05.2018 11:43 - With a little bit of color
v0.006 08.05.2018: Finds avaible devtty on its own
v0.005 07.05.2018: Now *runs* script plott.py and ftp.py using os.system
v0.004 - 02.05.2018 - Now imports plotting if >10 minutes, and imports ftp.py if over 15 minutes
v0.003 - 02.05.2018 - Minsket endringer for lenge siden
v0.002 - 12.04.2018 - ...
'''

from datetime import datetime
import serial
from time import sleep
import time
import os

# Fargelegging
from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)

# Finne åpen port til Aurdino
os.system("python3 devtty.py")
with open("devtty.txt") as devfile:
	port = devfile.readline().strip()
	print("port: "+str(port))
	if port is None:
		exit("Fant ikke åpen  port")
		
print(Style.DIM+"Opening port at: "+str(port))
sport = serial.Serial(port, 115200, timeout=None)

tempfile = open('temp.log', 'a')

# ts = timestamp
tsplotting = 0
tsftp = 0
tsautosave = 0

while True:
	# Arduino = 20, Python = .21
	sleep(0.21)
	
	if sport.inWaiting() > 0:
		a = sport.readline().rstrip()
		
	else:
		a = b""
		len = 0
	
	# debug 
	debug = 1
	if (debug == 1) and a: 
		if "DEBUG Compare" not in str(a,'utf-8'):
			print(Style.DIM+"Debug i python: "+str(a,'utf-8'))
	
	current = int(time.time())
	
	# Anta at variabel a alltid finnes
	if b"Temperature" in a:
		# print("Temperature found in string")
		b = a.split(b'= ')
		# 09.04.2018: Det er Arduino's oppgave å oppgi ønsket antall desimaler
		# 12.04.2018: Try a Try block
		try:
			temp = b[1]
		except IndexError:
			print("IndexError: A er: "+str(a))
		
		tempd = temp.decode('utf-8')
		
		d = datetime.now().isoformat()
		# print(d)
		# print("Skrevet til fil: "+d+' '+tempd)
		print(Style.DIM+d+' '+Back.WHITE+Fore.BLUE+" "+str(tempd)+" ")
		
		savediff = current-tsautosave
		if (savediff >= 3600):
			tempfile.close()
			print(Style.BRIGHT+"Autosaved temp.log")
			tempfile = open('temp.log', 'a')
			tsautosave = current
			
		tempfile.write(d+' '+tempd+'\n')
		tempfile.flush()
		# print(type(tempd))
		
	# TODO: Lete etter feilmeldinger fra Arduino.

	diff = current-tsplotting
	# print(diff)
	
	if (diff >= 600):
		print(Style.BRIGHT+"Timestamp is over 10 minutes, runs plotting.py")
		tsplotting = current
		os.system("python3 ./plotting.py")
	
	diff2 = current-tsftp
	
	if (diff2 >= 900):
		print(Style.BRIGHT+"Timestamp is over 15 minutes, runs ftp.py")
		tsftp = current
		os.system("python3 ./ftp.py")

print("sread.py is sompleted? Re-run it if needed")
