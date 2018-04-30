#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw, ImageFont
import os

'''
Script for å lage egne graph på egne forutsetninger
'''

# Options
grey = 240
border = 50
lengde = 950
heigth = 300

def version():
	return "v0.001"

print("PiPlot "+str(version())+" starting...")

'''
Masse forutsetninger

Vi antar at temp.log er dagens logging
Vi antar at vi kun skal vise for de siste 24 timer
Vi antar at vi selv velger størrelsen på grafen
Vi antar at vi må lete i FORRIGE dagen for å få 24 timer (v0.2+)
'''

if (os.path.exists("temp.log")):
	print("temp.log finnes")
	bytes = os.path.getsize("temp.log")
	print("Bytes: "+str(bytes))
else:
	print("temp.log finnes ikke, og ingen fil etterspurt. Exit")
	exit(2)
	
# Fint, vi har en fil for i dag
# Begynne med å lage bildet

# Graph Image
grafim = Image.new('RGB',(lengde,heigth), (grey,grey,grey))
grafim.save('graf.png')

# Tegne-objekt
graf = ImageDraw.Draw(grafim)

# Lage border

x0 = border
y0 = border
x1 = lengde-border
y1 = heigth-border

print( [ (x0,y0),(x1,y1) ] )

graf.rectangle( [ (border,border),(x1,y1) ],outline=0)
grafim.save("graf.png")

# Øvelse: Finne 0,0 pos i vår egen graf

pos = border,y1
print("Vi tror 0,0 er: "+str(pos))
graf.point( [ (pos) ] ,fill=0)
