#!../bin/python3

from pdb import set_trace as st
from tkinter import *

from functools import partial
import time
import threading
import queue
from math import radians, cos, sin
import sys

from piloteUIfunctions import *


addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

def commandsButtons():
    buttons = []
    buttons.append(babord5)
    buttons.append(babord1)    
    buttons.append(changeMode)
    buttons.append(tribord1)
    buttons.append(tribord5)
    
    columns = [0, 1, 2, 3, 4]
    xpads = [3, 3, 5, 3, 3]
    ypads = [0, 0, 5, 0, 0]
    widths = [10, 10, 10, 10, 10]
    heights = [2, 2, 4, 2, 2]
    texts = ["Babord 5°", "Babord 1°",
             "Passer en\nPilote Auto",
             "Tribord 1°", "Tribord 5°"
             ]
    bgs = ["#FF0000", "#FF4500",
           "#FAFAD2",
           "#d6ff97", "#00ff00"]

    cmds = [baTri, baTri,
            changeModeCmd,
            baTri, baTri]
    params = [('b', 5), ('b', 1),
              (None, None),
              ('t', 1), ('t', 5)]
            
    i = 0
    for button in buttons:
        # print(button)
        button.config(text=texts[i],
                      width=widths[i],
                      height=heights[i],
                      command=partial(cmds[i], params[i]),
                      background=bgs[i],
                      activebackground=bgs[i],
                      )
        button.grid(column=columns[i], row=1,
                    padx=xpads[i],
                    pady=ypads[i],)
        i += 1


def headingDisplays():
    # labels for heading display
    currentHeading.grid(column=2, row=0)
    targetHeading.grid(column=2, row=2)

def miscButtons():
    # misc buttons
    """
    startGPS_button = Button(mainWindow)
    startGPS_button.config(text='Start GPS...',
                        width=10,
                        height=2,
                        pady=3,
                        background='#FF8C00',
                        activebackground='#FF8C00',
                        foreground='#FFFFFF',
                        command=partial(startStopGPS, startGPS_button),
                        )
    startGPS_button.grid(column=2,
                      row=3)
    """
    # button for double tiller movement : to change the heading
    # we must change the tiller angle and to restore it to its firts
    # position. Only use in pilote mode !
    """
    tillerDouble_button = Button(mainWindow)
    tillerDouble_button.config(text='Double Tiller\nmovement',
                        width=10,
                        height=2,
                        pady=3,
                        background='#FF8C00',
                        activebackground='#FF8C00',
                        foreground='#FFFFFF',
                        command=partial(tillerDoubleSwitch, tillerDouble_button),
                        )
    tillerDouble_button.grid(column=2,
                             row=3)
    """
    w = '#FFFFFF'
    b = '#000000'
    quitButton.config(text='Quit !!',
                      background=w,
                      foreground=b,
                      activebackground=b,
                      activeforeground=w,
                      command=partial(quitPilot))
    quitButton.grid(column=3, row=3)


def PIDTunningButtons():
    global pidpVal
    global pidiVal
    global piddVal
    inc = 5
    pidpLab = Label(mainWindow,
                    text='P param')
    pidpLab.grid(column=0, row=6,
                 pady=5)
    pidpVal = DoubleVar(value=2)
    pidp.config(text='P pid param',
                textvariable=pidpVal,
                from_=0,
                to=100,
                increment=inc,
                width=3,
                )
    
    pidp.grid(column=0, row=7)
    pidiLab = Label(mainWindow,
                    text='I param')
    pidiLab.grid(column=1, row=6)
    pidi.config(text='I pid param',
                textvariable=pidiVal,
                from_=0,
                to=100,
                increment=inc,
                width=3,
                )
    pidi.grid(column=1, row=7)
    piddLab = Label(mainWindow,
                    text='D param')
    piddLab.grid(column=2, row=6)
    pidd.config(text='D pid param',
                textvariable=piddVal,
                from_=0,
                to=100,
                increment=inc,
                width=3,
                )
    pidd.grid(column=2, row=7)
    mainWindow.geometry('580x400+40+30')


def tuningButtons():
    global minAngleVal
    global maxAngleVal
    global multiplierVal
    minAngleVal.set(1)
    maxAngleVal.set(40)
    multiplierVal.set(50)
    minALab = Label(mainWindow,
                    text='min Angle')
    minALab.grid(column=0, row=4,
                 pady=5)
    minAngle.config(textvariable=minAngleVal,
                    from_=0,
                    to=20,
                    increment=1,
                    width=3)
    minAngle.grid(column=0, row=5)
    # pass
    maxALab = Label(mainWindow,
                    text='MAX Angle')
    maxALab.grid(column=1, row=4,
                 pady=5)
    maxAngle.config(textvariable=maxAngleVal,
                    from_=1,
                    to=45,
                    increment=1,
                    width=3)
    maxAngle.grid(column=1, row=5)
    # pass
    multiplierLab = Label(mainWindow,
                    text='Multiplier')
    multiplierLab.grid(column=2, row=4,
                       pady=5)
    multiplier.config(textvariable=multiplierVal,
                    from_=1,
                    to=999,
                    increment=1,
                    width=3)
    multiplier.grid(column=2, row=5)
    
    
    

def compass():
    """
    https://docs.python.org/3/library/turtle.html
    https://docs.python.org/fr/3/library/turtle.html
    https://johanneskinzig.de/index.php/systems-engineering/11-reading-and-visualising-sensor-data-compass-heading
    """
    compassDrawCanvas.config(background="white",
                       width=100,
                       height=100,
                       )
    compassDrawCanvas.grid(column=0, row=3)
    headingScreen.screensize(100, 100)

    desiredHeading.penup()
    desiredHeading.setposition(50, -50)
    desiredHeading.shape("triangle")
    desiredHeading.shapesize(0.4, 6)
    desiredHeading.fillcolor("red")
    desiredHeading.settiltangle(90)

    actualHeading.penup()
    actualHeading.setposition(50, -50)
    actualHeading.shape("triangle")
    actualHeading.shapesize(0.1, 4)
    actualHeading.fillcolor("blue")
    actualHeading.settiltangle(90)


def initUI():
    # global mainWindow
    # mainWindow = Tk() # Création de la fenêtre racine
    mainWindow.title('Pilote Automatique')
    mainWindow.config(background='#1E90FF')
    mainWindow.geometry('580x300+40+30')

    headingDisplays()
    # main command buttons
    commandsButtons()
    miscButtons()
    compass()
    if PIDTunigMode:
        PIDTunningButtons()
    if tuningMode:
        tuningButtons()

    
def manageQueue():
    print('manageQueue() Started...')
    global q
    i = 0
    while 1:
        if finished:
            return
        msg = q.get()
        steering = ord(msg[0])
        angle = msg[1]
        # duration = angle * 50
        duration = angle
        x_duration = "{:05}".format(duration)
        duration = [ord(d) for d in x_duration]
        print ('.... %s' % (str(msg)))
        bus.write_block_data(addr, steering, duration)
        

