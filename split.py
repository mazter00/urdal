#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SPLITS temp.log with the previous day, and only that day
Moves that portio from merge.log to its own folder and file

split.py (this) has the responsibillity for date-cehcking
"""

from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)

import os


def version():
	return "v0.001"

# Assume temp.log is todays log, but import/read/merge yesterday

from datetime import datetime

def today():
	d = datetime.now().isoformat()
	e = d.find('T')
	# print("e: "+str(e))

	f = d[0:e]
	print("f: "+str(f))
	return(f)

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

	# Ting er visst ikke globale...
	cwd = os.getcwd()
	
	# year folder, month folder, "filename.log"
	yf = cwd+"/"+firstdate[0]
	ym = cwd+"/"+firstdate[0]+"/"+firstdate[1]
	datefile = ym+"/"+str(firstdate[2]+".log")

	print("yf: "+str(yf))
	print("ym: "+str(ym))
	print("datefile: "+str(datefile))

	exit("Arbitrary exit code")
	
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
	return(datefile,string)

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


from datetime import datetime

# Mine egne funksjoner
def main():
	from plotting import today
	from plotting import extractdate

	print(Style.BRIGHT+"Split "+version()+Style.NORMAL+" starting")

	f = today()
	if f is None: 
		print("F finnes ikke")
		exit()
	dagensdato = extractdate(f)
	print("Dagens dato er: "+str(dagensdato))

if __name__ == "__main__":
    # execute only if run as a script
    main()
