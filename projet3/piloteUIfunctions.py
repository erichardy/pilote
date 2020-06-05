#!../bin/python3

from pdb import set_trace as st
from tkinter import *
from functools import partial
import turtle
import time
import threading
import queue
import sys
import os
import argparse
from smbus import SMBus
sys.path.append('/home/pi/PILOTE/pilote/lib/python3.7/site-packages')
# from simple_pid import PID
from gps import WATCH_ENABLE, gps

# debugMode = True
# debugMode = False
# PIDTunigMode = True

GPSstarted = True
currentMode = str('manual')

headingCurrent = '0.0'
headingTarget = '0.0'

# global variables for UI widjets
mainWindow = Tk()
babord5 = Button(mainWindow)
babord1 = Button(mainWindow)
changeMode = Button(mainWindow)
tribord1 = Button(mainWindow)
tribord5 = Button(mainWindow)

currentHeading = Label(mainWindow,
                       text="current Heading")
realTimeHeading = Label(mainWindow,
                    text="Real Time Heading")
targetHeading = Label(mainWindow,
                      text="target Heading",
                      pady=2)

quitButton = Button(mainWindow)
compassDrawCanvas = Canvas(mainWindow)
headingScreen = turtle.TurtleScreen(compassDrawCanvas)
desiredHeading = turtle.RawTurtle(headingScreen)
actualHeading = turtle.RawTurtle(headingScreen)


tillerDouble = False
finished = False

# Args parser
parser = argparse.ArgumentParser(description='Essais args ')
parser.add_argument('-t', help='Tunnig mode', action="store_true")
parser.add_argument('-p', help='PID tunning mode', action="store_true")
parser.add_argument('-s', help='Simulation mode', action="store_true")

args = parser.parse_args()
PIDTunigMode = args.p
tuningMode = args.t
# END Args parser

# pilote control
# piloteCTL = PID(1, 1, 1, 0.0)

MIN_ANGLE = 8
MAX_ANGLE = 40
MULTIPLIER = 100
SAMPLES = 6

# correction entre le mouvement babord et tribord car l'actuateur ne se déplace
# pas egalement pour t ou b
# si > 1 : b = t * BT_CORRECTION
BT_CORRECTION = 1.06

if PIDTunigMode:
    pidp = Spinbox(mainWindow)
    pidi = Spinbox(mainWindow)
    pidd = Spinbox(mainWindow)
    pidpVal = DoubleVar(mainWindow)
    pidiVal = DoubleVar(mainWindow)
    piddVal = DoubleVar(mainWindow)

if tuningMode:
    # minAngle : trigger, move the tiller if delta beetween currentHeading
    # and targetHeading is grater this value 
    minAngle = Spinbox(mainWindow)
    # maxAngle : if delta if grater this value, !!!PROBLEM!!!
    maxAngle = Spinbox(mainWindow)
    # multipier : factor to angle for convertion of the angle
    # to duration movement of the tiller
    multiplier = Spinbox(mainWindow)
    # samples : number of samples used to compute mean heading
    samples = Spinbox(mainWindow)
    # flipTillerCmds : 'b' becomes 't' and 't' becomes 'b'
    # for test purposes
    flipTillerCmds = Button(mainWindow)
    
    minAngleVal = DoubleVar(mainWindow)
    maxAngleVal = DoubleVar(mainWindow)
    multiplierVal = IntVar(mainWindow)
    samplesVal = IntVar(mainWindow)
    flipTiller = False
    

q = queue.Queue()

# lastSendTime : time of the last command sent to ADN
# is modified every send command (see sendToADN())
lastSendTime = time.time()


def tillerDoubleSwitch(but):
    global tillerDouble
    
    if not tillerDouble:
        but.config(background='#9932CC',
                   activebackground='#9932CC',
                   text='Désactiver Double\n Mouvement de barre')
    else:
        but.config(background='#FF8C00',
                   activebackground='#FF8C00',
                   text='Activer Double\n Mouvement de barre')
    tillerDouble = not tillerDouble
    

