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

def merge(ldm2):
	# List for dates to merge
	print("Hello, this is merge from merge.py")
	print("Argument recieved: "+str(ldm2))
	print("We want to merge this number of files into one: "+str(len(ldm2)))
	
	with open("merged.log",'w') as merged:
		
		for fil in ldm2:
			print("fil: "+str(fil))
			
			txt = open(fil,'r').read()
			
			print("Len of txt: "+str(len(txt)))
			
			merged.write(txt)
		
		print("Outside for loop, merging last file, temp.log")
		txt = open("temp.log",'r').read()
		merged.write(txt)
			
	print("Merging ended, check merged.log, even with temp.log added on")
			
		
	
	# Return False until code is complete
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
