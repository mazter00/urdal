#!/usr/bin/python3

# 06.04.2018
# Lager denn python-fila for å sjekke matplotlib
# Merk at dette er fra "plotting.py" som finnes på Github. Det er en direkte kopi.
# matplotlib er installert via Pycharm, og pythonfila må være lagd av Pycharm også.
# Deretter er det å gjøre det Windows-spesifikk.

'''
v0.002 20.03.2018: Fikse opp temp.log
'''

# OPTIONS

kuttdesimaler = False
drawplot = True

import matplotlib

print(matplotlib.__version__)
print(str(matplotlib.__file__))

import numpy

print(numpy.version.version)
# print(numpy.__path__)

import os
print("Current platform: "+str(os.name))

# Endring fra rPI til Win7
# Windows krever raw string
templog = r"C:\pyscript\temp.log"
templog2 = r"C:\pyscript\temp2.log"

fs = os.path.getsize(templog)
print("Bytes: " + str(fs))

assert (fs > 0),"Vil ha noe å jobbe med"

import math

fsL = math.floor(fs / 33)
print("Antatt antall linjer: " + str(fsL))


# exit(2)

def fikslinje():
    """Fikse manglende linjeskift i temp.log"""

    with open(templog) as ff:
        f = ff.read()

        s = f.split()
        print("0: " + str(s[0]) + " 1: " + str(s[1]))
        # TODO: Kode ikke ferdig. Fikser ikke det jeg vil fikse
        # exit(10)
        pass


fikslinje()

from datetime import datetime

d = datetime.now().isoformat()
e = d.find('T')
# print("e: "+str(e))

f = d[0:e]
print("f: " + str(f))


def extractdate(f):
    year = None
    month = None
    day = None
    print("extractdate start with string: " + str(f))

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
    return (year, month, day)


dagensdato = extractdate(f)
print("Dagens dato er: " + str(dagensdato))

# 19.03.2018 - Finne øverste dato og sjekk om folder finnes

with open(templog) as fl:
    first_line = fl.readline().strip()

print("Første linje: " + str(first_line))

firstdate = extractdate(first_line)

# Ønsker at det skal være tuple
# print("Type: "+str(type(firstdate)))

print("Øverste dato kan være: " + str(firstdate))

# Sjekk for folder

import os

cwd = os.getcwd()
print("cwd: " + str(cwd))


def checkfolder(firstdate):
    # year folder, month folder, "filename.log"
    yf = cwd + "/" + firstdate[0]
    ym = cwd + "/" + firstdate[0] + "/" + firstdate[1]
    datefile = ym + "/" + str(firstdate[2] + ".log")

    print("yf: " + str(yf))
    print("ym: " + str(ym))
    print("datefile: " + str(datefile))

    if not os.path.exists(yf):
        os.makedirs(yf)
        print("FOLDER " + str(yf) + " created!")

    if not os.path.exists(ym):
        os.makedirs(ym)
        print("FOLDER " + str(ym) + " created!")

    if not os.path.isfile(datefile):
        open(datefile, 'x')
        print("FILE " + str(datefile) + " created!")
    string = firstdate[0] + "-" + firstdate[1] + "-" + firstdate[2]
    return (datefile, string)


print("Sjekker for dagens dato")

dagensdatofile = checkfolder(dagensdato)[0]
dagensdatostring = checkfolder(dagensdato)[1]

print("Sjekker for øverste dato")

firstdatefile = checkfolder(firstdate)[0]
firstdatestring = checkfolder(firstdate)[1]

print("firstdatefile: " + str(firstdatefile))

# print strings
print("Dagens Dato String: " + str(dagensdatostring))
print("First Date String: " + str(firstdatestring))

# Hvis dagensdato og øverste dato er ulike, så må vi renske filer

if dagensdato != firstdate:
    print(str(dagensdato) + " er ulik fra " + str(firstdate))

    print("Vi må flytte VELDIG mange linjer fra tenp.log til " + str(firstdatefile))

    # Åpner destination først
    dest = open(firstdatefile, 'w')

    # Åpner backup templog2.log
    log2 = open(templog2, 'w')

    # tenp log file
    count = 0

    with open(templog) as tlf:
        for line in tlf:
            count = count + 1
            if firstdatestring in line:
                print("datostring funnet - linje " + str(count))
                dest.write(line)
            else:
                print("datostring Ikke funnet - linje " + str(count))
                log2.write(line)
    # Kanskje ikke så dumt å lukke filen? Hva med log2?
    tlf.close()
    log2.close()

    fs2 = os.path.getsize(templog2)
    if (os.name == "nt"):
        os.replace(templog2, templog)
    else:
        os.rename(templog2, templog)
    print("Rename succesful?")
    print("Gikk fra " + str(fs) + " bytes til " + str(fs2) + " bytes!")