def baTri(params):
    """
    Change direction : babord / Tribord
    If in pilote mode :
        display the new target heading in UI : the new target heading depends of
        the current target and the command received in params,
        and modify the target heading : headingTarget variable
        !!! NB : the global variable headingTarget is updated !!!
    If in manual mode : send command to change the tiller angle
    or heading if tillerDouble is True
    :params: params is a tuple ('b|t', 1|5)
        b = babord
        t = tribord
        1 = 1°
        5 = 5°
    """
    global headingTarget
    if currentMode == 'pilote':
        if params[0] == 'b':
            newTarget = updateTargetHeading('a', headingTarget, params[1])
        else:
            newTarget = updateTargetHeading('s', headingTarget, params[1])
        headingTarget = newTarget
        targetHeading.config(text=headingTarget)
        desiredHeading.settiltangle(360 - float(headingTarget) + 90)
        print('Heading modified !')
    else:
        # if not in pilote mode, interract directly with actuator
        sendToADN(params[0], params[1])
        

def sendAlert():
    print('ALERT ALERT ALERT !!!!!!')

def sendToADN(direction, value):
    """
    direction is 'b' ot 't', but ca be reversed if flipTiller is True
    the value is an angle and is transformed to a duration of the actuator
    movement by MULTIPLIER
    """
    global lastSendTime
    currentTime = time.time()

    MULTIPLIER = multiplierVal.get()
    value = value * MULTIPLIER
    # We must wait for last motor movement be completed
    # delay = X sec
    # value = Y msec
    delay = currentTime - lastSendTime
    if delay < (value / 1000):
        time.sleep((value / 1000) - delay)
        print("waiting for %f sec" % ((value / 1000) - delay))
    #
    # below, we are in the case of tests reverse tiller movement...
    if (currentMode == 'pilote') and flipTiller:
        if direction == 't':
            direction = 'b'
        else:
            direction = 't'
    #
    print("SendToADN : %s %i" % (direction, value))
    q.put((direction, value))
    if tillerDouble:
        if direction == 't':
            direction = 'b'
        else:
            direction = 't'
        time.sleep(value / 1000)
        q.put((direction, value))
    lastSendTime = time.time()


def doCorrection(target, current):
    """
    target : float
    current : float
    return : nothing
    call sendToADN() function with a direction ('b', 't') and an angle
    """
    diff = target - current
    
    MIN_ANGLE = minAngleVal.get()
    MAX_ANGLE = maxAngleVal.get()
    print("%f %f %i" % (MIN_ANGLE, MAX_ANGLE, MULTIPLIER))
    # target and current closed => do nothing
    if abs(diff) <= MIN_ANGLE:
          return(True)

    if abs(diff) < MAX_ANGLE:
        # we are in the case of t and c are usable immediatly,
        # they are in the same zone
        if diff < 0:
            direction = 't' # correction to Tribord
        else:
            direction = 'b' # correction to Badord
        sendToADN(direction, int(abs(diff)))
    else:
        """ either they are too far,
         either they are around the 0 """
        if (360 - abs(diff)) > MAX_ANGLE:
            sendAlert()
            return
        else:
            if diff > 0:
                direction = 't'
                sendToADN(direction, 360 - int(abs(diff)))
            else:
                direction = 'b'
                sendToADN(direction, abs(360 + int(diff)))


# misnamed function : PID is not used to compute the correction
# ... may be in the future...
def piloteAuto():
    time.sleep(1)
    """
    piloteCTL.set_auto_mode(True)
    print("%f -+- %f" % (float(headingTarget),
                         float(headingCurrent)))
    while 1:
        f_headingTarget = float(headingTarget)
        f_headingCurrent = float(headingCurrent)
        piloteCTL.setpoint = f_headingTarget
        correction = piloteCTL(f_headingCurrent)
        print("Correction = %f" % (correction))
        time.sleep(0.95)
    """
    while 1:
        f_headingTarget = float(headingTarget)
        f_headingCurrent = float(headingCurrent)
        print("%f -+- %f" % (f_headingTarget,
                             f_headingCurrent))
        if currentMode == 'pilote':
            doCorrection(f_headingTarget, f_headingCurrent)
            print('-----')
        time.sleep(1)
        if finished:
            return

