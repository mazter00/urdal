#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pga teite Python 2
from __future__ import print_function

'''
v0.016 25.06.2018 15:27 Removed function removedecimal. No longer needed, matplotlib will take care of it.
v0.015 25.06.2018 Added -intervall [num] as an option. Will default to 1500 if not set.
v0.014 19.06.2018 Creates folder where pictues will be stored for ftp-uoload
v0.013 22.05.2018 Now generates graphs at requested range in hours without hickup
V0.012 15.05.2018 Error output (verifylines) looks good, even calculates correct lines removed and shows correct error
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
* lots
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
.. og plotter alt sammen etter bestemt tids-range i timer
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

def verifylines(lines):
	""" Verfies by typecasting x and then y at the line before putting in into new list """
	import math
	
	import time
	tsstart = time.monotonic()
	
	lenx = len(lines)
	# Len X minus 1
	lenxm1 = lenx-1
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
	

	for i in range(0, lenxm1):
		
		# print statement
		p = False
		
		# print("For loop start")
		line2 = lines[i].split()
		
		
		# print(line2)
		# print(line2[0])
		# print(line2[1])
		
		# Check for contect (22.06.2018)
		try:
			ll2 = len(line2[0])
		except:
			print("Empty line 2, 0 @ counter "+str(i))
			p = False
			continue
		
		# Check for third element first
		
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
			
			# 22.06.2018: Feil her?
			
			# if (line2[0] is None): print("Massiv feil, 0 av line2 finnes ikke"), continue
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
			# 20.06.2018: 9 gives loads of error, 9.9 could be better?
			# Viktig å sette en ok grense her
			if (fabs >= 9): 
				errors = errors+1
				strline = "Diff: "+str(fabs)+" C: "+str(floaty)+" BA: "+str(floatyba)
				print("["+str(errors)+"] "+"Float distance too high at "+str(i)+Style.BRIGHT+Fore.YELLOW+": "+Style.RESET_ALL+str(strline))
				
				# 20.06.2018: Selv om distansen var mye, ta backup.
				floatyba = floaty
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

# finddiff(xlist2,y,xlist3,y3,anker,intervall)
def finddiff(xlist2,y,xlist3,y3,anker,intervall):
	# The list to work with
	# Starting position
	# Number of seconds
	
	loopc = 0
	diff = 0
	snitt = []
	xlist3 = xlist3
	y3 = y3
	intervall = intervall
	print("Intervall received: "+str(intervall))
	# exit()
	
	# Finne anker-punktet
	
	startpunkt = xlist2[anker]
	
	while (diff < intervall):
		loopc = loopc+1
		
		value = y[anker+loopc]
		# print("Value found: "+str(value))
		
		# Current tidspunkt
		cpunkt = xlist2[anker+loopc]
		
		d = cpunkt-startpunkt
		# print("Loopc: "+str(loopc)+" Diff: "+str(d))
		
		diff = d.total_seconds()
		
		snitt.append(value)
	
	lengde = len(snitt)
	
	assert lengde>0,"0 i lengde?"
	
	snitttemp = sum(snitt) / len(snitt)
	print(Style.BRIGHT+"Gjennomsnittstemperaturen var: "+str(snitttemp)+" av "+str(lengde)+" målinger")
	
	# Legge ting ny liste
	
	if (snitttemp > 0):
		xlist3.append(startpunkt)
		y3.append(snitttemp)
	else:
		print(Style.BRIGHT+Fore.RED+Back.BLACK+"Error! Negative value found, disregarding it")
		print("Startpunk?: "+str(startpunkt))
		# exit()
	
	assert (len(xlist3) == len(y3)),"Xlist3 og y3 er ikke av lik lengde"
	

	# Return in this format
	return(loopc,xlist3,y3,snitttemp)

def shortenlines(reallist):
	x = len(reallist)
	print("Shorten recieved: ")
	print("Length: "+str(x))
	
	for i in range(0,10):
		print("i: "+str(i)+" "+str(reallist[i]))
	
	
	# Return False until code is complete
	return(False)
			
def binarys(lines,t,wtdiff,wtdiffs):
	""" Binary Search """
	
	print(Style.BRIGHT+"[BinarySearch] "+Style.NORMAL+"starting...")
	from datetime import date,datetime
	lista = lines
	
	print("Latest timestamp: "+str(t))
	print("Wanted difference in hours: "+str(wtdiff))
	print("Wanted difference in seconds: "+str(wtdiffs))

	x = len(lista)
	print("Number of lines: "+str(x))
	
	# Først sjekke om første linja (eldste) i temp.log dekker søket
	# Det er for å svare på spørsmålet om man må merge datofiler...
	
	# False = Dekker ikke, må merge --- True, Dekker behovet, behøver ikke å merge
	mergeb = False
	i = 1
	print("Binary search line is (oldest): "+str(i))
	linje = lista[i]
	linje = linje.split()[0]

	try:
		t2 = datetime.strptime(linje,"%Y-%m-%dT%H:%M:%S.%f")
	except:
		print("Error in the line (oldest): "+str(linje))
		exit("bys failed, corrupt line, oldest")

	diff = t-t2
	h = float(diff.total_seconds())
	print(h)
	
	print("h: "+str(h)+" wtdiff: "+str(wtdiffs))
	
	if (h >= wtdiffs):
		print(Fore.GREEN+Style.BRIGHT+"No need to merge, we have all we need")
		mergeb = False
	else:
		mergeb = True

	if (mergeb is True):
		print("We need to merge files to fulfill the range-reqeust. Aborting due to incomplete code")
		return(False,mergeb)
		exit("Need to merge, incomplete code")

	# Alt ok så langt. Enten har temp.log rangen inne, eller så har vi merget filer. TODO: Merge filer ved behov

	# First try
	firstb = False
	
	# Start of loop?
	
	tries = 0
	oldh = h
	print("oldh (maximum diff): "+str(oldh))
	
	# Setter i her før loopen. Loopen har ansvar for nye i'er
	i = int(x/2)
	minL = 0
	maxL = x
		
	for something in range(x):
		tries = tries+1

		print("Try: "+Style.BRIGHT+str(tries)+Style.NORMAL+": Binary search line is: "+str(i)+"/"+str(x))
		linje = lista[i]
		linje = linje.split()[0]

		try:
			t2 = datetime.strptime(linje,"%Y-%m-%dT%H:%M:%S.%f")
		except:
			print("Error in the line: "+str(linje))
			# "bys"?
			exit("bys failed, corrupt line")

		diff = t-t2
		h = float(diff.total_seconds())
		# print(h)
		
		# Linediff
		ld = maxL-minL
		
		print("h: "+str(h)+" wtdiff: "+str(wtdiffs)+" Min: "+str(minL)+" Max: "+str(maxL)+" Linediff: "+str(ld))
		
		if (h > wtdiffs):
			print("Diff too high, need higher linenumber")

			print("Current i: "+str(i))
			if (minL < i): 
				minL = i
			else:
				print("Error in setting new minimum line, HOWEVER, I think we got it")
				return True,i
				
			i = int((minL+maxL)/2)
			print("New i: "+str(i))
		elif (h < wtdiffs):
			print("Diff too low, need lower linenumber")

			print("Current i: "+str(i))
			maxL = i
			i = int((minL+maxL)/2)
			print("New i: "+str(i))
		else:
			print("Diff is the same?!?")
			exit()
	
	exit("Fallen off loop?")

def list2xy(reallist):
	
	from time import mktime
	from datetime import datetime
	
	# Quickly seperate the list into x and y
	x = []
	y = []
	
	# print("Seperating list")
	
	# reallist er den vaska lista
	
	# reallist = list
	
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

	# print("x and y created")
	# print(len(y))
	# print(len(x))
	
	# Assert the list is correct size
	assert len(y) == len(x), "Len av ylist and x are not the same"
	
		# Deretter fra time_struct til datetime
	xlist2 = []
	
	# String Date Time Backup
	sdtba = None
	
	nydag = []

	for i in range(0, len(x)):
		# 09.05.2018: datetime.datetime?
		# 22.05.2018: *sukk* date?
		
		#print(x[i])
		
		dt = datetime.fromtimestamp(mktime(x[i]))
		
		# String, date time
		sdt = str(dt)
		sdt = sdt.split(' ')[0]
		# print(sdt)
		
		if sdtba is None:
			sdtba = sdt
			nydag.append([sdt,i])
		
		if (sdt != sdtba):
			sdtba = sdt
			nydag.append([sdt,i])
				
		xlist2.append(dt)
		# print("dt: "+str(dt)+" i: "+str(i))

	
	return(x,y,xlist2,nydag)

def firstd(logfile):
	with open(logfile,"r") as f:
		lines = f.readlines()
		
	# Get newest date (disregard "now", we are using the file)

	# Code for splitting temp.log into individual files
	
	first = lines[0]
	first = first.split()[0]
	
	# Should be something like "2018-05-10T00:00:00.561624"
	
	print(first)
	print(len(first))
	
	if len(first) != 26:
		# Noise in first line of temp.log, let's remove it and re-write temp.log
		print(Style.BRIGHT+Fore.RED+"[Error] Noise found in line 1 "+Fore.WHITE+str(first))
		
		with open("temp.log","w") as fixfile:
			fixedlines = lines[1:]
			fixedstr = ''.join(fixedlines)
			fixfile.write(fixedstr)
			# exit("sjekk temp.log")
			
			# TODO 24.05.2018: Flytte validering av linje en til egen funksjon, 
			# men nå bare tar vi og lager nye variabler, spesifikt "first"
			# 24.05.2018 15:18: Egen funksjon, yo
			first = fixedlines[0]
			first = first.split()[0]
			
	
	firstd = first.split('T')[0]
	print("firstd "+str(firstd))
	return(firstd)

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
		os.system("sudo pip3 install --upgrade matplotlib -v")
		# os.system("pip3 install matplotlib")

	from matplotlib.dates import MonthLocator, HourLocator, DateFormatter
	
	# 08.05.2018: For "jet" colormap
	# 09.05.2018: Får ikke til colormap, prøver igjen senere
	# from matplotlib import cm

	# Standard variabler
	argplot = False

	wtdiff = int(0)
	wtdiffs = int(0)
	
	firstdato = ""
	
	intervall = 0
	
	logfile = ""

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
			wtdiff = int(ali1txt)
		if ("-intervall" in al):
			print("-intervall found in al, checking for argument")

			ali = al.index("-intervall")
			ali1 = ali+1
			intervall = int(al[ali1])
			
			print("ali: "+str(ali))
			print("ali txt: "+str(intervall))
			print("Assume this is in seconds")
			print("Type: "+str(type(intervall)))
		if ("-log" in al):
			print("-log found in al, checking for argument")

			ali = al.index("-log")
			ali1 = ali+1
			logfile = al[ali1]
			
			print("ali: "+str(ali))
			print("ali txt: "+str(logfile))
			print("Assume this is the wanted logfile")
		else:
			print("End of argv")
			# Kanskje for "-ftp" ved senere anledning?
			print("Sys.argv 1: "+str(sys.argv[1]))

	import matplotlib
	# print(matplotlib.__version__)
	# print(str(matplotlib.__file__))
	
	from matplotlib.ticker import MaxNLocator
	# Kilde: https://stackoverflow.com/questions/34678130/matplotlib-how-can-i-use-maxnlocator-and-specify-a-number-which-has-to-be-in-a

	# 09.05.2018: Tror ikke vi bruker numpy? Sjekk for dette, TODO
	import numpy as np
	# Bruker jeg numpy til noe som helst nå? 07.05.2018
	# print(np.version.version)
	# print(np.__path__)

	import os

	# Filen som skrives til heter alltid temp.log
	# Fra og med 25.06.2018 så er ikke dette lenger sant. AM2302 har også sin egen log-file

	# Set standard showplot
	if (argplot == False): drawplot = False

	# Sjekker options
	
	if (wtdiff == 0):
		print("Wanted time difference not set; setting it to 24 hours")
		wtdiff = 24
		
	if (intervall == 0):
		print("Wanted intervall is not set, setting it to 1500 seconds")
		intervall = 1200

	if (logfile == ""):
		print("Logfile was empty, using default temp.log")
		logfile = "temp.log"

	fs = os.path.getsize(logfile)
	print(Style.BRIGHT+"Bytes: "+Style.NORMAL+str(fs))
	if (fs == 0): print("0 bytes, exit"), exit(405)

	# fikslinje()

	# Fordi vi heter Raspberry Pi
	matplotlib.use('tkagg')

	# 02.05.2018: Alltid importere etter tkagg
	import matplotlib.pyplot as plt
	import matplotlib.ticker as ticker

	# --- Kode for merging ---
	
	# Jeg vet at jeg også importerer det samme i binarys
	# Her i main så importerer vi datetime "direkt"
	from datetime import datetime,timedelta
	
	# Wanted time difference in seconds
	wtdiffs = int(float(wtdiff)*60*60)
	print("Wanted time difference in seconds is: "+str(wtdiffs))
	# print(str(type(wtdiffs)))

	# TODO: Unødvendig å åpne denne mange ganger (dette er første gang)
	# 24.05.2018: lines er ganske universell nedover (tror jeg)
	with open(logfile,"r") as f:
		lines = f.readlines()
		
	# Get newest date (disregard "now", we are using the file)

	# Code for splitting temp.log into individual files
	
	firstdato = firstd(logfile)
	print("firstdato "+str(firstdato))
		
	# Prepare t for binarys (se, her bruker vi lines)
	linje = lines[-1]
	linje = linje.split()[0]
	t = datetime.strptime(linje,"%Y-%m-%dT%H:%M:%S.%f")
	lastd = linje.split('T')[0]
	
	# Egne funksjoner, 25.05.2018: Trenger kanskje kun splittemp?
	# from split import today,extractdate,checkfolder,splittemp
	from split import checkfolder,splittemp
	from merge import merge
	
	# print("firstd vs lastd: "+str(firstd)+" "+str(lastd))
	while (firstdato != lastd):
		# Split Temp Boolean
		print(Fore.CYAN+"temp.log contains different dates, split "+Style.BRIGHT+str(firstdato)+Style.NORMAL+" from the log")
		
		# First Date List
		fdl = firstdato.split('-')
		print("fdl: "+Style.BRIGHT+str(fdl),end=" ")
		
		# Last Date List
		ldl = lastd.split('-')
		print("ldl: "+Style.BRIGHT+str(ldl))
		
		stb = splittemp(fdl,ldl)
		if stb != True: exit("Split Temp failed...?")
		
		# Make new firstd so this while loop can work
		firstdato = firstd(logfile)
		print("While loop, firstdato: "+str(firstdato))
	else:
		print(Fore.GREEN+Style.BRIGHT+"temp.log inneholder kun dagens dato :)")
		
	# exit("Arbitrary exit loop after cleaning all dates except today")

	# Remember, verifylines comes *after* this, noise could be a problem.
	# However, we are only working against date [x], and not the pair of date and value.
	
	# Beregne hvor mange og hvilke log-filer vi må merge...
	
	# t er fra siste linje i temp.log
	print("t: "+str(t))
	
	# Total seconds in a day
	tsd = 24*60*60
	# print(tsd)
	
	# List of days to merge
	ldm = []
	
	# Backup
	wtdiffs2 = wtdiffs
	# Check for above 24 hours
	while (wtdiffs2 >= tsd):
		# Time Merge, t-Wanted_io_sekunder
		tm = t-timedelta(seconds=wtdiffs2)
		wtdiffs2 = wtdiffs2-tsd
		
		# Time, Merge, to String
		tms = str(tm)
		# print(tms)
		
		tms = tms.split(' ')[0]
		# print(tms)
		
		tms = tms.split('-')
		# print(tms)
		ldm.append(tms)
		
	# Then add last day, if needed
	
	print("Adding last day")
	tm = t-timedelta(seconds=wtdiffs2)
	
	tms = str(tm)
	print(tms)
	
	tms = tms.split(' ')[0]
	print(tms)
	
	tms = tms.split('-')
	print(tms)
	print("Before we append...")
	# exit("Sjekk tm")
	
	ldm.append(tms)


	
	
	
	print("Her har vi en range? (sjekk også for last-to-current-day)")
	print(ldm)
	
	print("Len of ldm (if > 0, then merge was needed?): "+str(len(ldm)))
	
	ldm2 = []
	
	for i in ldm: 
		print(i)
		ldm2.append(checkfolder(i)[0])
			
	print("ldm2: "+str(ldm2))
	
	m = merge(ldm2)
	if (m is False): print("Merge is false, cannot continue..."), exit()
	
	print("Len of ldm2 (if > 0, then merge was needed?): "+str(len(ldm2)))
	if (len(ldm2) > 0):
		with open("merged.log",'r') as f:
			lines = f.readlines()
		print(Style.BRIGHT+Fore.CYAN+"Using merged.log instead of temp.log")
	
	
	# "lines" kommer fra temp.log
	
	# Binary Search Boolean, Binary Search Line Number Returned
	bsb,bsl = binarys(lines,t,wtdiff,wtdiffs)
	if bsb is False:
		# Her finner vi ut at vi må merge
		print("BSL: "+str(bsl))
		# merger = 
		exit("[Main] Binary Search failed")
	else:
		print("Binary Search Succeded, Line Number Returned: "+str(bsl))
		
	# Loop for å lage liste out av en selected range fra temp.log ([lines])
	print("Lines exists, len: "+str(len(lines)))
	
	lines = lines[bsl:]
	print("New Lines, len: "+str(len(lines)))
	

	# --- KODE FOR PLOTTINGz --- 
	
	linjer = len(lines)
	if (linjer == 0): 
		print("Ingen linjer i temp.log, exit! Linjer er: "+str(linjer))
		exit()
	else:
		print("Linjer funnet: "+Style.BRIGHT+str(linjer))
	
	# Verifiserer lista kun på linjer fra temp.log, antar at resten er riktig (TODO: Flytte denne kodelinja litt opp)
	reallist = verifylines(lines)
	
	# Denne splitter reallist til henholdvis x og y
	x,y,xlist2,nydag = list2xy(reallist)
	
	# Våre nye lister, skal erstatte xlist2 og y
	xlist3 = []
	y3 = []
	
	# Anker Hansen
	anker = 0
	loopc = 0

	# Def: Ut ifra liste x og y, legg på liste x3 og y3, søk fra pos anker, med sekund intervall
	# vennligst returner loop counter, current liste for xlist3 og y3, snittet som ble funnet
	# originale xlist2 og y beholdes fra min side (ønskes ikke returnert)
	
	# Ikke sette egen: intervall = 1200

	a2 = 0
	
	while (a2 < len(xlist2)):
		# print("a2 av len: "+str(a2)+" "+str(len(xlist2)))
		loopc,xlist3,y3,snitt = finddiff(xlist2,y,xlist3,y3,anker,intervall)

		assert (loopc > 0),"No loop executed?"
		assert (snitt != 0),"No average found?"

		# print(Style.BRIGHT+"Snittet denne gang ble: "+str(snitt))
		
		anker = anker+loopc
		l2 = loopc*2
		a2 = anker+l2
		
		# print("Oppdatert a2: "+str(a2))


	print(Style.BRIGHT+str(snitt))
	print("Sjekk for stats")
	
	# print(y3)
	
	print("Len av xlist3: "+str(len(xlist3)))
	print("Len av y3: "+str(len(y3)))
	
	# exit("sjekk x og y")
	
	xlist2 = xlist3
	y = y3
	
	# exit("sjekk x og y")

	# shortenlist vil finne gjennomsnitt av X sekunder
	# reallist = shortenlines(reallist)
	# if (reallist is False): exit("Missing code from shortenlines")
	
	
	
	# Etter vi har fått y til å bli float, så finner vi nå max
	
	ymax = max(y)
	assert isinstance(ymax, float), "Max of y is not a float?"
	
	ymin = min(y)
	assert isinstance(ymin, float), "Min of y is not a float?"


		
	# Selve plotte-kommandoen

	print(nydag)
	# exit("Sjekk nydag")


	print("matplotlib is now plotting, please wait...")

	plt.grid(True)
	# plt.plot(xlist2,y,'k.',linewidth=1, markersize=1)
	# plt.plot(xlist2,y,'darkblue', marker='point', linewidth=1, markersize=1)
	# plt.plot(xlist2,y,'darkblue', linewidth=1, markersize=1)
	# OK plt.plot(xlist2,y,'darkblue', marker='.', markersize=2, linestyle='None')
	plt.plot(xlist2,y,'darkblue', marker='|', linewidth=3)
	# plt.plot(xlist2,y,'#01386a.',linewidth=1, markersize=1)
	
	

	# Finne en sensible min og max for å vise i matplotlib ETTER plot
	# (Egentlig bare minimum)

	
	# After input for mr. Jan O
	if (ymin > 20): 
		print("Setting own limit on y-axis, minimum, to 20")
		plt.gca().set_ylim(bottom=20)
		
	# if (ymin < 20): 
	# print("Setting own limit on y-axis, maximum, to 20")
	#	plt.gca().set_ylim(top=20)

	# plt.axvspan()
	
	# For x-aksen til å vise time:minutt
	# Kilde: https://matplotlib.org/gallery/text_labels_and_annotations/date.html
	# Manuell Day Intervall for hver 100. time + 200% -> 150%
	ivald = int((wtdiff/100)*1.25
	)
	if ivald == 0: ivald = 1
	print(Style.BRIGHT+"Custom day intervall: "+str(ivald))
	days  = mdates.DayLocator(interval=ivald)
	# hours = mdates.HourLocator(byhour=range(2,21,6))
	
	# Manuell Hour Intervall + 250% -> 200%
	# 300 timer er for høy for 72 timer
	ival = int((wtdiff/17)*2.46)
	print(Style.BRIGHT+"Custom hour intervall: "+str(ival))
	
	mh = 1
	xh = 22
	if (wtdiff >= 48): 
		print("Setting new range for hour to show - 48")
		mh = 1
		xh = 20
	if (wtdiff >= 72): 
		print("Setting new range for hour to show - 72")
		mh = 3
		xh = 19
	if (wtdiff >= 100): 
		print("Setting new range for hour to show - 100")
		mh = 3
		xh = 17
	if (wtdiff >= 150): 
		print("Setting new range for hour to show - 150")
		mh = 4
		xh = 17
		
	hours = mdates.HourLocator(byhour=range(mh,xh), interval=ival)
	if (wtdiff >= 150): 
		hours = hours = mdates.HourLocator(byhour=range(mh,xh), interval=ival)
	
	myFmtD = mdates.DateFormatter('%d.%m.%Y')
	myFmtH = mdates.DateFormatter('%H:%M')
	
	# plt.gca().xaxis.set_major_formatter(myFmt)
	
	plt.gca().xaxis.set_major_formatter(myFmtD)
	plt.gca().xaxis.set_minor_formatter(myFmtH)
	
	# 30.05.2018, det er en *locator*
	plt.gca().xaxis.set_major_locator(days)
	
	plt.gca().xaxis.set_minor_locator(hours)
	# plt.gca().xaxis.set_minor_locator(ticker.AutoMinorLocator())
	
	if (wtdiff >= 150):
		# plt.gca().xaxis.set_minor_locator(ticker.NullLocator())
		plt.gca().xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
	
	# fig, ax = plt.subplots()
	# plt.gca().xaxis.autoscale_view()
	
	# 28.06.2018: Virker fortsatt ikke... Det virker?!
	# 29.06.2018: gcf = figure, gza = axis

	plt.MaxNLocator(5)

	plt.ylabel('Temperatur i Nidelva')

	# 22.05.2018: Men nå kan jeg ikke "datetime.datetime." ?
	dato = datetime.now().strftime('%d.%m.%y')
	print("Dato: "+str(dato))
	
	ttxt = "Siste "
	ttxt = ttxt+str(wtdiff)+" timer"
	plt.title(dato+" ("+str(ttxt)+")")

	# --- Legend eller Annontation ---

	plt.text(0,0,"Dagens høyeste temperatur",color='red',fontsize=30)
	
	# Brukes på figure!
	plt.gcf().autofmt_xdate()
	
	# Sjekke og gjennomgå x-labels for erstatting av 00:00 til dato.
	# 09.05.2018: Useful for senere, sjekke midnatt, rekord, minimum
	locs, labs = plt.xticks()
	print("Locs: "+str(locs))
	print(labs)
	
	# mdates er importert
	print("len of labs: "+str(labs))
	
	ymin,ymax = plt.ylim()
	print("ymin: "+str(ymin))
	print("ymax: "+str(ymax))
	
	# Sjekke om folderen finnes
	
	if (os.path.exists("temp")) is False:
		os.makedirs("temp")
		print("Folder temp created")
		
	if (os.path.exists("temp/urdal")) is False:
		os.makedirs("temp/urdal")
		print("Folder temp/urdal created")
	
	
	# TODO: Navngi hvis en automatisert request ble mottatt
	
	if (wtdiff != 24): 
		print("Custom wtdiff: "+str(wtdiff))
		plt.savefig("temp/urdal/temp"+str(wtdiff)+".png")
		uploadfile = "temp/urdal/temp"+str(wtdiff)+".png"
	else:
		# Assume standard 24h graph
		plt.savefig("temp/urdal/temp.png")
		uploadfile = "temp/urdal/temp.png"
	
	print("Uploading custom png-file to the FTP-server now")
	print(Style.BRIGHT+"Exact filename: "+str(uploadfile))
	cmd = "python3 ftp.py -upload "+str(uploadfile)
	os.system(cmd)
	print("Done uploading custome file")

	if drawplot is True:
		print(Fore.YELLOW+Style.BRIGHT+"Viser plot")
		plt.show()
	
if __name__ == "__main__":
    # execute only if run as a script
    
    pyv = sys.version_info[0]
    # print("Vi kjører Python version: "+str(pyv))
    
    assert pyv > int(2),"Krever Python 3, Python 2 er for dårlig"

    main()
