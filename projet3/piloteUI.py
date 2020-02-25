#!../bin/python3

from pdb import set_trace as st
from tkinter import *
from functools import partial
import time
import threading
import queue
import sys

from piloteUIfunctions import *


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
             "Manuel",
             "Tribord 1°", "Tribord 5°"
             ]
    bgs = ["#FF0000", "#FF4500",
           "#FAFAD2",
           "#d6ff97", "#00ff00"]
    """
    cmds = [babord5Cmd, babord1Cmd,
            changeModeCmd,
            tribord1Cmd, tribord5Cmd]
    """
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
    start_button = Button(mainWindow)
    start_button.config(text='Start...',
                        width=10,
                        height=2,
                        pady=3,
                        background='#FF8C00',
                        activebackground='#FF8C00',
                        foreground='#FFFFFF',
                        command=partial(startStop, start_button),
                        )
    start_button.grid(column=2,
                      row=3)
    w = '#FFFFFF'
    b = '#000000'
    quitButton.config(text='Quit !!',
                      background=w,
                      foreground=b,
                      activebackground=b,
                      activeforeground=w,
                      command=partial(quitPilot))
    quitButton.grid(column=3, row=3)

def debugButtons():
    pass
    
def initUI():
    # global mainWindow
    # mainWindow = Tk() # Création de la fenêtre racine
    mainWindow.title('Pilote Automatique')
    mainWindow.config(background='#1E90FF')
    mainWindow.geometry('580x200+40+30')

    headingDisplays()
    # mains command buttons
    commandsButtons()
    miscButtons()
    
    if debugMode:
        debugButtons()

