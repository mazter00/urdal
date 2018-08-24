#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
v0.002 26.06.2018 Able to upload custom files. Either by pure number, or from plotting.py
'''

from ftplib import FTP
import os
import sys
import time

# Fargelegging
from colorama import init
init()
from colorama import Fore, Back, Style
init(autoreset=True)

# ftp = FTP("files.000webhost.com")
# ftp = FTP("cpanel64.proisp.no")
ftp = FTP("ftp.urdalservices.com")

# 15.08.2018: Lagde ny FTP-konto i cPanel hos proisp kun for dette
# Brukernavn: temp@urdalservices.com
# FTP-server: ftp.urdalservices.com
# FTP-port: 21

# Laste inn passordet til FTPen
# with open("ftpassord.txt") as txtfile:
#	passord = txtfile.read()

with open("ftpassord2.txt") as txtfile:
	passord = txtfile.read()

# ftp.login(user="rivertemp", passwd = passord)
# ftp.login(user="urdalerx", passwd = passord)
ftp.login(user="temp@urdalservices.com", passwd = passord)

# Vi vet hva som er på serveren

ftp.cwd('public_html')

uploadfile=""
filepath=""
al = None

if (len(sys.argv) > 1):
	
	# argv list
	al = sys.argv[:]
	del al[0]
	print(al)
			
	if ("-upload" in al):
		print(Style.BRIGHT+Fore.CYAN+"Plot argument found; checking for argument")

		ali = al.index("-upload")
		ali1 = ali+1
		ali1txt = al[ali1]
		
		try:
			uploadfile = al[ali1]
		except:
			print(Style.BRIGHT+Fore.RED+"Please add the filename to be uploaded. Exiting...")
			# return(False)

		print("ali: "+str(ali))
		print("ali txt: "+str(ali1txt))

		print("Assume this is the file to be uploaded")

		del al[ali1]


# For moro skyld
# listftp = ftp.retrlines('LIST')

# Vi vet alltid plassering til filen vår
if (uploadfile == ""):
	print("Uploadfile is empty; Using default file (TP-temp.png)")
	filepath = "/home/pi/pyscript/temp/urdal/TP-temp.png"
	filnavn = "TP-temp.png"
else:
	if ("png" in uploadfile): 
		filepath = uploadfile
		print("png found in filepath")
	else: 
		filepath = "/home/pi/pyscript/temp/urdal/temp"+uploadfile+".png"
		print("png NOT found in filepath")
		
	print("Current (custom/requsted) filepath: "+str(filepath))
	print("Current (custom/requsted) uploadfile: "+str(uploadfile))
	
	# print(type(filepath))
	
	uploadfileshort = filepath.rsplit("/")[-1]
	# print(uploadfileshort)
	
	# uploadfileshort = uploadfileshort[-1]
	# print(uploadfileshort)
	
	print("Requested filepath (short): "+str(uploadfileshort))
	
	filnavn = uploadfileshort
	print("filnavn ifra uploadfile: "+Style.BRIGHT+str(filnavn))
	
print("Sleeping for 10 seconds in fear of a automatic ban")
time.sleep(10)
ftp.storbinary('STOR '+filnavn, open(filepath, "rb"), 1024)

if al is not None:
	print("FTP-scriptet ended with arguments of: "+str(al))
