#!../bin/python3

from pdb import set_trace as st
from tkinter import *
from functools import partial
import turtle
import time
import threading
import queue
import sys

# debugMode = True
debugMode = False

started = False
currentMode = str('manual')

headingCurrent = 0.0
headingTarget = 0.0

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


if debugMode:
    pidp = Spinbox(mainWindow)
    pidi = Spinbox(mainWindow)
    pidd = Spinbox(mainWindow)
    pidpVal = DoubleVar(mainWindow)
    pidiVal = DoubleVar(mainWindow)
    piddVal = DoubleVar(mainWindow)

q = queue.Queue()


def baTri(params):
    """
    Change direction : babord / Tribord
    If in pilote mode : use of PID controler...
        display the new target heading in UI : the new target heading depends of
        the current target and the command received in params
        test if actuator is moving
            if not moving : send to ADN command for the actuator
            if moving : wait for end of actuator move then send command to ADN
    If in manual mode :
        test if actuator is moving :
            if moving : wait for end of actuator move then send command to ADN to
                change the tiller agle
            if not moving : send command to change the tiller angle
    :params: params is a tuple ('b|t', 1|5)
        b = babord
        t = tribord
        1 = 1°
        5 = 5°
    !!! NB : the global variable headingTarget is modified !!!
    """
    # print(params)
    global headingTarget
    # global targetHeading
    if currentMode == 'pilote':
        if params[0] == 't':
            newTarget = updateTargetHeading('a', headingTarget, params[1])
        else:
            newTarget = updateTargetHeading('s', headingTarget, params[1])
        headingTarget = newTarget
        targetHeading.config(text=headingTarget)
        desiredHeading.settiltangle(float(headingTarget) + 90)
        # -- test if actuator is moving
        # when not moving, send command to ADN
        # the command should be sommething similar to the params of this function
        # q.put('
        # q.put(('c', headingTarget))
    else:
        # -- test if actuator is moving
        # when not moving, send command to ADN
        pass
        # q.put((params[0], params[1]))

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
        desiredHeading.settiltangle(float(headingTarget) + 90)
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

def startStop(but):
    global started
    if not started:
        but.config(background='#9932CC',
                   activebackground='#9932CC',
                   text='Stop pilote!')
        started = True
        manageGPS = threading.Thread(target=getGPSdata,
                             name='manageGPS',
                             daemon=True)
        computeGPSdata = threading.Thread(target=manageQueue,
                                          name='computeGPSdata',
                                          daemon=True)
        manageGPS.start()
        computeGPSdata.start()
        print('started...')
    else:
        started = False
        if currentMode != "manual":
            changeModeCmd(None)
        but.config(background='#FF8C00',
                   activebackground='#FF8C00',
                   text='Start...')

def quitPilot():
    sys.exit()

def getHeading(line):
    """
    Cette fonction, telle qu'elle est, n'est utilisée que dans le cas de la similation
    où le cap actuel est issus d'un fichier (GggppssX-11)
    En situation réelle, ce sera le résultat de la requête à GPSD
    """
    h = float(line.split('|')[2])
    return "{:06.2f}".format(h)

def getGPSdata():
    global headingCurrent
    global headingTarget
    print('getGPSdata started...')
    n = 0
    gpsDataFile = '../misc_tests/GggppssX-11'
    with open(gpsDataFile) as fp:
        line = fp.readline()
        while line:
            if not started:
                break
            headingCurrent = getHeading(line)
            currentHeading.config(text=headingCurrent)
            actualHeading.settiltangle(float(headingCurrent) + 90)
            # q.put(('g', headingCurrent))
            lheading = [len(headingCurrent)] + [ord(c) for c in list(headingCurrent)]
            time.sleep(1)
            line = fp.readline()
            n += 1
            if n > 25:
                break

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
