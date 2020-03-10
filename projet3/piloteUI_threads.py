#!../bin/python3

"""
No more used !!!
Those functions are in piloteUIfunctions.py
"""

from pdb import set_trace as st
from tkinter import *
# from tkinter.ttk import *
from functools import partial
import time
import threading
import queue
import sys

currentMode = 'manual'
q = queue.Queue()

def changeModeCmd():
    print("updateMode")
    bgPilote = "#FFD700"
    bgManual = "#FAFAD2"
    global currentMode
    if currentMode == "manual":
        bg = bgPilote
        txt = 'Pilote Auto'
        currentMode = 'pilote'
        q.put(currentMode)
    else:
        bg = bgManual
        txt = 'Manuel'
        currentMode = 'manual'
        q.put(currentMode)
    changeMode.config(background=bg,
                      activebackground=bg,
                      text=txt)

def babord5Cmd():
    print('babord5')
    q.put(('bab5','bab5'))

def babord1Cmd():
    print('babord1')
    q.put('bab1')

def tribord1Cmd():
    print('tribord1')
    q.put('trib1')

def tribord5Cmd():
    print('tribord5')
    q.put('trib5')


def configButtons():
    buttons = []
    global babord5
    babord5 = Button(mainWindow)
    buttons.append(babord5)
    global babord1
    babord1 = Button(mainWindow)
    buttons.append(babord1)
    global changeMode
    changeMode = Button(mainWindow)
    buttons.append(changeMode)
    global tribord1
    tribord1 = Button(mainWindow)
    buttons.append(tribord1)
    global tribord5
    tribord5 = Button(mainWindow)
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
    cmds = [babord5Cmd, babord1Cmd,
            changeModeCmd,
            tribord1Cmd, tribord5Cmd]
            
    i = 0
    for button in buttons:
        # print(button)
        button.config(text=texts[i],
                      width=widths[i],
                      height=heights[i],
                      command=partial(cmds[i]),
                      background=bgs[i],
                      activebackground=bgs[i],
                      )
        button.grid(column=columns[i], row=1,
                    padx=xpads[i],
                    pady=ypads[i],)
        i += 1
    
def initUI():
    # global userInterface
    print(userInterface.name)
    global mainWindow
    mainWindow = Tk() # Création de la fenêtre racine
    mainWindow.title('Pilote Automatique')
    mainWindow.config(background='#1E90FF',
                )
    mainWindow.geometry('580x150+30+30')
    global currentHeading
    currentHeading = Label(mainWindow,
                          text="current Heading")
    currentHeading.grid(column=2, row=0)
    global targetHeading
    targetHeading = Label(mainWindow,
                          text="target Heading",
                          pady=2)
    targetHeading.grid(column=2, row=2)
    configButtons()

    mainWindow.mainloop() # Lancement de la boucle principale

def getHeading(line):
    h = float(line.split('|')[2])
    return "{:06}".format(h)

def getGPSdata():
    global currentHeading
    global q
    n = 0
    gpsDataFile = '../misc_tests/GggppssX-11'
    with open(gpsDataFile) as fp:
        line = fp.readline()
        while line:
            heading = getHeading(line)
            q.put(('gsp', heading))
            currentHeading.config(text=heading)
            lheading = [len(heading)] + [ord(c) for c in list(heading)]
            time.sleep(1)
            line = fp.readline()
            n += 1
            if n > 15:
                break
    

def manageALL():
    global q
    i = 0
    while 1:
        msg = q.get()
        print(msg)
        if msg == 'trib5':
            print('Sortie....!!!')
            # sys.exit()
            return
        time.sleep(1)
        

# threading.Thread(target=manageGPS)
userInterface = threading.Thread(target=initUI,
                                 name='UserInterface',
                                 daemon=True)
userInterface.start()
manageGPS = threading.Thread(target=getGPSdata,
                             name='manageGPS',
                             daemon=True)
manageGPS.start()

manageALL()
time.sleep(1)

print('et il se passe quoi maintenant...?')
