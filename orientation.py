from sense_hat import SenseHat
import time
from random import *

'''
v0.001 - 25.04.2018 - Can detect left-to-right
'''

sense = SenseHat()
sense.set_rotation(270)
sense.clear()

dot = ""
rd = 0
po = False

sense.clear()
# Pitch, 1-6

for i in range(1,6):
	print(i)
	sense.set_pixel(i,0,255,0,0)
	time.sleep(0.1)

for i in range(2,7):
	sense.set_pixel(4,i,0,255,0)
	time.sleep(0.2)

# sense.set_pixel(0,0,255,0,0)
# sense.set_pixel(int(8/2),int(8/2),randint(48,255),randint(48,255),randint(48,255))
time.sleep(2.20)

# Rød for Pitch
# Grønn for Roll
# Blue for Yaw

while True:
	sense.clear()
	
	o = sense.get_orientation()

	# opp/ned?
	pitch = o["pitch"]
	# venstre/høyre?
	roll = o["roll"]
	# ?
	yaw = o["yaw"]

	pitch = int(round(pitch, 0))
	roll = int(round(roll, 0))
	yaw = int(round(yaw, 0))

	print(pitch, roll, yaw)
	# 	>   rød		grønn	blå
	
	# Pitch (rød)
	
	if pitch > 0 and pitch < 180:
		print("ned?")
	
	if pitch > 0 and pitch > 180:
		print("opp?")
	
	# Pitch, center
	
	if pitch == 0:
		print("pitch center ned")
		pd = pitch
		po = "ned"
		sense.set_pixel(0,5,randint(48,255),0,0)
	if pitch == 360:
		print("pitch center opp")
		pd = 0
		po = "opp"
		sense.set_pixel(0,4,randint(48,255),0,0)
	
	# Roll (grønn)
	
	if roll > 0 and roll < 180: 
		# print("Venstre?")
		rd = roll
		ro = "v"
	if roll > 180 and roll < 360: 
		print("Høyre?")
		rd = 360-roll
		print("rd, høyre: "+str(rd))
		ro = "h"
		print("?")
	
	# Roll, Center
	
	if roll == 0: 
		print("senter venstre")
		rd = 0
		ro = "s"
		sense.set_pixel(4,4,0,randint(48,255),0)
	if roll == 360:
		print("senter høyre")
		rd = 0
		ro = "s"
		sense.set_pixel(5,4,0,randint(48,255),0)
		
	# Distanse
	
	# print("Distanse: "+str(rd))
		
	if (po == "opp"):
		ypos = 4-pd
		if ypos < 0: ypos = 0
		if ypos > 7: ypos = 7
		sense.set_pixel(4,ypos,200,0,0)
		exit()
	if (po == "ned"):
		ypos = 4+pd
		if ypos < 0: ypos = 0
		if ypos > 7: ypos = 7
		sense.set_pixel(4,ypos,100,0,0)
		
	
	if (ro == "v"):
		# Start midt på
		xpos = 4-rd
		if xpos < 0: xpos = 0
		print("xpos for set_pixel: "+str(xpos))
		print("RD var: "+str(rd))
		sense.set_pixel(xpos,4,0,randint(48,255),0)
		# 02.05.2018: Ser ut til å være riktig
	if (ro == "h"):
		xpos = 4+rd
		print("xpos før justering: "+str(xpos))
		while xpos > 7: xpos = 7
		print("xpos etter justering: "+str(xpos))
		print("xpos for set_pixel: "+str(xpos))
		sense.set_pixel(xpos,4,0,randint(48,255),0)
		# Korrekt
	
	time.sleep(0.25)

print("While not true anymore?")
