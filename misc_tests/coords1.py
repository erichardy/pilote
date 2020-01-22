#!/home/hardy/pilote/bin/python

# https://mrjean1.github.io/PyGeodesy/

import os
from pygeodesy.formy import compassAngle
from pygeodesy.utily import radians

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
        


fich = "ggppss3"

coords = []

with open(fich) as fp:
    for line in iter(fp.readline, ''):
        # print (line)
        datax = line.split(' ')[2]
        # print(datax)
        # $GPGLL or $GPGGA
        if datax[:6] == '$GPGLL':
            data = datax.split(',')
            lat_raw = (data[1], data[2])
            lon_raw = (data[3], data[4])
            print(lat_raw)
            print(toRad(lat_raw))
            print(lon_raw)
            print(toRad(lon_raw))
            print('\n')
            coords.append((toRad(lat_raw), toRad(lon_raw)))

for i in range(0, len(coords) -1):
    angle = compassAngle(
        coords[i][0], coords[i][1],
        coords[i + 1][0], coords[i + 1][1])
    print(angle)

	


