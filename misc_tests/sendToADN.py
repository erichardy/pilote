#  sendToADN.py
#  Connects to Arduino via I2C
  
#  DroneBot Workshop 2019
#  https://dronebotworkshop.com

# https://raspberrypi.stackexchange.com/questions/8469/meaning-of-cmd-param-in-write-i2c-block-data
# http://wiki.erazor-zone.de/wiki%3alinux%3apython%3asmbus%3adoc

from smbus import SMBus
import time
from pdb import set_trace as st
from sys import exit

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

steerings = ['b', 'b', 't', 'b', 't', 't', 't', 'b']
durations = [200, 134, 855, 565,
             777, 254, 686, 741]

i = 0

while i < len(steerings):
    steering = ord(steerings[i])
    x_duration = "{:05}".format(durations[i])
    duration = [ord(d) for d in x_duration]
    print("%s %i %i %s" % (
        steerings[i], steering,
        durations[i], duration))
    bus.write_block_data(addr, steering, duration)
    time.sleep(0.95)
    i += 1
    

time.sleep(0.1)

