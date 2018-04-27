'''
TODO: Finne ut av dev/tty automatisk
TODO: Minske endringer

v0.002 - 12.04.2018 - ...
'''

from datetime import datetime
import serial
from time import sleep

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
