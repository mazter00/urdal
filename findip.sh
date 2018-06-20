#!/bin/bash
echo "Waiting 30 seconds before finding IP..."
sleep 30
echo "My ifconfig info is:" > interface.txt
ifconfig >> interface.txt
echo "Curl found this external IP:" >> interface.txt
curl http://bot.whatismyipaddress.com/ >> interface.txt
echo -e "\n" >> interface.txt
cd /home/pi/pyscript
echo $PWD
sleep 10
lxterminal --command python3 ftp-ip.py
