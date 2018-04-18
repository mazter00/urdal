from sense_hat import SenseHat
import time
from random import *

# Gjennom testing, så vises ikke RGB-verdier som er 47 og/eller lavere!

'''
v0.002 - Lagde funksjoner som retunerer verdi. Ikke ferdig.
v0.001 - Lagde en while loop som tester Sensehat

''' TODO:
Lage en funksjon som dekker DISTANSE fra 0.25 til f.eks 0.44
og så beregne  RGB-verdien
'''

sense = SenseHat()

sense.set_rotation(180)
sense.clear()
sense.low_light = False

# Format: sense.set_pixel(0,0,255,255,255)

# Starter med blåfargen

# Blue loop
bl = 255
c = 0

print("starter loop")

# Random temperatur:
# Range: -40 -> +30

min = randint(-50,-10)
max = randint(25,50)

r = abs(min)+abs(max)
print("Max range is: "+str(r))
print("Rangen er fra/til: "+str(min)+" <-> "+str(max))

tall = randint(min,max)
print(tall)

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
	
	print("Nonexisting code for getR "+str(scala))
	return False
	
def getG(scala):
	# 0%-25%: Gradvis fra 0 til 255
	# 25%-75%: 255
	# 75%-100%: Grdvis fra 255 til 0
	if (scala > 0.25) and (scala < 0.75): return 255
	
	v = getvalue(scala,"green")
	
	print("Nonexisting code for getG "+str(scala))
	return False

def getB(scala):
	# 0%-25%: 255
	# 25%-50%: Gradvis fra 255 til 0
	
	if (scala < 0.25): return 255
	if (scala > 0.5): return 0
	
	v = getvalue(scala,"blue")
	
	print("Nonexisting code for getB "+str(scala))
	return False

def getvalue(scala,color):
	if (color == "red"):
		if (scala > 0.5) and (scala < 0.75):
			value = 255/(scala/0.25)
			print(value)
			exit()
			
		return False
	
	if (color == "green"):
		if (scala < 0.25):
			value = 255/(scala/0.25)
			print(value)
			return value

		if (scala > 0.75):
			value = 255/(scala/0.25)
			print(value)
			return value
			
		return False
	
	if (color == "blue"):
		if (scala > 0.25) and (scala < 0.5):
			return False
		return False
	

getr = getR(scala)
getg = getG(scala)
getb = getB(scala)

print(getr, getg, getb)

print("done")
