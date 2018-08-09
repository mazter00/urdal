# Prosjekt Elvemåler
Codebase for Prosjekt Elvemåler.

Installation: Not automatic, but if you download this as zipped, unzip it into a folder, copy to where you want it to be, i.e. /home/pi/pyscript and then use it.

What it does: It reads a serial connection from Arduino, reads lines which has "Temperature" in it and writes it to a single file at ./TP/temp.log. The file sread.py does that.

sread.py also calls plotting.py at timed intervalls and plotting.py uses matplotlib to make graphs. At the end of plotting.py, it calls ftp.py to upload it to a given webhost.

read-dht.py reads the AM2302/DHT22-sensor plugged into Raspberry Pi 3. It will log to ./AM/temp.log and call plotting.py at timed intervals.

Commandline options:

A user can any time make a graph for any sensor for any time duration (in hours), with or without FTP-upload and with or without local showing of the plot. (You can ask matplotlib to show the plot or not.)

Any combination is allowed:

python3 plotting.py -time 25
python3 plotting.py -time 25 -plot
python3 plotting.py -time 25 -plot -intervall 3600
python3 plotting.py -time 25 -plot -intervall 3600 -log "TP|AM"
python3 plotting.py -time 25 -plot -intervall 3600 -sensor "TP|AM"
python3 plotting.py -time 25 -plot -intervall 3600 -luft (Will assume sensor and log to be "AM")


