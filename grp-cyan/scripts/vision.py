#!/usr/bin/python3
import cv2
import numpy as np


# var. global:
###############

var = 0                 #Compteur de frames
lower_red = np.array([0,50,60])
upper_red = np.array([9,255,255])

# call back:
###############
def isBottle(img):
    h=len(img)
    w=len(img[0])
    sum=0
    r=False
    for ii in range(h):
        for jj in range(w):
            sum=sum+img[ii,jj]//255
    if sum > (h*w)*0.15 :
        r=True
    return r

def getPhi(height, width, image):
    hmax, wmax = image.shape()
    origin = [hmax, wmax//2]
    y = origin[0] - height
    x = origin[1] - width
    return np.arccos(x)

# Script:
###############
cap=cv2.VideoCapture(0) #Ouvre la caméra

while True:
    ret, frame = cap.read() #Lis les images de la caméra
    #frame = cv2.imread('/Users/gabrielharivel/IMT/NU/LARM/Filtre hsv/NukaCola4.jpeg')  #Lis uune image pour tester

    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    image_grey=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    bottle_cascade = cv2.CascadeClassifier('./cascade/cascade.xml')


    detected_bottle = bottle_cascade.detectMultiScale(image_grey, scaleFactor=1.10, minNeighbors=3)

    for (column, row, width, height) in detected_bottle:
        crop_image = image_hsv[row:row+height, column:column+width] #crop les detections
        filtre_hsv = cv2.inRange(crop_image, lower_red, upper_red)  #Filtrage des couleurs sur les images croppé
        
        if isBottle(filtre_hsv):
            cv2.rectangle(frame ,( column, row) , (column + width, row + height) , (0, 255, 0) , 2) #Met un rectangle vert sur les bouteilles
            middle_position = ( column+ width//2,row+ height//2)
            cv2.rectangle(frame ,(middle_position[0] , middle_position[1]) , (middle_position[0] +3 , middle_position[1] + 3) , (0, 255, 0) , 2)
            print(getPhi(middle_position[1], middle_position[0], frame))
        else:
            cv2.rectangle(frame ,( column, row) , (column + width, row + height) , (0, 0, 255) , 2) #Met un rectangle rouge sur les faux positifs
        

    
    
    cv2.imshow('Filtre', frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break