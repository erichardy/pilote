#!../bin/python3

from pdb import set_trace as st
from tkinter import *
from functools import partial

def updateMode():
    changeMode.config(background="#FF0000",
                      activebackground="#FF0000")
    st()

currentMode = "manual"




root = Tk() # Création de la fenêtre racine

changeMode = Button(root,
                    text="Manuel",
                    command=partial(updateMode))
changeMode.config(background="#00FF00",
                  activebackground="#00FF00",
                  padx=5, pady=5,
                  width=10,
                  height=3)
changeMode.grid(column=3, row=1)

babord1 = Button(root,
                 text="Babord 1°"
                 )
babord1.config(padx=10, pady=5,
               width=10)
babord1.grid(column=2, row=1)

babord5 = Button(root,
                 text="Babord 5°",
                 padx=5, pady=5,
                 )
babord5.grid(column=1, row=1)

tribord1 = Button(root,
                 text="Tribord 1°",
                 padx=5, pady=5,
                 )
tribord1.grid(column=4, row=1)
tribord5 = Button(root,
                 text="Tribord 5°",
                 padx=5, pady=5,
                 )
tribord5.grid(column=5, row=1)

currentHeading = Label(root,
                      text="current Heading")
currentHeading.grid(column=3, row=0)


root.mainloop() # Lancement de la boucle principale


