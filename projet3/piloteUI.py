#!../bin/python3

from pdb import set_trace as st
from tkinter import *
from functools import partial

currentMode = 'manual'

def changeModeCmd():
    print("updateMode")
    bgPilote = "#FFD700"
    bgManual = "#FAFAD2"
    global currentMode
    if currentMode == "manual":
        bg = bgPilote
        txt = 'Pilote Auto'
        currentMode = 'pilote'
    else:
        bg = bgManual
        txt = 'Manuel'
        currentMode = 'manual'
    changeMode.config(background=bg,
                      activebackground=bg,
                      text=txt)

def babord5Cmd():
    print('babord5')

def babord1Cmd():
    print('babord1')

def tribord1Cmd():
    print('tribord1')

def tribord5Cmd():
    print('tribord5')


def configButtons():
    buttons = []
    global babord5
    babord5 = Button(root)
    buttons.append(babord5)
    global babord1
    babord1 = Button(root)
    buttons.append(babord1)
    global changeMode
    changeMode = Button(root)
    buttons.append(changeMode)
    global tribord1
    tribord1 = Button(root)
    buttons.append(tribord1)
    global tribord5
    tribord5 = Button(root)
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
    



root = Tk() # Création de la fenêtre racine
root.config(background='#1E90FF')
root.geometry('580x150+30+30')

currentHeading = Label(root,
                      text="current Heading")
currentHeading.grid(column=2, row=0)
targetHeading = Label(root,
                      text="target Heading")
targetHeading.grid(column=2, row=2)
configButtons()

root.mainloop() # Lancement de la boucle principale


