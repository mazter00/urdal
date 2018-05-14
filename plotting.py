#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.008 14.05.2018 03:03 (home): Added verifylines. Should replace xclean and yclean. Testing needed.
v0.007 11.05.2018 (home): Installs matplotlib if not installed (import failed)
v0.006 11.05.2018: Lots of tries to cleaning the y and x list
v0.005 07.05.2018: Lagd en argv, "-plot"
v0.004 02.05.2018: Lager ny liste på en ok måte grunnet floats
v0.003 12.04.2018: Fikset ymax
v0.002 20.03.2018: Fikse opp temp.log
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

def fikslinje():
	"""Fikse manglende linjeskift i temp.log"""
	
	with open("temp.log") as ff:
		f = ff.read()
		
		s = f.split()
		print("[fikslinje] 0: "+str(s[0])+" 1: "+str(s[1]))
		# TODO: Kode ikke ferdig.
		# Dette er et ikke-problem, men en bug som kan komme opp senere
		# exit(10)
		# pass

def removedecimal():
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
	
def getmax(y,x):
	if x is None: exit("No second list given")
	
	ymax = max(y)
	print("max er: "+str(ymax))
	
	try:
		float(ymax)
	except:
		print("Could not convert to float from max in given list")
		print("max is: "+str(ymax))
		indeks = y.index(ymax)
		
		del y[indeks]
		del x[indeks]
		
		print("POPPED Item number from both given lists: "+str(indeks))
		# Gives new max. He who asked should ask again if it's still an error
		print("Gives new max. He who asked should ask again if it's still an error")
		return(max(y))

def pop(x,y,i):
	# print("type: "+str(type(x[i])))
	# Foreløpig kun x som bruker denne

	ylen = len(y)
	xlen = len(x)
	
	# print("[pop] Before "+str(ylen)+" "+str(xlen))
	
	assert (xlen == ylen),"Lists is not of equal length?"
	
	# print("i: "+str(i))
	# print("y av i: "+str(y[i]))
	# print("x av i: "+str(x[i]))
	# print("[POP] POPPED Item number from both list y and list x: "+str(i))
	print("Kunne ikke konvertere til structtime: "+Style.BRIGHT+Fore.RED+str(x[i]))
	
	# print("y av i som slettes: "+str(y[i]))
	
	del y[i]
	del x[i]
	
	ylen2 = len(y)
	xlen2 = len(x)

	# print("[pop] After "+str(ylen2)+" "+str(xlen2))
	
	assert ((ylen != ylen2) or (xlen != xlen2)),"Item not popped?"


def yclean(y,x,lines):
	""" Cleaning y list by trying to convert to float """
	count = 0
	pop = False
	
	for i in y:
		try:
			i2 = float(i)
		except:
			# print("Delete item no. "+str(count))
			pop = True
		if pop is True: 
			print("Kunne ikke konvertere til float: "+Style.BRIGHT+Fore.RED+str(i))

			indeks = y.index(i)
			print("Indeks: "+str(indeks))

			string = str(i)
			print("String: "+str(string))
			
			del y[indeks]
			
			j = 0
			for j in range(0,len(lines)):
				if string in lines[j]:
					print("Found a partial hit at pos: "+str(j))
					par = lines[j]
					print("slette pos par?"+str(par))
					del lines[j]
					j-1
					del lines[j]
			
			# print("POPPED item "+str(count)+" in list y!")
			
			xslett = x[count]
			print(xslett)
			
			del x[count]
			# print("POPPED item "+str(count)+" in list x!")
			count = count-1
			pop = False

		count = count+1
	
	# Returnere lista
	return(y)

def maxy(y):
	
	maks = max(y)
	print("Current max: "+str(maks))
	print("Type: "+str(type(maks)))
		
	return(y)
	
