#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ftplib import FTP
import os

# ftp = FTP("files.000webhost.com")
ftp = FTP("cpanel64.proisp.no")

# Laste inn passordet til FTPen
with open("ftpassord.txt") as txtfile:
	passord = txtfile.read()

# ftp.login(user="rivertemp", passwd = passord)
ftp.login(user="urdalerx", passwd = passord)

# Vi vet hva som er på serveren

ftp.cwd('public_html')

uploadfile=""

if (len(sys.argv) > 1):
	
	# argv list
	al = sys.argv[:]
	del al[0]
	print(al)
			
	if ("-upload" in al):
		print(Style.BRIGHT+Fore.CYAN+"Plot argument found; checking for argument")

		ali1 = ali+1
		uploadfile = al[ali1]

		print("ali: "+str(ali))
		print("ali txt: "+str(ali1txt))

		print("Assume this is the file to be uploaded")

		del al[0]


# For moro skyld
# listftp = ftp.retrlines('LIST')

# Vi vet alltid plassering til filen vår
if (uploadfile == ""):
	filepath = "/home/pi/pyscript/temp/urdal/temp.png"
	filnavn = "temp.png"
else:
	filepath = "/home/pi/pyscript/temp/urdal/"+uploadfile
	print("Requested filepath: "+str(uploadfile))
	
	filnavn = uploadfile
	print("filnav ifra uploadfile: "+str(filnavn))
	

ftp.storbinary('STOR '+filnavn, open(filepath, "rb"), 1024)

print("FTP-scriptet ended")
