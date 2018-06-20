#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.011 23.05.2018 Added more debugging. Enabled by default. Creates a some noise, though
v0.010 22.05.2018 15:29 Added "blocking" debug, disabled by default. Was supposed to give a list of "blocked" temps...
v0.009 22.05.2018 Tried to reduce some output
v0.008 09.05.2018 - Now autosaves temp.log once per hour
v0.007 08.05.2018 11:43 - With a little bit of color
v0.006 08.05.2018: Finds avaible devtty on its own
v0.005 07.05.2018: Now *runs* script plott.py and ftp.py using os.system
v0.004 - 02.05.2018 - Now imports plotting if >10 minutes, and imports ftp.py if over 15 minutes
v0.003 - 02.05.2018 - Minsket endringer for lenge siden
v0.002 - 12.04.2018 - ...
'''
'''
TODO:
Show debug outputs of PONG
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

catchb = False
blocked = None
# Debug Outtemp? True/False
blokking = False

while True:
	# Arduino = 20, Python = .21
	sleep(0.21)
	
	if sport.inWaiting() > 0:
		a = sport.readline().rstrip()
	else:
		a = b""
		len = 0
	
	current = int(time.time())
	
	# Anta at variabel a alltid finnes
	if b"Temperature" in a:
		# print("Temperature found in string")
		b = a.split(b'= ')
		bl = len(b)
		if (bl != 2):
			print("len of b: "+str(bl))
			print("Tror dette er garbled?")
			print("a: "+str(a))
			print("b: "+str(b))
			pass
		
		# 09.04.2018: Det er Arduino's oppgave å oppgi ønsket antall desimaler
		# 12.04.2018: Try a Try block
		try:
			temp = b[1]
		except IndexError:
			# Dette skjer aldri?
			print("IndexError: A er: "+str(a))
		
		tempd = temp.decode('utf-8')
		
		# Try Boolean, True if it can be typecast to float
		tryb = False
		
		try: 
			float(tempd)
			tryb = True
		except:
			print(Style.BRIGHT+Fore.RED+"Typecasting to float failed, temperature may be invalid: "+str(a))
			tryb = False
	
		d = datetime.now().isoformat()
		
		savediff = current-tsautosave
		if (savediff >= 3600):
			tempfile.close()
			print(Style.BRIGHT+"Autosaved temp.log")
			tempfile = open('temp.log', 'a')
			tsautosave = current
			
		if (tryb is True):
			txt = Style.DIM+d+' '+Back.WHITE+Fore.RED+" "+str(tempd)+" "
			if blocked and blokking:
				txt = txt+Style.RESET_ALL+Style.DIM+" Blocked: "+blocked
			print(txt)
			tempfile.write(d+' '+tempd+'\n')
			tryb = False
			catchb = True
		tempfile.flush()
		# print(type(tempd))

	s = a.split()
	sl = len(s)
		
	j = ">"
	# 3 = Temp, 16 = Outtemp, 6 = NED/OPP
	# 19.06.2018: Etter reinstall, kommentert ut
	# if ((sl != 3) and (sl != 16) and (sl != 6)): 
	#	for i in s:
	#		j = j+" "+i.decode('utf-8')
	#		# print(j)
	#	print(j)
	#	print(sl)
		
	# Se etter "outtemp"
	if blokking is True:
		if b"Outtemp" in a:
			print("Outtemp found in a: "+str(a))
					
			c = a.decode('utf-8')
			c = c.split(' ')
			# print("x av c: "+str(len(c)))
			
			b1,b2 = c[2],c[4]
			out1,out2,out3 = c[-5],c[-3],c[-1]
			
			if (b1 == 0):
				blocked = str(out2)+" og "+str(out3)
			else: 
				print(c)
				print("b1 og b2: ",str(b1),str(b2))
				print("out1, 2 og 3: ",str(out1),str(out2),str(out3))
				# blocked = str(out1)+" "+str(out2)
	
	# debug 
	# Tar vekk debugging etter reinstall av OS, 19.06.20128
	# if (catchb is False):
	#	debug = 1
	#	if (debug == 1) and a: 
	#		# if "DEBUG Compare" not in str(a,'utf-8'):
	#		if b"DEBUG Compare" not in a:
	#			print(Style.DIM+"Partial line, Debug i python: "+str(a,'utf-8'))

	
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
