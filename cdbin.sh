#!/bin/bash
cd /home/pi/pyscript
lxterminal --command python3 sread.py
# 20.06.2018: sread.py er ansvarlig for å holde vindu åpent
# 27.06.2018: Husk at Python2 brukes, ikke python3
lxterminal --command python2 read-dht.py