def xclean(x,y):
	""" Clean x list by trying to convert string to datetime """

	i = None
	xlist = []
	xlen = len(x)
	
	# Fra string til time_struct

	# print("Len av liste: "+str(len(x)))
	for i in range(0, len(x)):
		# print("x av i: "+str(x[i]))
		# print("p "+str(time.strptime(x[i],"%Y-%m-%dT%H:%M:%S.%f")))
		# Prøver å sette xlist som limit istedenfor x?
		if (i >= len(y)): 
			print("Slettet så mange at vi har kommet oss til slutten av lista "+str(i)+" "+str(len(x))+ " "+str(len(xlist)))
			break
		try:
			xlist.append(time.strptime(x[i],"%Y-%m-%dT%H:%M:%S.%f"))
		except:
			print("Before calling pop...")
			print("y: "+str(y[i])+" x: "+str(x[i]))
			print("y: "+str(len(y))+" x: "+str(len(x)) +" xlist: "+str(len(xlist)))
			pop(x,y,i)

	return(x,xlist)

def verifylines(lines):
	""" Verfies by typecasting x and then y at the line before putting in into new list """
	import time
	
	lenx = len(lines)
	print("[VerifyLines] len er: "+str(lenx))

	# Verified x
	vx = []
	vy = []
	
	line2 = []

	# I have the option to create x and y right now
	reallist = []
	
	timy = None
	floaty = None
	

	for i in range(0, len(lines)):
		
		# print("For loop start")
		line2 = lines[i].split()
		# print(line2)
		# print(line2[0])
		# print(line2[1])

		try:
			timy = time.strptime(line2[0],"%Y-%m-%dT%H:%M:%S.%f")
			vxb = True
		except:
			print("Typecasting to timestruct failed")
			print("i er "+str(i))
			print(line2[0])
			vxb = False

		if (vxb == True):
			# print("x passed, tester y")
			# print(vx)
			
			try:
				floaty = float(line2[1])
				vyb = True
			except:
				print("Typecasting to float failed")
				print("i er "+str(i))
				print(line2[1])

				vyb = False
			
		if (vxb and vyb is True):
			# print("Both are true")
			# print("vx "+str(vx))
			reallist.append(timy)
			
			# print("vy "+str(vy))
			reallist.append(floaty)


	print("Verifylines ended")
	print("Length is now: " +str(len(reallist)))
	
	print("How many did we remove?")
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



	if (len(sys.argv) > 1):
		if (sys.argv[1] == "-plot"):
			print(Style.BRIGHT+Fore.CYAN+"Plot argument found; will show plot at the end")
			drawplot = True
			argplot = True
			
		else:
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

	# Egne funksjoner
	from merge import today,extractdate,checkfolder
	
	if kuttdesimaler is True:
		removedecimal()
	else:
		pass
		# print("Beholder desimalene")

	# Fordi vi heter Raspberry Pi
	matplotlib.use('tkagg')

	# 02.05.2018: Alltid importere etter tkagg
	import matplotlib.pyplot as plt

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
			
	y = []
	x = []
	
	feil = 0
	c = 0
	for i in range(0,len(lines)):
		x.append(lines[c].split()[0])
		c = c+1
	
	tag = False
	c = 0
	for i in range(0,len(lines)):
		a = lines[c].split()
		
		try:
			b = a[1]
		except:
			feil = feil+1
			# print("Feil i item nummer: "+str(c))
			
			# Fjerner tilsvarende item i forrige liste som er x
			del x[c]
			
			# print(a)
			tag = True
		
		if tag == False: y.append(b)
		if tag == True: tag = False
		c = c+1

	print("Antall feil funnet in liste-laging: "+Style.BRIGHT+str(feil))
	print("Len av y: "+str(len(y))+" og len av x: "+str(len(x)))

	# Assert the list is correct size
	assert len(y) == len(x), "Len av ylist and x are not the same"

	reallist = verifylines(lines)
	print(len(reallist))
	# print(reallist)
	
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
		
		if (m == 1):
			y.append(reallist[i])
		if (m == 0):
			x.append(reallist[i])
	
	assert len(y) == len(x), "Len av ylist and x are not the same"

	ybefore = len(y)

	y = yclean(y,x,lines)

	yafter = len(y)
	ydiff = ybefore-yafter
	print("Slettet "+Style.BRIGHT+str(ydiff)+Style.NORMAL+" linjer fra liste y")

	# Assert the list is correct size
	assert len(y) == len(x), "Len av ylist and x are not the same"

	# Etter vi har fått y til å bli float, så finner vi nå max
	
	y = maxy(y)
	print("Exit, etter maxy")
	exit()
	
	
	
	# Renske x

	xbefore = len(x)
	
	# x er rådata
	# xlist er timestruct
	# xlist2 er datetime
	# def xlean lager xlist
	
	# print("Problemet er y")
	# print("len av y før: "+str(len(y)))
	# print("len av x før: "+str(len(x)))
	# print("len av xlistfør: 0")
	
	x,xlist = xclean(x,y)
	
	# print("len av y etter: "+str(len(y)))
	# print("len av x etter: "+str(len(x)))
	# print("len av xlist etter: "+str(len(xlist)))
	
	print("Returned to me from clean: x and xlist: "+str(len(x))+" "+str(len(xlist)))
	print("Whereas y is: "+str(len(y)))
	
	xafter = len(x)
	xdiff = xbefore-xafter
	print("Slettet "+Style.BRIGHT+str(xdiff)+Style.NORMAL+" linjer fra liste x")
	
	# Merk at xclean lagde liste xlist
	print("Xlist is now: "+str(len(xlist)))
	
	# assert (len(y) == len(xlist)),"y er ulik xlist?"
	
	while (len(y) > len(xlist)):
		del y[0]
		print("Popped item from y list")
	
	# Lage loop som konverterer. Riktig format er: %Y-%m-%dT%H:%M:%S.%f

	print("X list should be clean and ready to go!")

	# Deretter fra time_struck til datetime
	xlist2 = []
	# d finnes, setter den til None	
	d = None

	for i in range(0, len(xlist)):
		# 09.05.2018: datetime.datetime?
		dt = datetime.datetime.fromtimestamp(mktime(xlist[i]))
		xlist2.append(dt)
		# print("dt: "+str(dt)+" i: "+str(i))

	# Selve plotte-kommandoen
	
	print("y: "+str(len(y)))
	print("x: "+str(len(x)))
	print("xlist: "+str(len(xlist)))
	print("xlist2: "+str(len(xlist2)))

	plt.grid(True)
	plt.plot(xlist2,y,'k.',linewidth=1, markersize=1)

	# Finne en sensible min og max for å vise i matplotlib ETTER plot
	# (Egentlig bare minimum)

	# Problemer både min og max
	ymin = min(y)
	try:
		float(ymin)
	except:
		print("could not convert")
		indeks = y.index(ymin)
		print("Index: "+str(indeks))
		yi = y[indeks]
		print("Innhold: "+yi)
		
		# Pop
		del y[indeks]
		del x[indeks]
			
	print("Ny ymin, ett forsøk")
	ymin = min(y)
	print(ymin)
	
	ymin = float(ymin)
	if (type(ymin)) is not float: print("fortsatt feil, trenger å lage loop"),exit()
	
	# getmax forventer to lister
	ymax = "textstring"
	while (type(ymax) is not float):
		print("Calling getmax")
		ymax = getmax(y,x)
		if (ymax is None): 
			print("Break from loop, got None")
			break
		print("Return from getmax: "+str(ymax))
	
	# Secondary check
	ymax2 = max(y)
	print("Ymax2: "+str(ymax2)+" og type er : "+str(type(ymax2)))
	while ("." not in ymax2):
		print("Type: "+str(type(ymax2)))
		indeks = y.index(ymax2)
		print("desimal ikke funnet, popper ved index "+str(indeks)+" ymax2 var: "+str(ymax2))
		del y[indeks]
		ymax2 = max(y)
		ymax = ymax2

	print("Konverterer max til float er det all good?")
	ymax = float(ymax)
	print("Hjelper ikke å si at det er float her, må hente det fra lista direkte")
	
	if (ymax < 10): 
		print("Jesus Crhist!")
		indeks = y.index(max(y))
		del y[indeks]
		ymax = max(y)
		print("Ny ymax: "+str(ymax))
	
	print("Max av y: "+max(y))
	print("Max (from variable) av y: "+str(ymax))
	
	# Final check for datatype
	while (type(ymax) is not float):
		print("Wrong datatype for ymax")
		indeks = y.index(max(y))
		print(indeks)
		ytemp = y[indeks]
		print(ytemp)
		del y[indeks]
		try:
			ymax = float(max(y))
		except:
			ymax = "jibberish"
			print("Could not set a new ymax as float")
		

	if (type(ymin) is not float):
		print("Wrong datatype for ymin, exit")
		exit()
	
	# After umput for mr. JO
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
