#!/home/hardy/pilote/bin/python

# https://mrjean1.github.io/PyGeodesy/

import os
from pygeodesy.formy import compassAngle
from pygeodesy.utily import radians, degrees

def toRad(v):
    # l = left side of '.'
    # r = right side of '.'
    l = v[0].split('.')[0]
    r = v[0].split('.')[1]
    if len(l) == 4:
        deg = float(l[:2])
        m = float(l[2:] + '.' + r)
    else:
        deg = float(l[:3])
        m = float(l[3:] + '.' + r)
    vDeg = deg + (m / 60)
    return radians(vDeg)
        


fich = "ggppss5"

coords = []

with open(fich) as fp:
    for line in iter(fp.readline, ''):
        # print (line)
        data = line.split(' ')
        lat = float(data[0])
        lon = float(data[1])
        track = float(data[2])
        coords.append((radians(lat), radians(lon), track))

for i in range(0, len(coords) -1):
    angle = compassAngle(
        coords[i][0], coords[i][1],
        coords[i + 1][0], coords[i + 1][1])
    print("%f %f" % (degrees(coords[i][0]), degrees(coords[i][1])) )
    print("%f %f" % (angle, coords[i][2]))
    print('\n')

	


