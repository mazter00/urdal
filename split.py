#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.002 24.05.2018 Now sucessfully splits a certain string in temp.log to its own file. Also removes noise!
v0.001 Inital code, copied from merge.py
'''

"""
SPLITS temp.log with the previous day, and only that day
Moves that portio from merge.log to its own folder and file

split.py (this) has the responsibillity for date-cehcking
"""
"""
def checkfolder CREATES files
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
	""" 24.05.2018: Tror ikke jeg bruker denne """
	
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

def splittings(datefile,fds):
	print("[Splittings] starts...")
	print("[Splittings] Will split "+str(fds)+" in temp.log and put it into its own file")
	
	# Åpner destination først
	dest = open(datefile,'w')
	
	# Åpner backup templog2.log
	log2 = open("temp2.log",'w')
	
	# temp log file
	count = 0
	antall = 0
	
	fs = os.path.getsize("temp.log")
	if (fs == 0): print("FATAL ERROR, 0 bytes!"), exit(666)


	with open("temp.log") as telle:
		for line in telle:
			if fds in line:
				antall += 1
				
	print("Splittings] We have "+str(antall)+" occurances of the requested date")
		
	with open("temp.log") as tlf:
		for line in tlf:
			count = count+1
			if fds in line:
				# print("datostring funnet - linje "+str(count))
				dest.write(line)
			else:
				if (count < antall): print("Datostring ikke funnet - linje "+str(count))
				if (len(line) > 30): log2.write(line)
				else: 
					print(Style.BRIGHT+Fore.RED+"Error, line not long enough! "+str(line).rstrip())
					# exit("sjekk line length")
				
	fs2 = os.path.getsize("temp2.log")
	if (fs2 == 0): print("FATAL ERROR, 0 bytes!"), exit(666)
	os.rename("temp2.log","temp.log")
	print("Rename succesful?")
	print("Gikk fra "+str(fs)+" bytes til "+str(fs2)+" bytes!")
	return(True)


# No longer needs dagensdato in arguments, just firstdate
def checkfolder(firstdate):
	# print("[CheckFolder]: "+str(firstdate)+" "+str(dagensdato))

	# Ting er visst ikke globale...
	cwd = os.getcwd()
	
	# year folder, month folder, "filename.log"
	yf = cwd+"/"+firstdate[0]
	ym = cwd+"/"+firstdate[0]+"/"+firstdate[1]
	datefile = ym+"/"+str(firstdate[2]+".log")

	print(Style.BRIGHT+"yf: "+Style.NORMAL+str(yf))
	print(Style.BRIGHT+"ym: "+Style.NORMAL+str(ym))
	print(Style.BRIGHT+"datefile: "+Style.NORMAL+str(datefile))

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
	
	fs = os.path.getsize(datefile)
	print("Datefile "+Style.BRIGHT+Fore.GREEN+"exists: "+Fore.WHITE+str(datefile)+" Size: "+str(fs))
	
	# 24.05.2018: Aner ikke hvorfor det er return her
	# return(datefile,string)

	# 24.05.2018: Som de er, siden funksjonen er ble kalt
	return(datefile,True)
	

# Sometimes, it is more fun to write things twice

def splittemp(firstd,lastd):
	# print("Type recieved: "+str(type(firstd)))
	assert(type(firstd) is list),"splittemp did not recieve type list (but maybe string)"
	
	datefile,b = checkfolder(firstd,lastd)
	# First Date String
	fds = '-'.join(firstd)
	print(firstd,fds,datefile,b)
	
	result = splittings(datefile,fds)
	print(result)
	
	return(result)

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
