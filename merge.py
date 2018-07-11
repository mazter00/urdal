#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Merges temp.log with the previous day
..and every day as wanted.
Creates merge.log for plotting.py to work with

merge.py (this) has the responsibillity for date-cehcking
"""

from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)

def merge(ldm2,sensor):
	# List for dates to merge
	print("Hello, this is merge from merge.py")
	print("Argument recieved: "+str(ldm2)+" and sensor: "+str(sensor))
	print("We want to merge this number of files into one: "+str(len(ldm2)))
	
	mergedfile = sensor+"/merged.log"
	
	# Current temporary tempurate file
	cttf = sensor+"/temp.log"
	print("CTTF: "+str(cttf))
	
	print("mergedfile: "+str(mergedfile))
	with open(mergedfile,'w') as merged:
		
		for fil in ldm2:
			print("fil: "+str(fil))
			
			txt = open(fil,'r').read()
			
			print("Len of txt: "+str(len(txt)))
			
			merged.write(txt)
		
		print("Outside for loop, merging last file, temp.log")
		txt = open(cttf,'r').read()
		print("len av latest txt which should be temp.log from sensor: "+str(sensor)+" and len "+str(len(txt)))
		merged.write(txt)
			
	print("Merging ended, check merged.log, even with temp.log tacked on")
	
	return(True)


def version():
	return "v0.001"

# Assume temp.log is todays log, but import/read/merge yesterday

from datetime import datetime

# Mine egne funksjoner
def main():
	from plotting import today
	from plotting import extractdate

	print(Style.BRIGHT+"Merge "+version()+Style.NORMAL+" starting")

	f = today()
	if f is None: 
		print("F finnes ikke")
		exit()
	dagensdato = extractdate(f)
	print("Dagens dato er: "+str(dagensdato))

if __name__ == "__main__":
    # execute only if run as a script
    main()
