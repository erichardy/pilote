
from gpiozero import Button
from signal import pause

button = Button(17)

def aff():
    print("Bouton pressé")

def aff2():
    print("Bouton relaché")

button.when_pressed = aff
button.when_released = aff2

pause()

