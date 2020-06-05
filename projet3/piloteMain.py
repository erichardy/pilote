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
    # userInterface : User interface with automatic pilot.
    # Send commands to ADN if in manual mode,
    # or switch to pilote mode (see pilotePilote thread)
    # and modify target Heading if desired
    userInterface = threading.Thread(target=initUI,
                                     name='UserInterface',
                                     daemon=False)
    userInterface.start()

    # manageQ : this thread reads messages from the queue and sends
    # commands to ADN. A correction is applied if 'b' (BT_CORRECTION)
    # no global variable modified
    manageQ = threading.Thread(target=manageQueue,
                                     name='manage_Queue',
                                     daemon=False)
    manageQ.start()

    # manageGPS : get data from GPS,
    # updated variables : headingCurrent, headingTarget
    # updated UI : currentHeading (curent heading display, number)
    #              actualHeading (compass, graphic)
    manageGPS = threading.Thread(target=getGPSdata,
                             name='manageGPS',
                             daemon=False,
                             )
    manageGPS.start()

    # 
    pilotePilote = threading.Thread(target=piloteAuto,
                                    name='piloteAuto',
                                    daemon=False)
    pilotePilote.start()

    mainWindow.mainloop() # Lancement de la boucle principale
    print('Main window closed !!!')
    # st()


__main__()

