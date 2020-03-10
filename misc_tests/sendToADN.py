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
durations = [2000, 1345, 55, 4565,
             4777, 1254, 4686, 741]

i = 0

while i < len(steerings):
    steering = ord(steerings[i])
    x_duration = "{:05}".format(durations[i])
    duration = [ord(d) for d in x_duration]
    print(steering)
    print(duration)
    # must wait the motor is free (not moving) before to send command !
    # only b-200, t-1254 and b-741 are received and excecuted...
    bus.write_block_data(addr, steering, duration)
    time.sleep(0.5)
    i += 1
    

time.sleep(0.1)

