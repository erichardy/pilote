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

from piloteUI import *


def __main__():
    initUI()
    mainWindow.mainloop() # Lancement de la boucle principale

__main__()
