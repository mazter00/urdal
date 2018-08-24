#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import time,sleep

# Fargelegging
from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)

def printdiff(x):
	""" Print diff from supplied X """
	
	now = time()
	diff = now-x
	print(now,diff)
	return(diff)

def plotstats(sensor):
	""" Return ready-formatted printout """
	print("plotstats recieved: "+str(sensor))
	
	# ts = timestamp - brukes for timer-baserte funksjoner. Grapfing, ftp, backup
	# 24, 168, 730, 8765

	if (sensor == "TP" or sensor == "AM"):
		print("Ren TP/AM, legger til temp...")
		sensor = sensor+"-temp"
		
	try:
		tsplot24 = os.path.getmtime("/home/pi/pyscript/temp/urdal/"+sensor+".png")
	except:
		tsplot24 = 0

	try:
		tsplot168 = os.path.getmtime("/home/pi/pyscript/temp/urdal/"+sensor+"-168.png")
	except:
		tsplot168 = 0

	try:
		tsplot730 = os.path.getmtime("/home/pi/pyscript/temp/urdal/"+sensor+"-730.png")
	except:
		tsplot730 = 0

	try:
		tsplot8765 = os.path.getmtime("/home/pi/pyscript/temp/urdal/"+sensor+"-8765.png")
	except:
		tsplot8765 = 0
		
	# print(tsplot24,tsplot168,tsplot730,tsplot8765)
	# sleep(1)

	# Max diff
	# Trøbbel med proisp.no, 10-dobler timeren (og dermed alle timere)
	xdiff24   = 6000
	xdiff168  = xdiff24*(168/24)
	xdiff730  = xdiff168*(730/168)
	xdiff8765 = xdiff730*(8765/730)

	# To minutes

	xdiff24m   = int(  xdiff24/60)
	xdiff168m  = int( xdiff168/60)
	xdiff730m  = int( xdiff730/60)
	xdiff8765m = int(xdiff8765/60)

	# To hours

	xdiff24h   =   round(xdiff24m/60,2)
	xdiff168h  =  round(xdiff168m/60,2)
	xdiff730h  =  round(xdiff730m/60,2)
	xdiff8765h = round(xdiff8765m/60,2)

	# To days

	xdiff24d   = str(  round(xdiff24h/24,3))
	xdiff168d  = str( round(xdiff168h/24,3))
	xdiff730d  = str( round(xdiff730h/24,3))
	xdiff8765d = str(round(xdiff8765h/24,3))

	# Numbers to strings for nicely formatted printout

	xdiff24m   =   str(xdiff24m)
	xdiff168m  =  str(xdiff168m)
	xdiff730m  =  str(xdiff730m)
	xdiff8765m = str(xdiff8765m)

	xdiff24h   =   str(xdiff24h)
	xdiff168h  =  str(xdiff168h)
	xdiff730h  =  str(xdiff730h)
	xdiff8765h = str(xdiff8765h)

	# Printout

	hc = " hours chart: "
	so = " seconds or "
	mo = " minutes or "
	ho = " hours or "

	h  = [Style.BRIGHT+"24"+Style.NORMAL,Style.BRIGHT+"168"+Style.NORMAL,Style.BRIGHT+"730"+Style.NORMAL,Style.BRIGHT+"7654"+Style.NORMAL]
	h2 = [Style.BRIGHT+str(int(xdiff24))+Style.NORMAL,Style.BRIGHT+str(int(xdiff168))+Style.NORMAL,Style.BRIGHT+str(int(xdiff730))+Style.NORMAL,Style.BRIGHT+str(int(xdiff8765))+Style.NORMAL]
	h3 = [Style.BRIGHT+xdiff24m+Style.NORMAL,Style.BRIGHT+xdiff168m+Style.NORMAL,Style.BRIGHT+xdiff730m+Style.NORMAL,Style.BRIGHT+xdiff8765m+Style.NORMAL]
	h4 = [Style.BRIGHT+xdiff24h+Style.NORMAL,Style.BRIGHT+xdiff168h+Style.NORMAL,Style.BRIGHT+xdiff730h+Style.NORMAL,Style.BRIGHT+xdiff8765h+Style.NORMAL]
	h5 = [Style.BRIGHT+xdiff24d+Style.NORMAL,Style.BRIGHT+xdiff168d+Style.NORMAL,Style.BRIGHT+xdiff730d+Style.NORMAL,Style.BRIGHT+xdiff8765d+Style.NORMAL]

	print("{:>13}{}{:>15}{}{:>13}{}{:>14}{}{:>14} days".format(h[0],hc,h2[0],so,h3[0],mo,h4[0],ho,h5[0]))
	print("{:>13}{}{:>15}{}{:>13}{}{:>14}{}{:>14} days".format(h[1],hc,h2[1],so,h3[1],mo,h4[1],ho,h5[1]))
	print("{:>13}{}{:>15}{}{:>13}{}{:>14}{}{:>14} days".format(h[2],hc,h2[2],so,h3[2],mo,h4[2],ho,h5[2]))
	print("{:>13}{}{:>15}{}{:>13}{}{:>14}{}{:>14} days".format(h[3],hc,h2[3],so,h3[3],mo,h4[3],ho,h5[3]))

	# print(tsplot24,tsplot168,tsplot730,tsplot8765)
	# 4 intervals, 4 starting points, True
	return(xdiff24,xdiff168,xdiff730,xdiff8765,tsplot24,tsplot168,tsplot730,tsplot8765,True)

def main():
	print("plotstats.py main function")
	sensor = ""
	sensors = ["TP","AM","AM-luft"]
	for i in range(0,3):
		sensor = sensors[i]
		en,to,tre,fire,a,b,c,d,B = plotstats(sensor)
		print(a,b,c,d)
		# print(B)
		print("Printdiff a: "+str(printdiff(a)))
		print("Printdiff b: "+str(printdiff(b)))
		print("Printdiff c: "+str(printdiff(c)))
		print("Printdiff d: "+str(printdiff(d)))

import sys
if __name__ == "__main__":
    # execute only if run as a script
    
    pyv = sys.version_info[0]
    # print("Vi kjører Python version: "+str(pyv))
    
    assert pyv > int(2),"Krever Python 3, Python 2 er for dårlig"

    main()
