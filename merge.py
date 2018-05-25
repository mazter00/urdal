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

def merge(ldm):
	# List for dates to merge
	print("Hello, this is merge from merge.py")


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
