#!/usr/bin/python3
from email.mime import image
from glob import glob
from math import dist
import cv2, tf
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import PoseStamped
import numpy as np

# var. global:
###############

bridge = CvBridge()
var = 0                             #Compteur de frames
bottle = []
depth_cv_image = None
lower_red = np.array([0,40,60])
upper_red = np.array([9,255,255])
fpsDiv = 5
resX = 1280
resY = 720
publisher= None

# call back:
###############

def detection(data):
    global lower_red
    global upper_red
    global bottle
    global var
    global fpsDiv

    distance=0
    var += 1

    if var % fpsDiv != 0:
        return
    # On convertit l'image ros en image cv2 de façon sûre
    try:
        cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
    except CvBridgeError:
        rospy.logerr("CvBridge Error") 

    # On cherche les bouteilles grâce à la méthode de Haar
    image_hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    image_grey=cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    bottle_cascade = cv2.CascadeClassifier("/home/gabriel.harivel/catkin_ws/src/uv_larm/grp-cyan/cascade/cascade.xml")

    detected_bottle = bottle_cascade.detectMultiScale(image_grey, scaleFactor=1.10, minNeighbors=3)

    #Pour chaque bouteilles détectées, on va appliquer un filtre HSV sur la couleur rouge pour enlever les faux positifs
    for (column, row, width, height) in detected_bottle:
        crop_image = image_hsv[row:row+height, column:column+width] # On rogne les détections les detections
        filtre_hsv = cv2.inRange(crop_image, lower_red, upper_red)  # Filtrage des couleurs sur les images croppé
        
        if isBottle(filtre_hsv):
            #Met un rectangle vert sur les bouteilles
            cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 255, 0) , 2) 
            middle_positionX =  column+ width//2
            middle_positionY = row + height//2
            
            distance: int = depth_cv_image.data[ middle_positionY,middle_positionX]
            printText((column,row),cv_image, str(int(distance/10)) + "cm")
            

            phi = getPhi(middle_positionX) #J'ai pas pu debugué mais si ca marche pas essaye de changer le 0 et le 1 et de mettre un arcsin dans getPhi()
            #et si ca marche toujours pas faut refaire une formule pour trouver phi
            relativeCoords = PoseStamped()
            coords = projectionPolaire(distance, phi)
            divider = 1000
            relativeCoords.pose.position.x = coords[0]/divider
            relativeCoords.pose.position.y = coords[1]/divider
            relativeCoords.pose.position.z = 0
            relativeCoords.pose.orientation.w = 1
            relativeCoords.header.frame_id = 'base_footprint'
            relativeCoords.header.stamp = rospy.Time()

            publisher.publish(relativeCoords)
            #Normalement tu as dans bottle phi et x (l'angle et la distance dans le repère polaire du robot)
            #Je te conseille de publish les éléments de bottle dans un topic pour les traiter dans un autre noeud
            #bottle.append([phi, distance])
        else:
            #Met un rectangle rouge sur les faux positifs
            cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 0, 255) , 2) 

    #Afficher la vidéo avec les cadres ou non
    show_img(cv_image,5, True)

def isCentred(rgbPixelX, rgbPixelY):
    global resX, resY
    centreRatio = 0.3
    if(rgbPixelX > resX*centreRatio/2 and rgbPixelX <  resX - (resX*centreRatio/2)):
        if(rgbPixelY > resY*centreRatio/2 and rgbPixelY <  resY - (resY*centreRatio/2)):
            return True
    return False

#
def show_img(image: Image, n: int, bool):
    global var 
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
    if sum > (h*w)*0.09 :
        r=True
    return r

#Récupère l'image 3D et la met dans depth_cv_image
def enregistrementProfondeur(data):
    global depth_cv_image
    depth_cv_image = bridge.imgmsg_to_cv2(data, "16UC1")

#Récupère l'angle phi de la bouteille par rapport au milieu de l'image
def getPhi(x):
    global resX
    middle = resX/2
    dist = 0
    if x > middle:
        dist = x - middle
    elif x < middle:
        dist = x - middle
    ratio = dist / middle

    fov = 69
    return ratio*fov/2
    return 0
    hmax, wmax = len(image), len(image[0])
    origin = [hmax, wmax//2]
    y = origin[0] - height
    x = origin[1] - width
    return np.arccos(x)

def projectionPolaire(dist, phi):
    x = np.cos(phi) * dist
    y = np.sin(phi) * dist
    return [x,y]

#Permet d'afficher un texte sur une image cv2
def printText(bottomLeftCorner, img, text):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 0.6
    fontColor              = (255,255,255)
    thickness              = 1
    lineType               = 2

    cv2.putText(img, text, 
       bottomLeftCorner, 
       font, 
       fontScale,
       fontColor,
       thickness,
       lineType)
    
# Script:
###############

rospy.init_node('detector', anonymous=True)

publisher = rospy.Publisher(
    "/BottleRelativeCoords", PoseStamped, queue_size=10
)

rospy.Subscriber('/camera/color/image_raw', Image, detection )
rospy.Subscriber('/camera/aligned_depth_to_color/image_raw', Image, enregistrementProfondeur )

rospy.spin()