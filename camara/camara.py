#### En el menu de la esquina superiro izq entrar a 'Preferences' ####
#### luego entrar a 'Raspberry Pi Configuration'                  ####
#### seleccionar el tab de 'Interfaces tab' y y colocar 'Enable'
#### en componente 'Camera'



from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.stop_preview()
