from sense_hat import SenseHat
import time
from random import *

# Gjennom testing, så vises ikke RGB-verdier som er 47 og/eller lavere!

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

exit()

while (bl > 0):
	row = 0
	
	# c = counter, c2 er current counter
	c2 = c
	while (c2 > 7):
		row += 1
		c2 -= 8
	
	if (c2 < 0): c2 = 0
	
	print("c, c2, row: "+str(c)+" "+str(c2)+" "+str(row))
	
	x = c2
	y = row
	while (y > 7): y -= 8
	
	# print("x,y,bl = "+str(x),str(y),str(bl))
	
	liste = [0,bl,0]

	if (bl <= 47): 
		print("Verdi for lav, break "+str(bl))
		break
	
	# print(type(liste))
	print(x,y,liste)
	
	sense.set_pixel(x,y,liste)

	getp = sense.get_pixel(x,y)
	tre = getp[1]
	if (tre == 0): print("Nullverdi i xy: "+str(x)+" "+str(y)); break
	
	# Oppdaterer variabler på slutten
	
	bl -= 1
	c += 1
	
	time.sleep(0.025)
	# sense.clear()

print("done")
