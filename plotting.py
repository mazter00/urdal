#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
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

# OPTIONS

# 13.04.2018: Vi kutter ikke lenger i desimanlene fordi Arduino sender kun en desimal
# 08.05.2018: Vi tillar to desimaler fordi matplotlib takler det

# Fargelegging

def fikslinje():
	"""Fikse manglende linjeskift i temp.log"""
	
	with open("temp.log") as ff:
		f = ff.read()
		
		s = f.split()
		print("0: "+str(s[0])+" 1: "+str(s[1]))
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
	



def main():
	# Alt som er i main kjøres, IKKE ved import
	from colorama import init
	init()
	from colorama import Fore, Back, Style
	init(autoreset=True)


	import sys
	import time
	# 07.05.2018: Datetime behøves for string->timestruct->datime
	from time import mktime
	import datetime

	# 07.05.2018: For bruk av x-aksen
	import matplotlib.dates as mdates

	# 08.05.2018: For "jet" colormap
	# 09.05.2018: Får ikke til colormap, prøver igjen senere
	# from matplotlib import cm

	argplot = False

	if (len(sys.argv) > 1):
		if (sys.argv[1] == "-plot"):
			print(Style.BRIGHT+Fore.YELLOW+"Plot argument found, setting it to True")
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
	print("Bytes: "+str(fs))
	if (fs == 0): print("0 bytes, exit"), exit(405)

	import math

	fsL = math.floor(fs/33)
	print("Beregnet Antatt Antall Linjer: "+str(fsL))
	# exit(2)

	fikslinje()


	from merge import today,extractdate,checkfolder

	
	if kuttdesimaler is True:
		removedecimal()
	else:
		print("Beholder desimalene")

	# Fordi vi heter Raspberry Pi
	matplotlib.use('tkagg')

	# 02.05.2018: Alltid importere etter tkagg
	import matplotlib.pyplot as plt

	# --- KODE FOR PLOTTINGz --- 

	with open('temp.log',"r") as f:
		lines = f.readlines()
		if (lines == 0): print("Ingen linjer i temp.log, exit"), exit("404")
		
		# 07.05.2018: Leser nå både x og y
		x = [line.split()[0] for line in lines]
		y = [line.split()[1] for line in lines]

	print("Len av y: "+str(len(y))+" og len av x: "+str(len(x)))

	# Finne egen min og max value av y

	s = sorted(y)
	# print("s: "+str(s))
	ymin = s[0]

	# 12.04.2018: Jeg finner "NED" randomt... Lager loop for å unngå.
	# 07.05.2018: Dette er en feil ifra kildefilen. Kanskje lage en sjekk i sread.py? [TODO]
	# 08.05.2018: Vet du hva, vi looper hele lista vi...

	count = 0
	pop = False
	ybefore = len(y)

	for i in y:
		try:
			i2 = float(i)
		except:
			print(Fore.RED+Style.BRIGHT+"Error in the shoe!")
			print("i: "+(str(i)))
			print("Delete item no. "+str(count))
			pop = True
		if pop is True: 
			del y[count]
			print("POPPED item "+str(count)+" in list Y!")
			
			del x[count]
			print("POPPED item "+str(count)+" in list X!")
			count = count-1
			pop = False

		count = count+1

	yafter = len(y)
	ydifference = ybefore-yafter

	print(Fore.GREEN+Style.BRIGHT+"All good with the ylist")
	print("Number of items from y deleted (if any): "+str(ydifference))

	# Assert the list is correct size
	assert len(y) == len(x), "Len av ylist and x is not the same"

	# Bedring av Plot
	# Grid-lines

	plt.grid(True)


	new_list = []
	for i in y: 
		# print(i)
		try:
			new_list.append(float(i))
		except:
			print("Exit: Failed convert to float")
			print("i er: "+str(i))
			print("y er: "+str(y[i]))
			
	print("Type av ny liste: "+str(type(new_list)))
	print("Len av ny liste: "+str(len(new_list)))

	# --- Lage x-akse ---

	# Lage loop som konverterer. Riktig format er: %Y-%m-%dT%H:%M:%S.%f

	print("Before x loop, len: "+str(len(x)))
	print("Type av x before loop: "+str(type(x)))

	i = None
	xlist = []

	# Fra string til time_struct

	for i in range(0, len(x)):
		xlist.append(time.strptime(x[i],"%Y-%m-%dT%H:%M:%S.%f"))
		# print("type: "+str(type(var)))
		
	print(xlist[0])
	print(type(xlist[0]))

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

	plt.plot(xlist2,new_list,'k.',linewidth=1, markersize=1)
	# plt.plot(npa)

	# Konfig ETTER plot

	# Finne en sensible min og max for å vise i matplotlib ETTER plot

	ymax = float(max(y))
	ymin = float(min(y))

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
