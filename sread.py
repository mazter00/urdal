'''
TODO: Finne ut av dev/tty automatisk

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

# sport = serial.Serial("/dev/ttyACM12", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM8", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM7", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM6", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM5", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM4", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM3", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM2", 115200, timeout=None)
# sport = serial.Serial("/dev/ttyACM1", 115200, timeout=None)
sport = serial.Serial("/dev/ttyACM0", 115200, timeout=None)


tempfile = open('temp.log', 'a')

# ts = timestamp
tsplotting = 0
tsftp = 0



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
			print("Debug i python: "+str(a,'utf-8'))
	
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
		print(d+' '+tempd)
		tempfile.write(d+' '+tempd+'\n')
		tempfile.flush()
		# print(type(tempd))
		
	# TODO: Lete etter feilmeldinger fra Arduino.
	
	current = int(time.time())
	
	# Skal være int for senere referanse: type(current)
	
	# print(current)
	
	diff = current-tsplotting
	# print(diff)
	
	if (diff >= 600):
		print("Diff is over 10 minutes, runs plotting.py")
		tsplotting = current
		os.system("python3 ./plotting.py")
	
	diff2 = current-tsftp
	
	if (diff2 >= 900):
		print("Diff2 is over 15 minutes, runs ftp.py")
		tsftp = current
		os.system("python3 ./ftp.py")
