import numpy as np
import cv2
import time
import math

global nClick

nCam = 0
cap = cv2.VideoCapture(nCam) 	

color1_hsv = np.array([0,0,0])

if cap.isOpened():
	cap.open(nCam)	

def _mouseEvent(event, x, y, flags, param):
	global nClick
	global color1_hsv

	
	if event == cv2.EVENT_LBUTTONDOWN:
		hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		color1_hsv = hsv_frame[y,x]
		print("Color 1: ",color1_hsv )
		print("Eje x: ", x)
		print("Eje y: ",y)


cv2.namedWindow('frame',  cv2.WINDOW_AUTOSIZE )	
cv2.moveWindow('frame', 30, 100)

cv2.namedWindow('frame2')
cv2.moveWindow('frame2', 700, 100)

#lower_color = np.array([155,80,80])
#upper_color = np.array([175,255,255])
lower_color = np.array([155,80,80])
upper_color = np.array([175,200,200])

cv2.setMouseCallback('frame',_mouseEvent)
			
while(True):
	ret, frame = cap.read()

	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask_color = cv2.inRange(hsv_frame, lower_color, upper_color)
	hsv_frame_mask = cv2.bitwise_and(frame,frame, mask= mask_color)
	
	cv2.imshow('frame',frame)
	cv2.imshow('frame2',hsv_frame_mask)
	cv2.imshow('frame3',mask_color)


	if cv2.waitKey(1) & 0xFF == 27:
		break


cap.release()
cv2.destroyAllWindows()