def changeModeCmd(p):
    # print("updateMode")
    global currentMode
    global headingCurrent
    global headingTarget
    global MULTIPLIER
    global MIN_ANGLE
    global MAX_ANGLE
    bgPilote = "#FFD700"
    bgManual = "#FAFAD2"
    if currentMode == "manual":
        bg = bgPilote
        txt = 'Passer en\nManuel'
        currentMode = 'pilote'
        headingTarget = headingCurrent
        targetHeading.config(text=headingTarget)
        desiredHeading.settiltangle(360 - float(headingTarget) + 90)
        #
        MULTIPLIER = multiplierVal.get()
        MIN_ANGLE = minAngleVal.get()
        MAX_ANGLE = maxAngleVal.get()
    else:
        bg = bgManual
        txt = 'Passer en\nPilote Auto'
        currentMode = 'manual'
    changeMode.config(background=bg,
                      activebackground=bg,
                      text=txt)


def quitPilot():
    global finished
    finished = True
    mainWindow.destroy()
    os.kill(os.getpid(),9)


def getGPSdata_S():
    def getHeading(line):
        """
        Cette fonction, telle qu'elle est, n'est utilisée que dans le cas de la simulation
        où le cap actuel est issus d'un fichier (GggppssX-11)
        En situation réelle, ce sera le résultat de la requête à GPSD
        """
        h = float(line.split('|')[2])
        return "{:06.2f}".format(h)

    global headingCurrent
    global headingTarget
    print('getGPSdata started...')
    while 1:
        if finished:
            return
        gpsDataFile = '../misc_tests/GggppssX-11'
        with open(gpsDataFile) as fp:
            line = fp.readline()
            while line:
                if finished:
                    return
                headingCurrent = getHeading(line)
                currentHeading.config(text=headingCurrent)
                # compassAngle : only for display compass on UI
                compassAngle = 360 - float(headingCurrent) + 90
                actualHeading.settiltangle(compassAngle)
                # print("%f / %f" % (float(headingCurrent), compassAngle))
                time.sleep(2.80)
                line = fp.readline()


def getGPSdata_N():
    def getHeading(report):
        try:
            heading = report['track']
            
            return "{:06.2f}".format(float(str(heading)))
        except:
            return "{:06.2f}".format(600.00)
    
    global headingCurrent
    global headingTarget
    session = gps(mode=WATCH_ENABLE)
    try:
        while True:
            if finished:
                return
            report = session.next()
            if report['class'] == 'DEVICE':
                session.close()
                session = gps(mode=WATCH_ENABLE)
            if report['class'] == 'TPV':
                headingRealTime = getHeading(report)
                # headingCurrent = ....
                # currentHeading.config(text=headingCurrent)
                realTimeHeading.config(text=headingRealTime)
                # compassAngle : only for display compass on UI
                compassAngle = 360 - float(headingCurrent) + 90
                actualHeading.settiltangle(compassAngle)
                # print("%f / %f" % (float(headingCurrent), compassAngle))
    except StopIteration:
        print ("GPSD has terminated")


def updateTargetHeading(op, heading, val):
    """
    op : operation, a = add, s = sub
    heading : string representing a float
    val : value to add to h
    returns: string representation of h + v
    cf https://docs.python.org/fr/3/library/functions.html?highlight=format#format
    pour plus de détails sur le formatage...
    Pour l'envoi de la durée : "{:05d}".format(duration)
    """
    h = float(heading)
    v = float(val)
    if op == 'a':
        newVal = (h - v) % 360.00
    else:
        newVal = (h + v) % 360.00
    return "{:06.2f}".format(newVal)


def flipTillerCommands():
    global flipTiller
    if not flipTiller:
        flipTillerCmds.config(background='#FF0000',
                              activebackground='#0000FF',
                              text='Mvt Barre\nInversé !')
    else:
        flipTillerCmds.config(background='#0000FF',
                              activebackground='#FF0000',
                              text='Inverse\nMvt Barre')
    flipTiller = not flipTiller
    print(flipTiller)

