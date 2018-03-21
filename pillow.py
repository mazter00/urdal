#!/usr/bin/python3

# 21.03.2018 10:50 - v0.002 - Now we Draw with Power (startet å importere ImageDraw)

from PIL import Image,ImageDraw, ImageFont
import sys
import os.path
import subprocess
import shutil

# OPTIONS
showp = False
step3 = True

if step3 is not True:

	if os.path.isfile("real.jpg") and showp is True:
		print("eksisterer, åpner nå")
		subprocess.call("feh real.jpg &", shell=True)
		subprocess.call("pkill feh")
	else:
		print("eksisterer ikke, exit")
		# exit(2)

	# Åpner meg egen custom bilde (innriss.jpg)

	im = Image.open("innriss.jpg")
	width, heigth = im.size
	print("im.size: "+str(im.size))
	print("bredde x høyrde: "+str(width)+" "+str(heigth))

	# Sjekker om vi kan manipulere det
	# Kilde: http://pillow.readthedocs.io/en/4.2.x/reference/ImageDraw.html

	# kopier fra orginalfil

	shutil.copy("innriss.jpg","innriss2.jpg")

	im2 = Image.open("innriss2.jpg")
	draw = ImageDraw.Draw(im2)
	print(draw)

	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 9)
	# draw.text((x, y),"Sample Text",(r,g,b))

	# Hardkoda koordinater - im2 har 40x52

	draw.text((9, 15),"23.7",(255,255,0),font=font)
	im2.save('innriss2.jpg')
	
else:
	print("Step3?: "+str(step3))

	# How to insert? First, let's be able to convert middle color to any color we want. We know the file is 50x50 (v2 of the marker image)

	im = Image.open("50-trans-red.png")
	print(im)
	
	width, heigth = im.size
	print(im.size)
	
	w2 = int(width/2)
	h2 = int(heigth/2)
	
	print("w2: "+str(w2))
	print("h2: "+str(h2))
	
	pixels = im.load()
	print(pixels)
	
	null = pixels[1,1]
	print(null)
	
	color = pixels[h2,w2]
	print(color)
	
	# ^^^ Color to be replaced ^^^
	
	newc = (0,255,0,0)
	
	countr = 0
	
	rlist = []
			
	for x in range(0, width):
		for y in range(0, heigth):
			c = pixels[x,y]
			if c[-1] == 0: print("Alpha i "+str(x)+"x"+str(y))
			if c[0] == 255 and c[-1] == 255: 
				print("To be replaced! "+str(x)+"x"+str(y))
				countr = countr + 1
				rlist.append((x,y))
	
	print("Antall pixler å overskrive: "+str(countr))
		
	print("rlist   : "+str(rlist))
	
	rlistlen = len(rlist)
	print("rlistlen: "+str(rlistlen))
	
	print("rlist -1: "+ ''.join(str(rlist[-1] )))
	print("rlist -1: "+ ''.join(str(rlist[1] )))
	
	for r in range(0, rlistlen):
		print("Pixel "+str(r)+" skal skifte farge til: "+''.join(str(rlist[r] ))
