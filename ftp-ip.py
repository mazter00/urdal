#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ftplib import FTP
import os

ftp = FTP("cpanel64.proisp.no")
print("ftp? "+str(ftp))

# Laste inn passordet til FTPen
# Denne gang med absolutt filnavn
with open("/home/pi/pyscript/ftpassord.txt") as txtfile:
	passord = txtfile.read()

ftp.login(user="urdalerx", passwd = passord)

# Vi vet hva som er på serveren

ftp.cwd('public_html')

# Vi vet alltid plassering til filen vår
filepath = "/home/pi/Desktop/interface.txt"
filnavn  = "interface.txt"

ftp.storlines('STOR '+filnavn, open(filepath, "rb"))
