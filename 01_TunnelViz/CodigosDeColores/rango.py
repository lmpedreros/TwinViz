import cv2
import numpy as np

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Captura el color en el punto donde se hizo clic
        color = frame[y, x]
        color_hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)[0][0]
        #print("Color BGR:", color)
        print("Color HSV:", color_hsv)

# Parámetros de la cámara
nCam = 0
cap = cv2.VideoCapture(nCam)

# Ventana
cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('frame', 30, 30)
cv2.setMouseCallback('frame', mouse_callback)

while True:
    ret, frame = cap.read()

    cv2.imshow('frame', frame)

    # Salir del bucle si se presiona la tecla 'Esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()