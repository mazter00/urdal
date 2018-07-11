#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.004 06.07.2018 15:30 Function splittings now works with AM-sensor
v0.003 06.07.2018 checkfolder now asks for sensor
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

# fds = First Date String
def splittings(datefile,fds,logfile):
	import time
	print("[Splittings] Will split "+str(fds)+" in "+str(logfile)+" and put it into "+str(datefile))
	
	cwd = os.getcwd()
	print("Current Working Directory: "+str(cwd))
	
	# Sane checks
	
	fs = os.path.getsize(logfile)
	if (fs == 0):
		print("FATAL ERROR, 0 bytes in logfile!")
		exit(666)
	else:
		print("Current size of logfile is: "+str(fs))

	# Det er ok om filen (datefile) finnes, men ikke hvis det er innhold
	# Vil alltid finnes pga checkfolder()

	fsd = os.path.getsize(datefile)
	if (fsd > 0): 
		print("FATAL ERROR, >0 bytes in datefile! "+str(fsd)+" bytes")
		time.sleep(5)
		return(False)
	
	# Åpner original logfile som read
	lf = open(logfile,'r')
	
	# Åpner destination som write
	dest = open(datefile,'w')
	destname = datefile
	
	# Åpner backup templog2.log som write
	log2 = open("filtered.log",'w')
	log2name = "/home/pi/pyscript/filtered.log"
	
	# temp log file
	count = 0
	antall = 0
	
	# Statistikk
	with open(logfile) as telle:
		for line in telle:
			if fds in line:
				antall += 1

	print("[Splittings] We have "+str(antall)+" occurances of the requested date")
	
	if (antall == 0):
		print("Fant ikke det jeg skulle, return False")
		return(False)
	
	with open(logfile) as tlf:
		for line in tlf:
			count = count+1
			if fds in line:
				# print("datostring funnet - linje "+str(count))
				dest.write(line)
			else:
				if (count < antall):
					print("Datostring ikke funnet - linje "+str(count))
				if (len(line) > 30): 
					# print("Writing to log2")
					log2.write(line)
				else: 
					print(Style.BRIGHT+Fore.RED+"Error, line not long enough! "+str(line).rstrip())
					# exit("sjekk line length")
				
	print("Done splitting files, sleeping for 3 seconds")
	time.sleep(3)

	dest.flush()
	dest.close()
	
	log2.flush()
	log2.close()
	
	fs2 = os.path.getsize(log2name)
	if (fs2 == 0): print("FATAL ERROR, 0 bytes!"), exit(666)
	
	print("Current size of filtered.log is: "+str(fs2))


	print("Renaming filtered.log to "+str(logfile))
	os.rename("filtered.log",logfile)
	print("Renamed filtered.log to "+str(logfile))

	print("Rename succesful?")
	print("Gikk fra "+str(fs)+" bytes til "+str(fs2)+" bytes!")
	
	diff = fs-fs2
	print("Differansen mellom gammel og ny logg: "+str(diff))
	
	fs3 = os.path.getsize(datefile)
	print(fs3)
	
	if (fs3 == diff): 
		print(Style.BRIGHT+Fore.GREEN+"Veldig awesome, alt stemmer!")
		return(True)
	else: 
		print("fs3 er ikke det samme som diff")
		print("Sleeing for 20 seconds")
		time.sleep(20)
		return(False)
	
	# 10.07.2018: Scriptet er egentlig avsluttet
	
	# True hvis ulik størrelse, endring ble gjort
	# False hvis samme størrelse, endring ble ikke gjort
	if (fs != fs2): return(True)
	else: return(False)


# No longer needs dagensdato in arguments, just firstdate
def checkfolder(firstdate,sensor):
	print("[Checkfolder]: "+str(firstdate)+" Sensor: "+str(sensor))
	
	# print("[CheckFolder]: "+str(firstdate)+" "+str(dagensdato))

	# Ting er visst ikke globale...
	cwd = os.getcwd()
	
	
	# year folder, month folder, "filename.log"
	yf = cwd+"/"+sensor+"/"+firstdate[0]
	ym = cwd+"/"+sensor+"/"+firstdate[0]+"/"+firstdate[1]
	datefile = ym+"/"+str(firstdate[2]+".log")
	print("Datefile is: "+str(datefile))

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
	
	# exit("Check for size")
	
	# 24.05.2018: Aner ikke hvorfor det er return her
	# return(datefile,string)

	# 24.05.2018: Som de er, siden funksjonen er ble kalt
	return(datefile,True)
	

# Sometimes, it is more fun to write things twice

def splittemp(firstdate,lastdate,sensor):
	# print("Type recieved: "+str(type(firstdate)))
	assert(type(firstdate) is list),"splittemp did not recieve type list (but maybe string)"
	
	# Only 1 argument needed, firstdate not lastdate
	datefile,b = checkfolder(firstdate,sensor)
	
	# First Date String
	fds = '-'.join(firstdate)
	print(firstdate,fds,datefile,b)
	
	logfile = sensor+"/temp.log"
	result = splittings(datefile,fds,logfile)
	print("result (to be returned): "+str(result))
	
	return(result)

from datetime import datetime

# Mine egne funksjoner
def main():
	# 04.07.2018: Hvis split.py blir executa, så skjer det egentlig ingenting her
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
