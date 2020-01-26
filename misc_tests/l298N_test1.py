# -*- coding: utf-8 -*-
# l298N_test1
# https://espace-raspberry-francais.fr/Composants/Module-L298N-controleur-moteur-Raspberry-Francais/

import RPi.GPIO as GPIO
from time import sleep


# Definition des pins
M1_En = 21
M1_In1 = 20
M1_In2 = 16

# Creation d'une liste des pins pour le moteur
Pins = [M1_En, M1_In1, M1_In2]

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(M1_En, GPIO.OUT)
GPIO.setup(M1_In1, GPIO.OUT)
GPIO.setup(M1_In2, GPIO.OUT)

M1_Vitesse = GPIO.PWM(M1_En, 100)
M1_Vitesse.start(100)


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

arretComplet()

while True :
    # Exemple de motif de boucle
    sens1()
    sleep(3)
    arretComplet()
    sleep(5)
    sens2(1)
    sleep(2)
    arret(1)
    sleep(1)
