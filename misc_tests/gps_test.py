#!/home/hardy/pilote/bin/python


# import gps
from gps import *
import os
from pygeodesy.formy import compassAngle
from pygeodesy.utily import radians

from pdb import set_trace as st

session = gps(mode=WATCH_ENABLE)
try:
    while True:
        # Do stuff
        report = session.next()
        # Check report class for 'DEVICE' messages from gpsd.  If
        # we're expecting messages from multiple devices we should
        # inspect the message to determine which device
        # has just become available.  But if we're just listening
    # to a single device, this may do.
        if report['class'] == 'DEVICE':
            # Clean up our current connection.
            session.close()
            # Tell gpsd we're ready to receive messages.
            session = gps(mode=WATCH_ENABLE)
        # st()
        # print("%f %f" % report['lat'], report['lon'])
        # print(report)
        if report['class'] == 'TPV':
            # print(report)
            print("%f %f %f %s %f" % (
                report['lat'],
                report['lon'],
                report['track'],
                report['time'],
                report['speed']))
    # Do more stuff
except StopIteration:
    print ("GPSD has terminated")


