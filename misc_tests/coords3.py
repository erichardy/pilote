#!../bin/python
# -*- coding: utf-8 -*-

# https://mrjean1.github.io/PyGeodesy/

import os
import sys
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
        


fich = sys.argv[1]

coords = []

with open(fich) as fp:
    for line in iter(fp.readline, ''):
        # print (line)
        data = line.split('|')
        lat = float(data[0])
        lon = float(data[1])
        track = float(data[2])
        coords.append((lat, lon,
                      (lat - 48.0) * 10,
                      (lon + 4.0) * 100,
                      track))
pangle = 0.0
panglea = 0.0
ptrack = 0.0
for i in range(0, len(coords) -1):
    la = coords[i][0]
    lo = coords[i][1]
    laa = coords[i][2]
    loa = coords[i][3]
    lat0 = radians(coords[i][0])
    lon0 = radians(coords[i][1])
    lat1 = radians(coords[i + 1][0])
    lon1 = radians(coords[i + 1][1])
    angle = compassAngle(lat0, lon0, lat1, lon1)

    lat0a = radians(coords[i][2])
    lon0a = radians(coords[i][3])
    lat1a = radians(coords[i + 1][2])
    lon1a = radians(coords[i + 1][3])
    anglea = compassAngle(lat0a, lon0a, lat1a, lon1a)
    track = coords[i + 1][4]

    # print('angle (Delta)\tRedui(Delta)\tTrack(Delta)')
    print("%.5f %.5f /// %.5f %.5f" % (la, lo, laa, loa))
    print("%.5f %.5f /// %.5f %.5f" % (lat0, lon0, lat0a, lon0a))
    print("%f (%f)\t%f (%f)\t%f (%f)" %
          (angle, angle - pangle,
           anglea, anglea - panglea,
           track, track - ptrack))
    print('\n')
    pangle = angle
    panglea = anglea
    ptrack = track
    # print('\n')

"""
il y a des grandes variations de l'angle de la route avec les
coordonnées brutes...!
les coordonnées postfixées avec 'a' sont des coordonnées modifiées
de façon à être (probablement) moins sensibles aux erreurs d'arondis
dans le calcul de la route : fonction compassAngle()
A VERIFIER :
que les coordonnées modifiées sont, les unes par rapport aux autres,
positionnées de la même façon... avec vérifier avec gnuplot... 
"""


