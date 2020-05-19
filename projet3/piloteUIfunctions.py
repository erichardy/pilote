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
from smbus import SMBus
sys.path.append('/home/pi/PILOTE/pilote/lib/python3.7/site-packages')
from simple_pid import PID
from gps import WATCH_ENABLE, gps

# debugMode = True
debugMode = False

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

# pilote control
piloteCTL = PID(1, 1, 1, 0.0)

MIN_ANGLE = 1
MAX_ANGLE = 40

if debugMode:
    pidp = Spinbox(mainWindow)
    pidi = Spinbox(mainWindow)
    pidd = Spinbox(mainWindow)
    pidpVal = DoubleVar(mainWindow)
    pidiVal = DoubleVar(mainWindow)
    piddVal = DoubleVar(mainWindow)

q = queue.Queue()


def tillerDoubleSwitch(but):
    global tillerDouble
    tillerDouble = not tillerDouble
    if not tillerDouble:
        but.config(background='#9932CC',
                   activebackground='#9932CC',
                   text='Single Tiller\nmovement')
    else:
        but.config(background='#FF8C00',
                   activebackground='#FF8C00',
                   text='Double Tiller\nmovement')
    

def baTri(params):
    """
    Change direction : babord / Tribord
    If in pilote mode : use of PID controler...
        display the new target heading in UI : the new target heading depends of
        the current target and the command received in params,
        and modify the target heading : headingTarget variable
        The PID controler must use this new parameter
    If in manual mode : send command to change the tiller angle
    :params: params is a tuple ('b|t', 1|5)
        b = babord
        t = tribord
        1 = 1°
        5 = 5°
    !!! NB : the global variable headingTarget is updated !!!
    """
    # print(params)
    global headingTarget
    # global targetHeading
    if currentMode == 'pilote':
        if params[0] == 'b':
            newTarget = updateTargetHeading('a', headingTarget, params[1])
        else:
            newTarget = updateTargetHeading('s', headingTarget, params[1])
        headingTarget = newTarget
        targetHeading.config(text=headingTarget)
        desiredHeading.settiltangle(360 - float(headingTarget) + 90)
        print('Heading modified !')
        
        # q.put('
        # q.put(('c', headingTarget))
    else:
        # if not in pilote mode, interract directly with actuator
        q.put((params[0], params[1]))


def sendAlert():
    print('ALERT ALERT ALERT !!!!!!')

def sendToADN(direction, value):
    """
    the value must be adapted with the duration of the actuator movement,
    may be more than a multiplier...???
    """
    # multiplier = XXX # to be defined ???
    multiplier = 1
    print("%s %i" % (direction, value * multiplier))
    if currentMode == 'pilote':
        q.put((direction, value * multiplier))
    if tillerDouble:
        if direction == 't':
            direction = 'b'
        else:
            direction = 't'
        q.put((direction, value * multiplier))



def getCorrection(target, current):
    """
    target : float
    current : float
    return : a direction ('b' or 't') and a value to be sent to ADN
    """
    diff = target - current
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
            
          

def pilotePID():
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
        getCorrection(f_headingTarget, f_headingCurrent)
        print('-----')
        time.sleep(1)
        if finished:
            return

def changeModeCmd(p):
    # print("updateMode")
    global currentMode
    global headingCurrent
    global headingTarget
    bgPilote = "#FFD700"
    bgManual = "#FAFAD2"
    if currentMode == "manual":
        bg = bgPilote
        txt = 'Passer en\nManuel'
        currentMode = 'pilote'
        headingTarget = headingCurrent
        targetHeading.config(text=headingTarget)
        desiredHeading.settiltangle(360 - float(headingTarget) + 90)
        
        # q.put(('m', 'p'))
        # q.put(('c', headingTarget))
    else:
        bg = bgManual
        txt = 'Passer en\nPilote Auto'
        currentMode = 'manual'
        # q.put(('m', 'm'))
    changeMode.config(background=bg,
                      activebackground=bg,
                      text=txt)

def startStopGPS(but):
    global GPSstarted
    if not GPSstarted:
        but.config(background='#9932CC',
                   activebackground='#9932CC',
                   text='Stop GPS!')
        GPSstarted = True
        startGPS.set()
        """
        manageGPS = threading.Thread(target=getGPSdata,
                             name='manageGPS',
                             daemon=True)
        """
        # manageGPS.start()
        print('started...')
    else:
        GPSstarted = False
        startGPS.clear()
        if currentMode != "manual":
            changeModeCmd(None)
        but.config(background='#FF8C00',
                   activebackground='#FF8C00',
                   text='Start GPS...')
        print('GPS Stopped .')


def quitPilot():
    global finished
    finished = True
    mainWindow.destroy()
    os.kill(os.getpid(),9)

def _XgetHeading(line):
    """
    Cette fonction, telle qu'elle est, n'est utilisée que dans le cas de la simulation
    où le cap actuel est issus d'un fichier (GggppssX-11)
    En situation réelle, ce sera le résultat de la requête à GPSD
    """
    h = float(line.split('|')[2])
    return "{:06.2f}".format(h)

def _XgetGPSdata():
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


def getHeading(report):
    try:
        heading = report['track']
        
        return "{:06.2f}".format(float(str(heading)))
    except:
        return "{:06.2f}".format(600.00)


def getGPSdata():
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
                headingCurrent = getHeading(report)
                currentHeading.config(text=headingCurrent)
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


def manageQueue():
    global q
    global started
    i = 0
    while started:
        msg = q.get()
        # print(msg)
