#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.004 02.05.2018: Lager ny liste på en ok måte grunnet floats
v0.003 12.04.2018: Fikset ymax
v0.002 20.03.2018: Fikse opp temp.log
'''
'''
https://stackoverflow.com/questions/1614236/in-python-how-do-i-convert-all-of-the-items-in-a-list-to-floats
'''

# OPTIONS

# 13.04.2018: Vi kutter ikke lenger i desimanlene fordi Arduino sender kun en desimal
kuttdesimaler = False
drawplot = True

import matplotlib
print(matplotlib.__version__)
print(str(matplotlib.__file__))

import numpy as np
print(np.version.version)
print(np.__path__)

import os


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
		# TODO: Kode ikke ferdig. Fikser ikke det jeg vil fikse
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

import os
cwd = os.getcwd()
print("cwd: "+str(cwd))

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

# print("exit")
# exit(9)

# Fordi vi heter Raspberry Pi
matplotlib.use('tkagg')

# 02.05.2018: Alltid importere etter tkagg
import matplotlib.pyplot as plt


with open('temp.log',"r") as f:
    lines = f.readlines()
    if (lines == 0): print("Ingen linjer i temp.log, exit"), exit(404)
    
    # Lese kun y, x og dato tar vi senere.
    # x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]

# Sette ax for senere, MaxNLocator er ETTER plot, import as figure
# from matplotlib.pyplot import figure as figure
# from matplotlib.ticker import MaxNLocator as MaxNLocator


# Override X from the start

x = np.linspace(0,24,24,endpoint=False)
print("Len av generert x: "+str(len(x)))
print(x)

# print(y)

# print(len(x))
print("Len av y: "+str(len(y)))

# Finne egen min og max value av y

s = sorted(y)
print("s: "+str(s))
ymin = s[0]

# 12.04.2018: Jeg finner "NED" randomt... Lager loop for å unngå.

loopc = 0

# Settings false value
ymax = ""

while ("." not in ymax):
	print("[Invalid ymax] Ymax er: "+str(ymax)+" og loopc er: "+str(loopc))
	loopc += 1
	ymax = s[len(y)-loopc]
	print("[After] Ymax er: "+str(ymax)+" og loopc er: "+str(loopc))

print("Antall loop for å finne korrekt ymax: "+str(loopc))
print("ymax: "+str(ymax)+" Type: "+str(type(ymax)))

	

print("Loop done. ymax er: "+str(ymax))
maxtype = type(ymax)
print("Type er: "+str(maxtype))

print("Ymax: "+str(ymax))

# tymi = type(ymin)
# tyma = type(ymax)

ymin = float(ymin)
ymax = float(ymax)

print("Type av ymin: "+str(type(ymin)))
print("Type av ymax: "+str(type(ymax)))

print("ymin: "+str(ymin))
print("ymax: "+str(ymax))

ymin2 = math.floor(ymin)
ymax2 = round(ymax)

print("ymin2: "+str(ymin2))
print("ymax2: "+str(ymax2))

# Sjekk om jeg kan sjekke om disse er satt

plt.grid(True)

npa = np.arange(ymin2,ymax2,0.1)
print("Type av npa: "+str(type(npa)))
print("Numpy arange: "+str(npa))

linspace = np.linspace(ymin2,ymax2,num=ymax2-ymin,endpoint=False,retstep=True,dtype=int)
print("Linspace: "+str(linspace))

# linspacelist = linspace.tolist()
# print(linspacelist)

# Se nærmere på denne - skal ikke ha stepping?
# print("Før vi setter inn npa: "+str(npa))
# print("Før vi setter inn linsace: "+str(linspace))

# 30.04.2018: Ikke sette yticks og ikke sette ylabels

# 30.04.2018: Settes dette, så settes det tett
# plt.yticks(npa)
# print("yticks fra npa has been set!")

# 30.04.2018: Settes i hytt og pine
# plt.ylabel(npa)
# print("ylabel has been set!")

# Virker ikke: plt.set_yticklabels(npa)
# Virker heller ikke: plt.yticklabels(npa)

# Lage "ticks" for x

# numpy arrange X axis
npax = np.arange(24)

# Printer 0-23 som forventet
print(str(npax))

# plt.xticks(npax)
# plt.xlabels(npax)

# 30.04.2018: Må sikkert importere noe?
# 30.04.2018> Må draw'e først
# plt.draw()
# plt.plot.Axis.set_major_locator(ticker.MaxNLocator(integer=True))

# ax rett før plot
# Bruke plt for å unnga dobling av grafer
# ax = plt().gca()
# ax = figure().gca()
# print(ax)


# plt.plot(x)

print("Dette plottes av y: "+str(y))
print("Type av y som plottes: "+str(type(y)))

x = len(y)

# Check last item
print("Last item: "+str(y[len(y)-1]))

new_list = []
for i in y: 
	print(i)
	try:
		new_list.append(float(i))
	except:
		print("Exit: Failed convert")
		
print("Type av ny liste: "+str(type(new_list)))
print("Len av ny liste: "+str(len(new_list)))

plt.plot(new_list)
# plt.plot(npa)


plt.ylabel('Temperatur')
plt.title(dagensdatostring)

# Gjør ikke mye forskjell, om noe
# plt.autoscale(enable=True, axis='y')

# Her finner vi ut av vi har 40 ylabels
locs, labs = plt.yticks()
print("Locs: "+str(locs))
print(labs)

# Teste om man kan sette labs til ylabel 27.04.2018
# plt.ylabel(str(locs))

# plt.locator_params(axis='y', nbins=auto)
# plt.locator_params(axis='x', nbins=auto)


# Last best hope
# plt og ikke ax
# Er det denne som lager to plots?
# plt.axes.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.savefig("temp/urdal/temp.png")

if drawplot is True:
	plt.show()
