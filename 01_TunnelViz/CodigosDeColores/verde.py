import numpy as np
import cv2

global nClick

nCam = 0
cap = cv2.VideoCapture(nCam)

color1_hsv = np.array([0, 0, 0])

if cap.isOpened():
    cap.open(nCam)

def _mouseEvent(event, x, y, flags, param):
    global nClick
    global color1_hsv

    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color1_hsv = hsv_frame[y, x]
        print("Color 1: ", color1_hsv)
        print("Eje x: ", x)
        print("Eje y: ", y)

cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('frame', 30, 100)

cv2.namedWindow('frame2')
cv2.moveWindow('frame2', 700, 100)

lower_color = np.array([35, 50, 50])  # Valor HSV para verde
upper_color = np.array([85, 255, 255])  # Valor HSV para verde

cv2.setMouseCallback('frame', _mouseEvent)

while True:
    ret, frame = cap.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_color = cv2.inRange(hsv_frame, lower_color, upper_color)
    hsv_frame_mask = cv2.bitwise_and(frame, frame, mask=mask_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Dibujar un círculo alrededor de cada contorno verde
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    cv2.imshow('frame2', hsv_frame_mask)
    cv2.imshow('frame3', mask_color)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()