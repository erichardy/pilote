#!../bin/python3


from pdb import set_trace as st
import time
import threading
import queue
import sys

from piloteUI import *


if args.s:
    getGPSdata = getGPSdata_S
else:
    getGPSdata = getGPSdata_N


def __main__():
    
    userInterface = threading.Thread(target=initUI,
                                     name='UserInterface',
                                     daemon=False)
    userInterface.start()

    manageQ = threading.Thread(target=manageQueue,
                                     name='manage_Queue',
                                     daemon=False)
    manageQ.start()
    manageGPS = threading.Thread(target=getGPSdata,
                             name='manageGPS',
                             daemon=False,
                             )
    manageGPS.start()
    pilotePilote = threading.Thread(target=pilotePID,
                                    name='pilotePID',
                                    daemon=False)
    pilotePilote.start()

    mainWindow.mainloop() # Lancement de la boucle principale
    print('Main window closed !!!')
    # st()


__main__()

