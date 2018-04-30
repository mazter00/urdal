#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ftplib import FTP
import os

ftp = FTP("files.000webhost.com")

# Laste inn passordet til FTPen
with open("ftpassord.txt") as txtfile:
	passord = txtfile.read()

ftp.login(user="rivertemp", passwd = passord)

# Vi vet hva som er på serveren

ftp.cwd('public_html')

# For moro skyld
ftp.retrlines('LIST')

# Vi vet alltid plassering til filen vår
filepath = "/home/pi/pyscript/temp/urdal/temp.png"
filnavn ="temp.png"

ftp.storbinary('STOR '+filnavn, open(filepath, "rb"), 1024)
