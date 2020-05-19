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
Les données dans la file q sont transmises à ADN par la
méthode write_i2c_block_data
    les lettres ci-dessus (g, c, ...) sont transmises dans le champ cmd
    les valeurs sont transmises sous forme d'un tableau de 6 caractères
    dans le champ val
NB: étant donné que ADN ne sera plus utilisé que comme transmetteur des
commandes au vérin, il n'y aura plus que ('b', 1), ('b', 5), ('t', 1) ('t', 5)
"""

from pdb import set_trace as st
import time
import threading
import queue
import sys

from piloteUI import *



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

