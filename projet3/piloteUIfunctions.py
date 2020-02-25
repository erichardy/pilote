#!../bin/python3

from pdb import set_trace as st
from tkinter import *
from functools import partial
import time
import threading
import queue
import sys

debugMode = True
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
compassDraw = Canvas(mainWindow)

if debugMode:
    pidp = Spinbox(mainWindow)
    pidi = Spinbox(mainWindow)
    pidd = Spinbox(mainWindow)
    pidpVal = DoubleVar(mainWindow)
    pidiVal = DoubleVar(mainWindow)
    piddVal = DoubleVar(mainWindow)

q = queue.Queue()


def baTri(params):
    print(params)
    global headingTarget
    # global targetHeading
    if currentMode == 'pilote':
        if params[0] == 't':
            newTarget = updateTargetHeading('a', headingTarget, params[1])
        else:
            newTarget = updateTargetHeading('s', headingTarget, params[1])
        headingTarget = newTarget
        targetHeading.config(text=headingTarget)
        q.put(('c', headingTarget))
    else:
        q.put((params[0], params[1]))

def changeModeCmd(p):
    # print("updateMode")
    global currentMode
    global headingCurrent
    global headingTarget
    bgPilote = "#FFD700"
    bgManual = "#FAFAD2"
    if currentMode == "manual":
        bg = bgPilote
        txt = 'Pilote Auto'
        currentMode = 'pilote'
        headingTarget = headingCurrent
        targetHeading.config(text=headingTarget)
        q.put(('m', 'p'))
        q.put(('c', headingTarget))
    else:
        bg = bgManual
        txt = 'Manuel'
        currentMode = 'manual'
        q.put(('m', 'm'))
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
        but.config(background='#FF8C00',
                   activebackground='#FF8C00',
                   text='Start...')

def quitPilot():
    sys.exit()

def getHeading(line):
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
            q.put(('g', headingCurrent))
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
    """
    h = float(heading)
    v = float(val)
    if op == 'a':
        newVal = (h + v) % 360.00
    else:
        newVal = (h - v) % 360.00
    return "{:06.2f}".format(newVal)


def manageQueue():
    global q
    global started
    i = 0
    while started:
        msg = q.get()
        print(msg)
