from sense_hat import SenseHat
import time
from random import *

'''
v0.001 - 25.04.2018 - Can detect left-to-right
'''

sense = SenseHat()
sense.set_rotation(270)

dot = ""
rd = 0

# Inital dot
sense.clear()
sense.set_pixel(int(8/2),int(8/2),255,0,255)


if (dot): sense.set_pixels(dot)

while True:
	o = sense.get_orientation()
	pitch = o["pitch"]
	roll = o["roll"]
	yaw = o["yaw"]

	pitch = int(round(pitch, 0))
	roll = int(round(roll, 0))
	yaw = int(round(yaw, 0))

	print(pitch, roll, yaw)
	
	if roll > 0 and roll < 180: 
		print("Venstre?")
		rd = roll
		ro = "v"
	if roll > 180 and roll < 360: 
		print("Høyre?")
		rd = 360-roll
		ro = "h"
	if roll == 0 or roll == 360: 
		print("senter plan?")
		rd = 0
	
	# Distanse
	
	rand = randint(0,255)
	print("Distanse: "+str(rd))
	
	if (ro == "v"):
		# Start midt på
		xpos = 4-rd
		if xpos < 0: xpos = 0
		sense.set_pixel(xpos,0,rand,rand,rand)
	if (ro == "h"):
			xpos = 4+rd
			while xpos > 7: xpos = 7
			print(xpos)
			sense.set_pixel(xpos,1,rand,rand,rand)
	
	
	
	
	
	time.sleep(0.1)
