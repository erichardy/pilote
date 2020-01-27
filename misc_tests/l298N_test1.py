#!../../bin/python
# -*- coding: utf-8 -*-
# l298N_test1
# https://espace-raspberry-francais.fr/Composants/Module-L298N-controleur-moteur-Raspberry-Francais/

import RPi.GPIO as GPIO
from time import sleep
from pdb import set_trace as st


# definition des pins
M1_En = 21
M1_In1 = 20
M1_In2 = 16

# Creation d'une liste des pins pour le moteur
Pins = [M1_En, M1_In1, M1_In2]

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setwarnings(True)


GPIO.setup(M1_En, GPIO.OUT)
GPIO.setup(M1_In1, GPIO.OUT)
GPIO.setup(M1_In2, GPIO.OUT)

# M1_Vitesse = GPIO.PWM(M1_En, 250)
# M1_Vitesse.start(100)

def sens1() :
    GPIO.output(Pins[1], GPIO.HIGH)
    GPIO.output(Pins[2], GPIO.LOW)
    print("Moteur tourne dans le sens 1.")


def sens2() :
    GPIO.output(Pins[1], GPIO.LOW)
    GPIO.output(Pins[2], GPIO.HIGH)
    print("Moteur tourne dans le sens 2.")

def arret() :
    GPIO.output(Pins[1], GPIO.LOW)
    GPIO.output(Pins[2], GPIO.LOW)
    print("Moteurn arret.")

def arretComplet() :
    GPIO.output(Pins[1], GPIO.LOW)
    GPIO.output(Pins[2], GPIO.LOW)
    print("Moteur arrete.")

def stop():
    arretComplet()

def s1(t):
    sens1()
    sleep(t)
    stop()

def s2(t):
    sens2()
    sleep(t)
    stop()

arretComplet()

sens1()
sleep(10)
stop()
# sens2()
# sleep(10)
# stop()

st()
"""
for i in range(0,3):
    sens1()
    sleep(1)
    # arretComplet()
    # sleep(5)
    sens2()
    # sleep(2)
    # arret()
    sleep(1)
"""
GPIO.cleanup()


"""
environ 20" pour faire un aller simple de l'actionneur.
Q? : comment faire tourner l'actionneur pendant 20"
     puis 10" pour l'amener au milieu ?

course de l'actionneur : 208 - 11 = 197mm  /2 = 98,5mm
après 10s : 12mm
       9s : 110mm -> OK
       8s : 90mm

"""
