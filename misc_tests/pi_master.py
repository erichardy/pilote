#  i2c_master_pi.py
#  Connects to Arduino via I2C
  
#  DroneBot Workshop 2019
#  https://dronebotworkshop.com

# https://raspberrypi.stackexchange.com/questions/8469/meaning-of-cmd-param-in-write-i2c-block-data
# http://wiki.erazor-zone.de/wiki%3alinux%3apython%3asmbus%3adoc
"""
pi@raspberrypi:~/PILOTE/pilote/misc_tests $ python
Python 2.7.16 (default, Apr  6 2019, 01:42:57)
[GCC 8.2.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import smbus
>>> help(smbus)
"""


from smbus import SMBus
import time
from pdb import set_trace as st
from sys import exit

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

"""
while 1:
    nb = input(">>>>   ")
    if int(nb) == 9:
        exit()
    msg= bus.read_i2c_block_data(addr, 7)
    st()
"""

while 1:
    print ("combien de nombres a envoyer...")
    nb = input(">>>>   ")
    msg = [x + 48 for x in list(range(int(nb)))]
    print(msg)
    bus.write_block_data(addr, 7, msg)
    if int(nb) == 9:
        break;
time.sleep(0.1)
"""
while 1:
    nb = input('>>>> ')
    lec = bus.read_byte(addr)
    print(type(lec))
    print(lec)
    print("\n")
    if int(nb) == 9:
        break;
"""

# time.sleep(1)
# xcar = bus.read_byte(addr)
# print(type(xcar))
# print("%i\n" % (xcar))
