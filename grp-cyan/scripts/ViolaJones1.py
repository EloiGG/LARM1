#!/usr/bin/python3
import cv2,tf
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int16MultiArray
from geometry_msgs.msg import PoseStamped

# Initialize ROS::node
rospy.init_node('detector', anonymous=True)
bridge = CvBridge()
var = 0                 #Compteur de frames
bottle=[]               #Coordonnées des bouteilles
depth_cv_image = 0      #L'image 3D correspondantes à frame
goal = PoseStamped()
listener = tf.TransformListener()

#Permet de traiter/afficher une frame sur n
def show_img(image: Image, n: int):
    global var 
    var = var + 1
    if(var % n == 0):
        cv2.imshow("Image2", image)
        cv2.waitKey(3)

def detection(data: Image):
        frame = data
        global depth_cv_image
        datatosend = Int16MultiArray()
        
        try:
            cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError:
          rospy.logerr("CvBridge Error") 

        #On utilise la cascade de Haar pour détecter les bouteilles
        image=cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier('/home/gabriel.harivel/Bureau/DataL/cascade.xml')
        detected_faces = face_cascade.detectMultiScale(image, scaleFactor=1.10, minNeighbors=3)
        goal = listener.lookupTransform('odom', 'base_footprint', rospy.Time(0))
        print(goal[0])
        #var = listener.transformPose("/base_footprint", goal)
        for (column, row, width, height) in detected_faces:
            if isSquareValid(column,row,width,height) :   

                middlePosition = ( column+ width//2,row+ height//2)
                cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 255, 0) , 2)
                cv2.rectangle(cv_image , middlePosition, (middlePosition[0]+3, middlePosition[1]+3) , (0, 0, 255) , 2)
                cv2.rectangle(depth_cv_image ,(0,50), (100,150) , (0, 0, 255) , 2)

                #send(getDistance(depth_image.data[0]))
                pixel: int = depth_cv_image.data[719, 1220]
                #print(pixel)
                #print(depth_cv_image.data)
                greyValue: int = depth_cv_image.data[row+ height//2 ,column+ width//2]
                distance = getDistance(greyValue)
                printText((column,row),cv_image,str(distance) + "cm")
                datatosend.data=()
                #send(datatosend)    

            else:
                print("invalid")
            show_img(cv_image, 2)

#Le script détecte des bouteilles en dehors de l'image, on choisit de les ignorer
def isSquareValid(column: int, row: int, width: int, height: int):
    if(column + width//2 < 1220):
        if(row + height//2 < 720):
            return True
    else:
        return False

#Récupère l'image 3D et la met dans depth_cv_image
def enregistrementProfondeur(data):
    global depth_cv_image
    depth_cv_image = bridge.imgmsg_to_cv2(data, "16UC1")

#On veut publier les coordonnées de la bouteille dans le topic /Bottle à chaque detection  
commandPublisher = rospy.Publisher(
    '/Bottle',
    Int16MultiArray, queue_size=10
)

#Publisher dans /Bottlegeometry_msgs
#Permet de récupérer une distance en cm en fonction du niveau de gris
def getDistance(depthPixel):
    distanceScaling = 3.86363
    return depthPixel

def getCoords(data):
    print("hello")
    if data.header.frame_id=='odom' or data.header.frame_id=='base_footprint':
        return data

#Permet d'afficher un texte sur une image cv2
def printText(bottomLeftCorner, img, text):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 0.4
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


rospy.Subscriber('/camera/color/image_raw', Image, detection )
rospy.Subscriber('/camera/aligned_depth_to_color/image_raw', Image, enregistrementProfondeur )

while not rospy.is_shutdown():
    rospy.spin()