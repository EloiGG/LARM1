#!/usr/bin/python3
import cv2,tf
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int16MultiArray
from geometry_msgs.msg import PoseStamped
import numpy as np

# var. global:
###############
rospy.init_node('detector', anonymous=True)
bridge = CvBridge()
var = 0                             #Compteur de frames
bottle = []
lower_red = np.array([0,50,60])
upper_red = np.array([9,255,255])

# call back:
###############

def detection(data):
    global lower_red
    global upper_red
    global bottle
    pixel_mid = 0
    distance=0

    # On convertit l'image ros en image cv2 de façon sûre
    #try:
        #cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
   # except CvBridgeError:
        #rospy.logerr("CvBridge Error") 
    cv_image=data
    # On cherche les bouteilles grâce à la méthode de Haar
    image_hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    image_grey=cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    bottle_cascade = cv2.CascadeClassifier('./cascade/cascade.xml')

    detected_bottle = bottle_cascade.detectMultiScale(image_grey, scaleFactor=1.10, minNeighbors=3)

    #Pour chaque bouteilles détectées, on va appliquer un filtre HSV sur la couleur rouge pour enlever les faux positifs
    for (column, row, width, height) in detected_bottle:
        crop_image = image_hsv[row:row+height, column:column+width] # On rogne les détections les detections
        filtre_hsv = cv2.inRange(crop_image, lower_red, upper_red)  # Filtrage des couleurs sur les images croppé
        
        if isBottle(filtre_hsv):
            #Met un rectangle vert sur les bouteilles
            cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 255, 0) , 2) 
            bottle.append(np.array(pixel_mid, distance))
        else:
            #Met un rectangle rouge sur les faux positifs
            cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 0, 255) , 2) 

    #Afficher la vidéo ou non
    show_img(cv_image,2)



def show_img(image: Image, n: int):
    global var 
    var = var + 1
    if(var % n == 0):
        cv2.imshow("Image2", image)
        cv2.waitKey(3)

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

# Script:
###############
cap=cv2.VideoCapture(0)
ret, frame=cap.read()
detection(frame)