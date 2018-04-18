from sense_hat import SenseHat
import time
from random import *

# Gjennom testing, så vises ikke RGB-verdier som er 47 og/eller lavere!

'''
v0.002 - Lagde funksjoner som retunerer verdi. Ikke ferdig.
v0.001 - Lagde en while loop som tester Sensehat

TODO:
Lage en funksjon som dekker DISTANSE fra 0.25 til f.eks 0.44
og så beregne  RGB-verdien
'''

sense = SenseHat()

# Hjemme er 180 sense.set_rotation(180)
# Jobb er 270, tydeligvis

sense.set_rotation(270)
sense.clear()
sense.low_light = False

# Eksempel-pixler :D
sense.set_pixel(0,0,255,0,0)
sense.set_pixel(1,0,0,255,0)
sense.set_pixel(2,0,0,0,255)

# Format: sense.set_pixel(0,0,255,255,255)

print("starter loop")

# Random temperatur:
# Range: -40 -> +30

min = randint(-50,-10)
max = randint(25,50)

r = abs(min)+abs(max)
print("Max range is: "+str(r))
print("Rangen er fra/til: "+str(min)+" <-> "+str(max))

tall = randint(min,max)
print("Current Random Temp: "+str(tall))

if (tall > 0): 
	scala = abs(min)+tall
else:
	scala = abs(min-tall)
	
scalaba = scala
scala = scala/r
print("Scala er: "+str(scalaba)+" av "+str(r))
print("Scala er: "+str(scala))

def getR(scala):
	# 50%-75%: Gradvis fra 0 til 255
	# 75%-100%: 255
	
	# Rød er 50-100%
	if (scala < 0.5): return 0
	if (scala > 0.75): return 255
	
	v = getvalue(scala,"red")
	print("V, getB: "+str(v))
	return v
	
def getG(scala):
	# 0%-25%: Gradvis fra 0 til 255
	# 25%-75%: 255
	# 75%-100%: Gradvis fra 255 til 0
	if (scala > 0.25) and (scala < 0.75): return 255
	
	v = getvalue(scala,"green")
	print("V, getB: "+str(v))
	return v

def getB(scala):
	# 0%-25%: 255
	# 25%-50%: Gradvis fra 255 til 0
	
	if (scala < 0.25): return 255
	if (scala > 0.5): return 0
	
	v = getvalue(scala,"blue")
	print("V, getB: "+str(v))
	return v

def getvalue2(scala,target,mode,color):
	
	# print("[GV2] Scala: "+str(scala))
	print("Target: "+str(target))
	print("Mode: "+str(mode))
	print("Color: "+str(color))
	
	distanse = abs(scala-target)
	print("Distanse: "+str(distanse))
	
	# Relativ distanse
	rdist = distanse/0.25
	
	print("Relativ distanse: "+str(rdist))
	# print("Er dette et slags prosentall?")
	
	temp = int(255*rdist)
	if (mode == "stigende"): 
		print("Mode var stigende, vender om...")
		temp = (255-temp)
	else:
		print("Mode er synkende")
			
	if temp <= 47: 
		# Sørge for at det alltid lyser
		temp = 48
	
	# print(temp)
	return(temp)
		
	# exit("exit 3")

def getvalue(scala,color):
	if (color == "red"):
		if (scala > 0.5) and (scala < 0.75):
			# target = 0.25
			# synkende
			gv2 = getvalue2(scala,0.75,"stigende",color)
			print(gv2)
			return(gv2)
						
		return False
	
	if (color == "green"):
		if (scala < 0.25):
			# target = 0.25
			# stigende
			gv2 = getvalue2(scala,0.25,"stigende",color)
			print(gv2)
			return(gv2)
			
		if (scala > 0.75):
			# target = 0.75
			# synkende
			gv2 = getvalue2(scala,0.75,"synkende",color)
			print(gv2)
			return(gv2)
			
		return False
	
	if (color == "blue"):
		if (scala > 0.25) and (scala < 0.5):
			# target = 0.25
			# synkende
			gv2 = getvalue2(scala,0.25,"synkende",color)
			print(gv2)
			return(gv2)

		return False
	

getr = getR(scala)
getg = getG(scala)
getb = getB(scala)

getrtype = type(getr)
getgtype = type(getg)
getbtype = type(getb)

print("getr type: "+str(type(getr)))
print("getg type: "+str(type(getg)))
print("getb type: "+str(type(getb)))

print(getr, getg, getb)

print("done")
