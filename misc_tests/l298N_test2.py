#!../../bin/python
# -*- coding: utf-8 -*-
# l298N_test2
# https://espace-raspberry-francais.fr/Composants/Module-L298N-controleur-moteur-Raspberry-Francais/

# test : Utilisation de gpiozero (vs RPi.GPIO)

from gpiozero import Motor
from time import sleep
from pdb import set_trace as st


# definition des pins
En = 21
In1 = 20
In2 = 16

# le parametre de sleep peut-etre un flottant
# ce qui permet d'avoir plus de precisions dans le deplacement


def push(t):
    m.forward()
    sleep(t)
    m.stop()

def pull(t):
    m.backward()
    sleep(t)
    m.stop()

m = Motor(In1, In2, En, False)
"""
m.forward()
print(m.is_active)
sleep(3)
m.reverse()
sleep(1)
m.stop()
"""
st()

"""
environ 20" pour faire un aller simple de l'actionneur.
Q? : comment faire tourner l'actionneur pendant 20"
     puis 10" pour l'amener au milieu ?

course de l'actionneur : 208 - 11 = 197mm  /2 = 98,5mm
après 10s : 12mm
       9s : 107mm -> OK
       8s : 90mm
       8.7s : 96mm

"""
