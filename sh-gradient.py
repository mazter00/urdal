from sense_hat import SenseHat
import time
from random import *


'''
v0.004 - Fikset en bug med grønnfagen. Viste 255 istedenfor 0.
v0.003 - Fyller nå ut den ferdige fargen.
v0.002 - Lagde funksjoner som retunerer verdi. Ikke ferdig.
v0.001 - Lagde en while loop som tester Sensehat

TODO:

* Lage egne digits, pixels.

'''

# Bruke målt innetemperatur hvis inne er satt til True. Hvis ikke, bruk en random verdi
inne = False

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

# print("starter script")

# Random temperatur:
# Range: -40 -> +30

min = randint(-50,-10)
max = randint(20,50)

r = abs(min)+abs(max)
print("Total range is: "+str(r))
print("Rangen er fra/til: "+str(min)+" <-> "+str(max))

temp = sense.get_temperature_from_humidity()
temp2 = sense.get_temperature_from_pressure()
if temp2 == 0:
	sense.get_temperature_from_pressure()

# print(temp)
# print(temp2)

temp3 = temp+temp2
# print(temp3)

temp3 = int(temp3/2)

if (temp3 == 0) or (inne is False):
	tall = randint(min,max)
	print("Current Random Temp: "+str(tall))
else:
	tall = temp3
	print("Målt innetemperatur: "+str(temp3))

if (tall > 0): 
	scala = abs(min)+tall
else:
	scala = abs(min-tall)
	
scalaba = scala
scala = scala/r
print("Scala er: "+str(scalaba)+" av "+str(r))
print("Scala er: "+str(scala))

# Check for korrekt scala
if (scala > 1):
	print("Warning: Sette ny scala")
	# Må sette disse på nytt: max, r
	max = tall
	r = abs(min)+abs(max)

def getvalue2(scala,target,mode,color):
	
	# print("[GV2] Scala: "+str(scala))
	# Virker som at denne koden virker...
	# print("Target: "+str(target))
	# print("Mode: "+str(mode))
	# print("Color: "+str(color))
	
	distanse = abs(scala-target)
	# print("Distanse: "+str(distanse))
	
	# Relativ distanse
	rdist = distanse/0.25
	
	# print("Relativ distanse: "+str(rdist))
	# print("Er dette et slags prosentall?")
	
	temp = int(255*rdist)
	if (mode == "stigende"): 
		# print("Mode var stigende, vender om...")
		temp = (255-temp)
	else:
		# print("Mode er synkende")
		pass
			
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
			# print(gv2)
			return(gv2)
						
		return False
	
	if (color == "green"):
		if (scala < 0.25):
			# target = 0.25
			# stigende
			gv2 = getvalue2(scala,0.25,"stigende",color)
			# print(gv2)
			return(gv2)
			
		if (scala > 0.75):
			# target = 0.75
			# synkende. BUG: Tror det skal være "stigende" på begge to
			gv2 = getvalue2(scala,0.75,"stigende",color)
			# print(gv2)
			return(gv2)
			
		return False
	
	if (color == "blue"):
		if (scala > 0.25) and (scala < 0.5):
			# target = 0.25
			# synkende
			gv2 = getvalue2(scala,0.25,"synkende",color)
			# print(gv2)
			return(gv2)

		return False


def getR(scala):
	# 50%-75%: Gradvis fra 0 til 255
	# 75%-100%: 255
	
	# Rød er 50-100%
	if (scala < 0.5): return 0
	if (scala > 0.75): return 255
	
	v = getvalue(scala,"red")
	# print("V, getR: "+str(v))
	return v
	
def getG(scala):
	# 0%-25%: Gradvis fra 0 til 255
	# 25%-75%: 255
	# 75%-100%: Gradvis fra 255 til 0
	if (scala > 0.25) and (scala < 0.75): return 255
	
	v = getvalue(scala,"green")
	# print("V, getG: "+str(v))
	return v

def getB(scala):
	# 0%-25%: 255
	# 25%-50%: Gradvis fra 255 til 0
	
	if (scala < 0.25): return 255
	if (scala > 0.5): return 0
	
	v = getvalue(scala,"blue")
	# print("V, getB: "+str(v))
	return v

	

getr = getR(scala)
getg = getG(scala)
getb = getB(scala)

# Debug
# getr = "debug"

getrtype = type(getr)
getgtype = type(getg)
getbtype = type(getb)

if ((getrtype is int) and (getgtype is int) and (getbtype is int)):
	# print("All is int :)")
	pass
else:
		
	print("getr type: "+str(type(getr)))
	print("getg type: "+str(type(getg)))
	print("getb type: "+str(type(getb)))

print(getr, getg, getb)

# inverted farge
igetr = 80-getr
igetg = 80-getg
igetb = 80-getb

if (igetr < 0): igetr = 0
if (igetg < 0): igetg = 0
if (igetb < 0): igetb = 0


print("Inverted text colour: ")
print(igetr,igetg,igetb)

farge = (getr,getg,getb)

fargelist = []
# print(type(fargelist))

while len(fargelist) < 64:
	fargelist.append(farge)
	
# print(fargelist)

sense.set_pixels(fargelist)

# Vi burde skrive tallet også fra "var tall". Bruker show_message i første omgang

# sense.show_message("Min "+str(min),0.050,back_colour=fargelist[0],text_colour=(igetr,igetg,igetb))

sense.show_message(str(tall),0.120,back_colour=fargelist[0],text_colour=(igetr,igetg,igetb))
time.sleep(1.1)
sense.show_message(str(tall),0.060,back_colour=fargelist[0],text_colour=(igetr,igetg,igetb))

# sense.show_message("Max "+str(max),0.050,back_colour=fargelist[0],text_colour=(igetr,igetg,igetb))

# Ferdig, lar fargen stå, med lyset dimmet
sense.set_pixels(fargelist)

# time.sleep(3)
# sense.low_light = True
print("done")
