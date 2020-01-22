#!/home/hardy/pilote/bin/python


# import gps
from gps import *
import os
from pygeodesy.formy import compassAngle
from pygeodesy.utily import radians

from pdb import set_trace as st

gpsKeys = []
gpsKeys.append('lat')
gpsKeys.append('lon')
gpsKeys.append('track')
gpsKeys.append('time')
gpsKeys.append('speed')
gpsKeys.append('ept')
gpsKeys.append('alt')
gpsKeys.append('mode')
gpsKeys.append('epv')

gpsData = []

# ggppss = os.open('ggppssX', os.O_CREAT|os.O_APPEND)
ggppss = open('ggppssX', 'a')

def getData(report):
    data = {}
    for d in gpsKeys:
        try:
            data[d] = report[d]
        except:
            data[d] = 0.0
    return data

def gpsSTR(data):
    gps_s = ''
    for d in gpsKeys:
        gps_s += str(data[d]) + '|'
    gps_s += '\n'
    return gps_s

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
        if report['class'] == 'TPV':
            data = getData(report)
            ggppss.write(gpsSTR(data))
            print(gpsSTR(data))
            # print(report)
            # print(report)
            """
            print("%f %f %f %s %f %f %f %i %f" % (
                report['lat'],
                report['lon'],
                report['track'],
                report['time'],
                report['speed'],
                report['ept'],
                report['alt'],
                report['mode'],
                report['epv']
                ))
           """

    # Do more stuff
except StopIteration:
    print ("GPSD has terminated")


