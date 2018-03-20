import matplotlib
print(matplotlib.__version__)
print(str(matplotlib.__file__))

import numpy
print(numpy.version.version)
print(numpy.__path__)

import os
fs = os.path.getsize("temp.log")
print("Bytes: "+str(fs))

import math

fsL = math.floor(fs/33)
print("Antatt antall linjer: "+str(fsL))
# exit(2)

from datetime import datetime
d = datetime.now().isoformat()
e = d.find('T')
# print("e: "+str(e))

f = d[0:e]
print("f: "+str(f))


def extractdate(f):

	year = None
	month = None
	day = None
	print("extractdate start with string: "+str(f))

	# error checks
	
	if not len(f) >= 10:
		print("String ikke lang nok")
		return None
	
	if not f.count('-') == 2:
		print("Feil i string, forventet to bindestreker")
		return None
	
	while (year is None):
		while (month is None):
			while (day is None):
				# print("Finn dagen")
				day = f[8:10]
				# print(day)
			# print("Finn måneden")
			month = f[5:7]
			# print(month)
		# print("Finn året")
		year = f[0:4]
		# print(year)
	return (year,month,day)

dagensdato = extractdate(f)
print("Dagens dato er: "+str(dagensdato))
	
# 19.03.2018 - Finne øverste dato og sjekk om folder finnes

with open('temp.log') as fl:
    first_line = fl.readline().strip()

print("Første llinje: "+str(first_line))

firstdate = extractdate(first_line)

# Ønsker at det skal være tuple
#print("Type: "+str(type(firstdate)))

print("Øverste dato kan være: "+str(firstdate))

# Sjekk for folder

import os
cwd = os.getcwd()
print("cwd: "+str(cwd))

def checkfolder(firstdate):

	# year folder, month folder, "filename.log"
	yf = cwd+"/"+firstdate[0]
	ym = cwd+"/"+firstdate[0]+"/"+firstdate[1]
	datefile = ym+"/"+str(firstdate[2]+".log")

	print("yf: "+str(yf))
	print("ym: "+str(ym))
	print("datefile: "+str(datefile))

	if not os.path.exists(yf):
		os.makedirs(yf)
		print("FOLDER "+str(yf)+" created!")

	if not os.path.exists(ym):
		os.makedirs(ym)
		print("FOLDER "+str(ym)+" created!")

	if not os.path.isfile(datefile):
		open(datefile,'x')
		print("FILE "+str(datefile)+" created!")
	string = firstdate[0]+"-"+firstdate[1]+"-"+firstdate[2]
	return (datefile,string)

print("Sjekker for dagens dato")

dagensdatofile = checkfolder(dagensdato)[0]
dagensdatostring = checkfolder(dagensdato)[1]

print("Sjekker for øverste dato")

firstdatefile = checkfolder(firstdate)[0]
firstdatestring = checkfolder(firstdate)[1]

print("firstdatefile: "+str(firstdatefile))

# print strings
print("Dagens Dato String: "+str(dagensdatostring))
print("First Date String: "+str(firstdatestring))

# Hvis dagensdato og øverste dato er ulike, så må vi renske filer

if dagensdato != firstdate:
	print(str(dagensdato)+" er ulik fra "+str(firstdate))
	
	print("Vi må flytte VELDIG mange linjer fra tenp.log til "+str(firstdatefile))
	
	# Åpner destination først
	dest = open(firstdatefile,'w')
	
	# Åpner backup templog2.log
	log2 = open("temp2.log",'w')
	
	# tenp log file
	count = 0
	
	with open("temp.log") as tlf:
		for line in tlf:
			count = count+1
			if firstdatestring in line:
				print("datostring funnet - linje "+str(count))
				dest.write(line)
			else:
				print("Ikke funnet - linje "+str(count))
				log2.write(line)
				
	fs2 = os.path.getsize("temp2.log")
	os.rename("temp2.log","temp.log")
	print("Rename succesful?")
	print("Gikk fra "+str(fs)+" bytes til "+str(fs2)+" bytes!")

def removedecimal():
	temp2 = open("temp2.log",'w')
	
	count = 0
	with open("temp.log") as temp:
		for line in temp:
			count = count+1
			line = line.strip()
			t = line.split(" ")
			txt = t[0]
			t = float(t[1])
			t = round(t,1)
			print("Linje: "+str(count)+" T: "+str(t))
			print("Print: "+str(txt)+" "+str(t))
			temp2.write(str(txt)+" "+str(t)+"\n")
	
	os.rename("temp2.log","temp.log")
	print("Rename succesful? for desimal-kutt")
	
	
removedecimal()

# print("exit")
# exit(9)

matplotlib.use('tkagg')
import matplotlib.pyplot as plt

with open('temp.log') as f:
    lines = f.readlines()
    # x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]

# print(y)

plt.grid(True)
# plt.set_major_locator(ticker.AutoLocator())
# plt.yticks(numpy.arange(min(y), max(y)+1, 1.0))



# plt.plot(x)
plt.plot(y)
plt.ylabel('Temperatur')
plt.title(dagensdatostring)

plt.autoscale(enable=True, axis='y')


plt.show()