def removedecimal():
    temp2 = open(templog2, 'w')

    count = 0
    with open(templog) as temp:
        for line in temp:
            count = count + 1
            line = line.strip()
            t = line.split(" ")
            txt = t[0]
            t = float(t[1])
            t = round(t, 1)
            print("Linje: " + str(count) + " T: " + str(t))
            print("Print: " + str(txt) + " " + str(t))
            temp2.write(str(txt) + " " + str(t) + "\n")

    temp2.close()
    os.rename(templog2, templog)
    print("Rename succesful? for desimal-kutt")


if kuttdesimaler is True:
    removedecimal()
else:
    print("Beholder desimalene")

# print("exit")
# exit(9)

if drawplot is False:
    print("Ikke vise plot, endre i options")
    exit("no show plot")

matplotlib.use('tkagg')
import matplotlib.pyplot as plt

with open(templog) as f:
    lines = f.readlines()
    # disable x til vi konverterer dato
    # x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]

# Sette ax for senere, MaxNLocator er ETTER plot, import as figure
# from matplotlib.pyplot import figure as figure
from matplotlib.ticker import MaxNLocator as MaxNLocator

# Override X from the start

# x = numpy.linspace(0,24,24,endpoint=False)
# print("Len av generert x: "+str(len(x)))
# print(x)

# print(y)

# print(len(x))
print(len(y))

# Finne egen min og max value av y

print("Len av y: +str(len(y)))")
assert (len(y)>0),"Y bør være over null"
s = sorted(y)
ymin = s[0]
ymax = s[len(y) - 1]

# tymi = type(ymin)
# tyma = type(ymax)

ymin = float(ymin)
ymax = float(ymax)

# print("Type av ymin: "+str(type(ymin)))
# print("Type av ymax: "+str(type(ymax)))

print("ymin: " + str(ymin))
print("ymax: " + str(ymax))

ymin2 = math.floor(ymin)
ymax2 = round(ymax)

print("ymin2: " + str(ymin2))
print("ymax2: " + str(ymax2))

# Sjekk om jeg kan sjekke om disse er satt

plt.grid(True)

npa = numpy.arange(ymin2, ymax2, 0.1)
print("Type av npa: " + str(type(npa)))
print("Numpy arange: " + str(npa))

linspace = numpy.linspace(ymin2, ymax2, num=ymax2 - ymin, endpoint=False, retstep=True, dtype=int)
print(linspace)

# linspacelist = linspace.tolist()
# print(linspacelist)

# exit(11)

# Se nærmere på denne - skal ikke ha stepping?
print("Før vi setter inn npa: " + str(npa))
print("Før vi setter inn linsace: " + str(linspace))

# plt.yticks(npa)

# plt.set_yticklabels(npa)

# Lage "ticks" for x

# numpy arrange X axis
npax = numpy.arange(24)
# Printer 0-23 som forventet
# print(str(npax))

# Lar xticks være default
# plt.xticks(npax)

# Vet ikke om denne er noe
# plt.plot.Axis.set_major_locator(ticker.MaxNLocator(integer=True))

# ax rett før plot
# Bruke plt for å unnga dobling av grafer
# ax = plt().gca()
# ax = figure().gca()
# kl 12:37 - gir opp ax
# print(ax)


# plt.plot(x)
plt.plot(y)

plt.ylabel('Temperatur')
plt.title(dagensdatostring)

# Gjør ikke mye forskjell, om noe
# plt.autoscale(enable=True, axis='y')

# Her finner vi ut av vi har 40 ylabels
locs, labs = plt.yticks()
print("Locs: " + str(locs))
print(labs)

# plt.locator_params(axis='y', nbins=auto)
# plt.locator_params(axis='x', nbins=auto)


# Last best hope
# plt og ikke ax
# Er det denne som lager to plots?
# plt.axes.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.show()