#!/home/pi/PILOTE/pilote/bin/python3
#i2c_master_pi.py
#  Connects to Arduino via I2C
  
#  DroneBot Workshop 2019
#  https://dronebotworkshop.com

# https://raspberrypi.stackexchange.com/questions/8469/meaning-of-cmd-param-in-write-i2c-block-data
# les fonctions I/O :
# http://wiki.erazor-zone.de/wiki%3alinux%3apython%3asmbus%3adoc
"""
pi@raspberrypi:~/PILOTE/pilote/misc_tests $ python
Python 2.7.16 (default, Apr  6 2019, 01:42:57)
[GCC 8.2.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import smbus
>>> help(smbus)
"""
"""
Il serait intéressant de trouver un moyen pour détecter la précence et la disponibilité
de l'arduino...
"""

from smbus import SMBus
import time
from pdb import set_trace as st
from sys import exit

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
n = 0
gpsDataFile = '../misc_tests/GggppssX-11'

def getHeading(line):
    h = float(line.split('|')[2])
    return "{:06}".format(h)

with open(gpsDataFile) as fp:
    line = fp.readline()
    while line:
        heading = getHeading(line)
        lheading = [len(heading)] + [ord(c) for c in list(heading)]
        print(heading)
        print(lheading)
        bus.write_i2c_block_data(addr, 17, lheading)
        time.sleep(0.5)
        line = fp.readline()
        n += 1
        if n > 15:
            break

st()

time.sleep(0.1)
