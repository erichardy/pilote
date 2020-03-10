
=======================
Documentation technique
=======================

TODO
----

* connexion entre le ACS712 et Rpi
   lecture des données retournées par l'ACS712 pour déterminer que le moteur est (ou non) en mouvement

* mise en oeuvre du controleur PID



piloteMain.py
-------------

Entrée de l'application "pilote" : ``piloteMain.py``

* initialisation de l'interface graphique avec initUI() (définie dans piloteUI.py)

* activation de l'interface par ``mainloop()``

import de ``piloteUI.py``

piloteUI.py
-----------

Mise en place de l'interface graphique : piloteUI.py

import de ``piloteUIfunctions.py``

Mode débug :
activé par la variable globale ``debugMode`` (True|False) déclarée dans ``piloteUIFunctions.py``

Ce mode permet d'afficher et de gérer les valeurs p, i et d du controleur PID


piloteUIfunctions.py
--------------------

Actions déclenchées par l'interface graphique

``baTri()``
   changements de direction : dans le mode **pilote auto**, la main est passée au contrôleur PID. Cependant, un changement
   de cap reste possible et le controleur PID doit être réinitialisé...(?)

``changeModeCmd()``
   passage du mode manuel au mode pilote et vice-versa :

      * mise à jour de l'interface graphique

      * modification des variables globales ``currentMode`` ``headingCurrent`` et ``headingTarget``

``startStop()``
   démarage/arrêt du pilote

   * démarage/arrêt de l'acquisition du cap à partir de ``gpsd``

   * mise à jour de l'interface graphique


``getGPSdata()``
   obtient le cap de ``gpsd``
   
   * met à jour la valeur de ``currentHeading``

   * la valeur retournée est utilisée par le controleur PID comme étant la **mesure**


``updateTargetHeading()``
   est utilisée par la fonction ``baTri`` pour la gestion du compas et la mise à jour des valeurs dans l'interface graphique

