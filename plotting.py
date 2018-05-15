#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
V0.012 15.05.2018 Error output looks good, even calculates correct lines removed and shows correct error
v0.011 14.05.2018 16:38 It now plots again! (four+ days). Problem with y minimum; it's wrong
v0.010 14.05.2018 15:17 Happy with print output for verifylines
v0.009 14.05.2018 13:49 No longer tests [1] for existense, it will be caught in verifylines
v0.008 14.05.2018 03:03 (home): Added verifylines. Should replace xclean and yclean. Testing needed.
v0.007 11.05.2018 (home): Installs matplotlib if not installed (import failed)
v0.006 11.05.2018: Lots of tries to cleaning the y and x list
v0.005 07.05.2018: Lagd en argv, "-plot"
v0.004 02.05.2018: Lager ny liste på en ok måte grunnet floats
v0.003 12.04.2018: Fikset ymax
v0.002 20.03.2018: Fikse opp temp.log
'''

''' TODO:
14.05.2018 16:37: Fikse slik at y minimum ikke er 10 eller 20 ifra, plutselig droppes et helt tall
'''

'''
Kildehenvisning:
https://stackoverflow.com/questions/1614236/in-python-how-do-i-convert-all-of-the-items-in-a-list-to-floats
'''
'''
Dette scriptet gjør følgende:
Sjekker dagens dato i forhold til hva som er i temp.log
- Hvis ukjent dato finnes, rensk ut denne til egen fil
Lager to lister ut fra temp.log, x og y, konnverterer dette til riktig datatype
.. og plotter alt sammen
TODO: Ønsker å få skilt sjekking av temp.log til egen pythonfil.
'''

# 07.05.2018: Datetime behøves for string->timestruct->datime
from time import mktime
import datetime
from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)
import sys
import time


# OPTIONS

# 13.04.2018: Vi kutter ikke lenger i desimanlene fordi Arduino sender kun en desimal
# 08.05.2018: Vi tillar to desimaler fordi matplotlib takler det

def removedecimal():
	""" Trenger nok denne koden litt til hvis vi skal bytte sensor og den har tre desimaler """
	temp2 = open("temp2.log",'w')
	
	count = 0
	with open("temp.log") as temp:
		for line in temp:
			count = count+1
			line = line.strip()
			t = line.split(" ")
			txt = t[0]
			t = float(t[1])
			t = round(t,1)
			print("Linje: "+str(count)+" T: "+str(t))
			print("Print: "+str(txt)+" "+str(t))
			temp2.write(str(txt)+" "+str(t)+"\n")
	
	os.rename("temp2.log","temp.log")
	print("Rename succesful? for desimal-kutt")
	exit()

def verifylines(lines):
	""" Verfies by typecasting x and then y at the line before putting in into new list """
	import math
	
	import time
	tsstart = time.monotonic()
	
	lenx = len(lines)
	lenx2 = lenx*2
	print(Style.BRIGHT+"[VerifyLines]"+Style.NORMAL+" len er: "+str(lenx)+" and therefore "+str(lenx2)+" items")
	
	line2 = []

	reallist = []
	
	timy = None
	floaty = None
	floatyba = None
	
	# Error already printed?
	p = False
	
	errors = 0
	

	for i in range(0, len(lines)):
		
		# print statement
		p = False
		
		# print("For loop start")
		line2 = lines[i].split()
		# print(line2)
		# print(line2[0])
		# print(line2[1])
		
		# Third check first
		
		if len(line2) > 2: 
			strline = ' '.join(line2[2:])
			errors = errors+1
			pre = str("["+str(errors)+"] ["+str(i)+"] ")
			print(pre+"Third element was present"+Style.BRIGHT+Fore.YELLOW+": "+Style.DIM+Fore.RESET+str(strline))
			p = True
			continue
			
			# print("Setting other flags to False")
			vzb = True
		else:
			vzb = False

		# Test for element 1 (time)
		try:
			timy = time.strptime(line2[0],"%Y-%m-%dT%H:%M:%S.%f")
			vxb = True
		except:
			# print("Typecasting to timestruct failed")
			# print("i er "+str(i))
			# print(line2[0])
			errors = errors+1
			pre = str("["+str(errors)+"] ["+str(i)+"] ")
			print(pre+"["+str(errors)+"] "+"Typecasting to timestruct "+str(i)+Style.BRIGHT+Fore.YELLOW+": "+Style.NORMAL+Fore.WHITE+str(line2[0]))
			vxb = False
			p = True
			continue

		if (vxb == True):
			# print("x passed, tester y")
			# print(vx)
			
			try:
				floaty = float(line2[1])
				# if (floaty > 1000): print("line2: "+str(line2)), exit()
				vyb = True
			except:
				vyb = False
		
		# Check if y is okay
		if (vyb is True and floatyba is None): floatyba = floaty
		
		if (vyb is True):
			d = floaty-floatyba
			fabs = math.fabs(d)
			if (fabs >= 9): 
				errors = errors+1
				strline = "Diff: "+str(fabs)+" C: "+str(floaty)+" BA: "+str(floatyba)
				print("["+str(errors)+"] "+"Float distance too high at "+str(i)+Style.BRIGHT+Fore.YELLOW+": "+Style.RESET_ALL+str(strline))
				p = True
				continue
			
		# Catching and printing out errors
		# X shows errors right away; Here we show y errors (if needed)
		if (vyb is False):
			txtline = line2[1]
			errors = errors+1
			print("["+str(errors)+"] "+"Typecasting to float failed at "+str(i)+Style.BRIGHT+Fore.YELLOW+": "+Fore.RED+str(txtline))
			p = True
			continue

		# All successful, adding to list
		if (vxb is True and vyb is True and vzb is False):
			# print("Both are true")
			# print("vx "+str(vx))
			reallist.append(timy)
			
			# print("vy "+str(vy))
			reallist.append(floaty)
		else:
			if (p == False):
				errors = errors+1
				strline = ' '.join(line2[:])
				# print("["+str(errors)+"] "+"Unknown error/invalid input at "+str(i)+Style.BRIGHT+Fore.YELLOW+": "+Fore.RED+str(strline))
				print("["+str(errors)+"] "+"Unknown error/invalid input at "+str(i))
			



	print("Length of elements is now: " +str(len(reallist)))
	
	diffe = lenx2-len(reallist)
	print("We removed "+Style.BRIGHT+str(diffe)+Style.NORMAL+" items")
	
	l = len(reallist)
	l = int(l/2)
	
	print("Which means we are down to (lines): "+Style.BRIGHT+str(l))
	
	l2 = lenx-l
	print("Which means we removed this number of lines: "+Style.BRIGHT+str(l2))

	lrl = len(reallist)
	errorrate = round((diffe/lrl)*100,4)
	erp = str(errorrate)+"%"
	print("The errorrate is: "+Fore.RED+Style.BRIGHT+str(erp))

	
	print("Verifylines "+Fore.GREEN+"ended")
	tsend = time.monotonic()
	diff = tsend-tsstart
	print("[Verifylines] Time used: "+Style.BRIGHT+str(round(diff,3))+Style.NORMAL+" seconds")

	return(reallist)
			
def main():
	# Alt som er i main kjøres, IKKE ved import
	
	from colorama import init
	init()
	from colorama import Fore, Back, Style
	init(autoreset=True)

	import os
	try:
		import matplotlib.dates as mdates
	except:
		print(Style.BRIGHT+"import matplotlib failes, will download and install it using pip")
		
		os.system("sudo aptitude install libatlas-base-dev")
		os.system("sudo apt install python3-pip")
		os.system("sudo pip3 install --upgrade matplotlib")
		# os.system("pip3 install matplotlib")

	# 08.05.2018: For "jet" colormap
	# 09.05.2018: Får ikke til colormap, prøver igjen senere
	# from matplotlib import cm

	argplot = False

	wtdiff = 0

	if (len(sys.argv) > 1):
		
		# argv list
		al = sys.argv[:]
		del al[0]
		print(al)
				
		if ("-plot" in al):
			print(Style.BRIGHT+Fore.CYAN+"Plot argument found; will show plot at the end")
			drawplot = True
			argplot = True
			del al[0]
		if ("-time" in al):
			print("-time found in al, checking for argument")
			
			# Find in list
			ali = al.index("-time")
			ali1 = ali+1
			ali1txt = al[ali1]
			print("ali: "+str(ali))
			print("ali txt: "+str(ali1txt))
			print("Assume this is in hours")
			
			# Wanted time difference
			wtdiff = ali1txt
		else:
			print("End of argv")
			# Kanskje for "-ftp" ved senere anledning?
			print("Sys.argv 1: "+str(sys.argv[1]))
		

	kuttdesimaler = False

	# Set standard showplot
	if (argplot == False): drawplot = False

	import matplotlib
	# print(matplotlib.__version__)
	# print(str(matplotlib.__file__))

	# 09.05.2018: Tror ikke vi bruker numpy? Sjekk for dette, TODO
	import numpy as np
	# Bruker jeg numpy til noe som helst nå? 07.05.2018
	# print(np.version.version)
	# print(np.__path__)

	import os

	# Filen som skrives til heter alltid temp.log

	fs = os.path.getsize("temp.log")
	print(Style.BRIGHT+"Bytes: "+Style.NORMAL+str(fs))
	if (fs == 0): print("0 bytes, exit"), exit(405)

	# fikslinje()
	
	if kuttdesimaler is True:
		removedecimal()
	else:
		pass
		# print("Beholder desimalene")

	# Fordi vi heter Raspberry Pi
	matplotlib.use('tkagg')

	# 02.05.2018: Alltid importere etter tkagg
	import matplotlib.pyplot as plt

	# --- Kode for merging ---
	
	# Egne funksjoner
	from merge import today,extractdate,checkfolder
	
	from datetime import date,datetime
	
	if (wtdiff == 0):
		print("Wanted time difference not set; setting it to 24 hours")
		wtdiff = 24

	# TODO: Unødvendig å åpne denne mange ganger
	with open('temp.log',"r") as f:
		lines = f.readlines()
		
		# Get newest date
		
		linje = lines[-1]
		linje = linje.split()[0]
		t = datetime.strptime(linje,"%Y-%m-%dT%H:%M:%S.%f")
		# print("Type av t: "+str(type(t)))
		
		# Loop
		i = -1
		c = 0
		xlen = len(lines)-2
		
		print("type if wtdiff:"+str(type(wtdiff)))
		
		wtdiffs = float(int(wtdiff))
		
		print("type if wtdiffs:"+str(type(wtdiffs)))
		
		print("str diff: "+str(wtdiff))
		print("str diffs: "+str(wtdiffs))
		
		# Wanted time difference in seconds
		wtdiffs = wtdiffs*60*60
		
		print("Wanted time difference in seconds is: "+str(wtdiffs))
		
		while (c < xlen):
			i = i-1
			linje = lines[i]
			linje = linje.split()[0]
			try:
				t2 = datetime.strptime(linje,"%Y-%m-%dT%H:%M:%S.%f")
			except:
				print("Error in the line: "+str(linje))
				continue
				
			# print("type i loop (t2): "+str(type(t2)))
			# mk = time.mktime(t2)
			# print(mk)
			tdiff = t-t2
			# print("Type av tdiff: "+str(type(tdiff)))
			# print("tdiff: "+str(tdiff))
			
			h = float(tdiff.total_seconds())
			# print(h)
			
			print("h: "+str(h)+" wtdiff: "+str(wtdiffs))
			
			if (h >= wtdiffs):
				print("We've found what we were looking for! :D")
				break
				
			# print(t)
			# print("Type: "+str(type(t)))

	# --- KODE FOR PLOTTINGz --- 

	with open('temp.log',"r") as f:
		lines = f.readlines()
		lines2 = lines
	
	# print(lines)
	# exit()
	
	linjer = len(lines)
	if (linjer == 0): 
		print("Ingen linjer i temp.log, exit! Linjer er: "+str(linjer))
		exit()
	else:
		print("Linjer funnet: "+Style.BRIGHT+str(linjer))
	
	# 07.05.2018: Leser nå både x og y (tid og value)
	
	reallist = verifylines(lines)
	
	# Quickly seperate the list into x and y
	x = []
	y = []
	
	print("Seperating list")
	
	for i in range(0,len(reallist)):
		# print(reallist[i])
		
		j = i+1
		# 1%2=1=x
		# 2%2=0=y
		# 3%2=1=x
		
		m = j%2
		# print(m)
		
		# Alltid forvirra over hva som er x og y, partall og oddetall
		if (m == 1):
			x.append(reallist[i])
		if (m == 0):
			y.append(reallist[i])

	print("x and y created")
	# print(len(y))
	# print(len(x))
	
	# Assert the list is correct size
	assert len(y) == len(x), "Len av ylist and x are not the same"

	# Etter vi har fått y til å bli float, så finner vi nå max
	
	ymax = max(y)
	assert isinstance(ymax, float), "Max of y is not a float?"
	
	ymin = min(y)
	assert isinstance(ymin, float), "Min of y is not a float?"

	# Deretter fra time_struck til datetime
	xlist2 = []
	# d kanskje brukt tidligere, setter den til None	
	d = None

	for i in range(0, len(x)):
		# 09.05.2018: datetime.datetime?
		dt = datetime.datetime.fromtimestamp(mktime(x[i]))
		xlist2.append(dt)
		# print("dt: "+str(dt)+" i: "+str(i))

		
	# Selve plotte-kommandoen

	print("matplotlib is now plotting, waiting...")

	plt.grid(True)
	# plt.plot(xlist2,y,'k.',linewidth=1, markersize=1)
	plt.plot(xlist2,y,'k-',linewidth=1, markersize=1)

	# Finne en sensible min og max for å vise i matplotlib ETTER plot
	# (Egentlig bare minimum)

	
	# After input for mr. JO
	if (ymin > 20): 
		print("Setting own limit on y-axis, lower, to 20")
		plt.gca().set_ylim(bottom=20)

	# For x-aksen til å vise time:minutt
	myFmt = mdates.DateFormatter('%H:%M')
	plt.gca().xaxis.set_major_formatter(myFmt)

	plt.ylabel('Temperatur')
	
	# 09.05.2018: Siden jeg flytta kode...
	# Lager ny tittel

	dato = datetime.datetime.now().strftime('%d.%m.%Y')
	print("Dato: "+str(dato))
	plt.title(dato)

	# --- Legend eller Annontation ---

	plt.text(0,0,"Dagens høyeste temperatur",color='red',fontsize=30)

	# Her finner vi ut av vi har 40 ylabels
	# 09.05.2018: Useful for senere, sjekke midnatt, rekord, minimum
	locs, labs = plt.yticks()
	# print("Locs: "+str(locs))
	# print(labs)

	plt.savefig("temp/urdal/temp.png")

	if drawplot is True:
		print(Fore.GREEN+Style.BRIGHT+"Viser plot")
		plt.show()
	
if __name__ == "__main__":
    # execute only if run as a script
    main()
