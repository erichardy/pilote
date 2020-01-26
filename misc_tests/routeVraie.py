#!../bin/python

import os
import sys
from pygeodesy.formy import compassAngle
from pygeodesy.utily import radians, degrees
from math import atan, cos
from pdb import set_trace as st

"""
GggppssX-11 lignes 2 et 3
48.164788333|-4.046563333|333.09|2020-01-25T14:19:20.000Z|29.786|0.005|93.7|3|19.32|
48.16503|-4.04674|335.04|2020-01-25T14:19:21.000Z|29.658|0.005|92.6|3|19.32|

"""
l0 = 48.164788333
ll0 = -4.046563333
l1 = 48.16503
ll1 = -4.04674

lat0 = radians(48.164788333)
lon0 = radians(-4.046563333)

lat1 = radians(48.16503)
lon1 = radians(-4.04674)

def toTuple(angle):
    # convertit un angle en tuple de (Deg, min, sec)
    deg = int(angle)
    rDeg = (angle - deg) * 60
    if rDeg < 0:
        rDeg = rDeg * -1
    mins = int(rDeg)
    sec = (rDeg - mins) * 60
    return (deg, mins, sec)



def lox(la0, lo0, la1, lo1):
    # cf https://fr.wikipedia.org/wiki/Loxodromie
    latm = (lat0 + lat1) / 2
    tanRv = ((lon1 - lon0) / (lat1 - lat0)) * cos(latm)
    rV = atan(tanRv)
    return rV


print(toTuple(48.164788333))
print(toTuple(-4.046563333))
print(toTuple(48.16503))
print(toTuple(-4.04674))


loxodromy = degrees(lox(lat0, lon0, lat1, lon1))
cAngle = compassAngle(lat0, lon0, lat1, lon1)
st()
print("%.5f\t%.5f" % (loxodromy, cAngle))






