#!/usr/bin/python3
from email.mime import image
import cv2, tf
from scripts.ViolaJones1 import getDistance
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int16MultiArray
from geometry_msgs.msg import PoseStamped
import numpy as np

# var. global:
###############

bridge = CvBridge()
var = 0                             #Compteur de frames
bottle = []
depth_cv_image = None
lower_red = np.array([0,50,60])
upper_red = np.array([9,255,255])

# call back:
###############

def detection(data):
    global lower_red
    global upper_red
    global bottle
    distance=0

    # On convertit l'image ros en image cv2 de façon sûre
    try:
        cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
    except CvBridgeError:
        rospy.logerr("CvBridge Error") 

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
            middle_position = ( column+ width//2,row+ height//2)
            distance: int = depth_cv_image.data[row+ height//2 ,column+ width//2]
            phi = getPhi(middle_position[1], middle_position[0], image) #J'ai pas pu debugué mais si ca marche pas essaye de changer le 0 et le 1 et de mettre un arcsin dans getPhi()
            #et si ca marche toujours pas faut refaire une formule pour trouver phi

            #Normalement tu as dans bottle phi et x (l'angle et la distance dans le repère polaire du robot)
            #Je te conseille de publish les éléments de bottle dans un topic pour les traiter dans un autre noeud
            bottle.append([phi, distance])
        else:
            #Met un rectangle rouge sur les faux positifs
            cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 0, 255) , 2) 

    #Afficher la vidéo avec les cadres ou non
    show_img(cv_image,2, True)


#
def show_img(image: Image, n: int, bool):
    global var 
    var = var + 1
    if(var % n == 0) and (bool):
        cv2.imshow("Image2", image)
        cv2.waitKey(3)

#Trie les bouteilles des faux positifs
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

#Récupère l'image 3D et la met dans depth_cv_image
def enregistrementProfondeur(data):
    global depth_cv_image
    depth_cv_image = bridge.imgmsg_to_cv2(data, "16UC1")

#Récupère l'angle phi de la bouteille par rapport au milieu de l'image
def getPhi(height, width, image):
    hmax, wmax = image.shape()
    origin = [hmax, wmax//2]
    y = origin[0] - height
    x = origin[1] - width
    return np.arccos(x)

def projectionPolaire(dist, phi):
    x = np.cos(phi) * dist
    y = np.sin(phi) * dist
    return

    
# Script:
###############

rospy.init_node('detector', anonymous=True)

rospy.Subscriber('/camera/color/image_raw', Image, detection )
rospy.Subscriber('/camera/aligned_depth_to_color/image_raw', Image, enregistrementProfondeur )

rospy.spin()