#!../bin/python3

"""
Les tuples envoyés dans la file q (Queue) :
('l', val)
'l' = type de donnée
    g = donnée GPS actuelle ; val = angle
    c = consigne GPS ; val = angle
    m = mode manuel ; val = m (manuel) ou p (pilote auto)
    b = babord ; val = 1 ou 5 degrés
    t = tribord ; val = 1 ou 5 degrés
Les données dans la file q sont transmises à ADN par la méthode write_i2c_block_data
    les lettres ci-dessus (g, c, ...) sont transmises dans le champ cmd
    les valeurs sont transmises sous forme d'un tableau de 6 caractères dans le champ val
"""

from pdb import set_trace as st
import time
import threading
import queue
import sys

import piloteUI

debugMode = 1
currentMode = str('manual')
q = queue.Queue()
started = False
headingCurrent = 0.0
headingTarget = 0.0


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
        # sys.exit()


def initUI():
    # global mainWindow
    # mainWindow = Tk() # Création de la fenêtre racine
    mainWindow.title('Pilote Automatique')
    mainWindow.config(background='#1E90FF')
    mainWindow.geometry('580x200+40+30')

    # labels for heading display
    currentHeading.grid(column=2, row=0)
    targetHeading.grid(column=2, row=2)

    # mains command buttons
    configButtons()

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
    if debugMode:
        debugButtons()
    mainWindow.mainloop() # Lancement de la boucle principale


def manageQueue():
    global q
    global started
    i = 0
    while started:
        msg = q.get()
        print(msg)
        

def __main__():
    initUI()
    mainWindow.mainloop() # Lancement de la boucle principale

time.sleep(1)

print('et il se passe quoi maintenant...?')
