#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.005 07.05.2018: Lagd en argv, "-plot"
v0.004 02.05.2018: Lager ny liste på en ok måte grunnet floats
v0.003 12.04.2018: Fikset ymax
v0.002 20.03.2018: Fikse opp temp.log
'''
'''
https://stackoverflow.com/questions/1614236/in-python-how-do-i-convert-all-of-the-items-in-a-list-to-floats
'''

# OPTIONS

# 13.04.2018: Vi kutter ikke lenger i desimanlene fordi Arduino sender kun en desimal
# 08.05.2018: Vi tillar to desimaler fordi matplotlib takler det

# Fargelegging
from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)


import sys
import time
# 07.05.2018: Datetime behøves for string->timestruct->datime->whatever matplotlib krever
from time import mktime
import datetime

# 07.05.2018: For bruk av x-aksen
import matplotlib.dates as mdates

# 08.05.2018: For "jet" colormap
from matplotlib import cm

argplot = False

if (len(sys.argv) > 1):
	if (sys.argv[1] == "-plot"):
		print(Style.BRIGHT+Fore.YELLOW+"Plot argument found, setting it to True")
		drawplot = True
		argplot = True
		
	else:
		print("Sys.argv 1: "+str(sys.argv[1]))


kuttdesimaler = False

# Set standard showplot
if (argplot == False): drawplot = False

import matplotlib
# print(matplotlib.__version__)
# print(str(matplotlib.__file__))

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

def fikslinje():
	"""Fikse manglende linjeskift i temp.log"""
	
	with open("temp.log") as ff:
		f = ff.read()
		
		s = f.split()
		print("0: "+str(s[0])+" 1: "+str(s[1]))
		# TODO: Kode ikke ferdig.
		# Dette er et ikke-problem, men en bug som kan komme opp senere
		# exit(10)
		pass

fikslinje()

from datetime import datetime
d = datetime.now().isoformat()
e = d.find('T')
# print("e: "+str(e))

f = d[0:e]
print("f: "+str(f))


def extractdate(f):

	year = None
	month = None
	day = None
	print("extractdate start with string: "+str(f))

	# error checks
	
	if not len(f) >= 10:
		print("String ikke lang nok")
		return None
	
	if not f.count('-') == 2:
		print("Feil i string, forventet to bindestreker")
		return None
	
	while (year is None):
		while (month is None):
			while (day is None):
				# print("Finn dagen")
				day = f[8:10]
				# print(day)
			# print("Finn måneden")
			month = f[5:7]
			# print(month)
		# print("Finn året")
		year = f[0:4]
		# print(year)
	return (year,month,day)

dagensdato = extractdate(f)
print("Dagens dato er: "+str(dagensdato))
	
# 19.03.2018 - Finne øverste dato og sjekk om folder finnes

with open('temp.log') as fl:
    first_line = fl.readline().strip()

print("Første llinje: "+str(first_line))

firstdate = extractdate(first_line)

# Ønsker at det skal være tuple
#print("Type: "+str(type(firstdate)))

print("Øverste dato kan være: "+str(firstdate))

# Sjekk for folder

# Allerede importert
# import os

cwd = os.getcwd()
print("Current Working Directory: "+str(cwd))

def checkfolder(firstdate):

	# year folder, month folder, "filename.log"
	yf = cwd+"/"+firstdate[0]
	ym = cwd+"/"+firstdate[0]+"/"+firstdate[1]
	datefile = ym+"/"+str(firstdate[2]+".log")

	print("yf: "+str(yf))
	print("ym: "+str(ym))
	print("datefile: "+str(datefile))

	if not os.path.exists(yf):
		os.makedirs(yf)
		print("FOLDER "+str(yf)+" created!")

	if not os.path.exists(ym):
		os.makedirs(ym)
		print("FOLDER "+str(ym)+" created!")

	if not os.path.isfile(datefile):
		open(datefile,'x')
		print("FILE "+str(datefile)+" created!")
	string = firstdate[0]+"-"+firstdate[1]+"-"+firstdate[2]
	return (datefile,string)

print("Sjekker for dagens dato")

dagensdatofile = checkfolder(dagensdato)[0]
dagensdatostring = checkfolder(dagensdato)[1]

print("Sjekker for øverste dato")

firstdatefile = checkfolder(firstdate)[0]
firstdatestring = checkfolder(firstdate)[1]

print("firstdatefile: "+str(firstdatefile))

# print strings
print("Dagens Dato String: "+str(dagensdatostring))
print("First Date String: "+str(firstdatestring))

# Hvis dagensdato og øverste dato er ulike, så må vi renske filer

if dagensdato != firstdate:
	print(str(dagensdato)+" er ulik fra "+str(firstdate))
	
	print("Vi må flytte VELDIG mange linjer fra temp.log til "+str(firstdatefile))
	
	# Åpner destination først
	dest = open(firstdatefile,'w')
	
	# Åpner backup templog2.log
	log2 = open("temp2.log",'w')
	
	# temp log file
	count = 0
	
	with open("temp.log") as tlf:
		for line in tlf:
			count = count+1
			if firstdatestring in line:
				print("datostring funnet - linje "+str(count))
				dest.write(line)
			else:
				print("Datostring ikke funnet - linje "+str(count))
				log2.write(line)
				
	fs2 = os.path.getsize("temp2.log")
	# if (fs2 == 0): print("FATAL ERROR, 0 bytes!"), exit(666)
	os.rename("temp2.log","temp.log")
	print("Rename succesful?")
	print("Gikk fra "+str(fs)+" bytes til "+str(fs2)+" bytes!")

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
	dt = datetime.fromtimestamp(mktime(xlist[i]))
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
plt.title(dagensdatostring)

# --- Legend eller Annontation ---

plt.text(0,0,"Dagens høyeste temperatur",color='red',fontsize=30)

# Her finner vi ut av vi har 40 ylabels
locs, labs = plt.yticks()
# print("Locs: "+str(locs))
# print(labs)

plt.savefig("temp/urdal/temp.png")

if drawplot is True:
	plt.show()
