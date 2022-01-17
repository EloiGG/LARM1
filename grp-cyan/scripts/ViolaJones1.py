#!/usr/bin/python3
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int16MultiArray


# Initialize ROS::node
rospy.init_node('detector', anonymous=True)
bridge = CvBridge()
var2 =0
var = 0
bottle=[]
depth_cv_image = 0

commandPublisher = rospy.Publisher(
    '/Bottle',
    Int16MultiArray, queue_size=10
)
def show_img2(image: Image):
    global var 
    var = var + 1
    if(var % 5 == 0):
        cv2.imshow("Image2", image)
        cv2.waitKey(3)

def show_img(image: Image):
    global var2 
    var2 = var2 + 1
    if(var2 % 2 == 0):
        cv2.imshow("Image", image)
        cv2.waitKey(3)

def detection(data: Image):
        frame = data
        
        try:
            cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError:
          rospy.logerr("CvBridge Error") 

        image=cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier('/home/gabriel.harivel/Bureau/DataE/cascade.xml')

        global depth_cv_image
        detected_faces = face_cascade.detectMultiScale(image, scaleFactor=1.10, minNeighbors=3)
        datatosend = Int16MultiArray()
        for (column, row, width, height) in detected_faces:
            if isSquareValid(column,row,width,height) :   
                middlePosition = ( column+ width//2,row+ height//2)
                cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 255, 0) , 2)
                cv2.rectangle(cv_image , middlePosition, (middlePosition[0]+3, middlePosition[1]+3) , (0, 0, 255) , 2)
                cv2.rectangle(depth_cv_image ,(0,50), (100,150) , (0, 0, 255) , 2)
                #send(getDistance(depth_image.data[0]))
                pixel: int = depth_cv_image.data[719, 1220]
                print(pixel)
                #print(depth_cv_image.data)
                greyValue: int = depth_cv_image.data[row+ height//2 ,column+ width//2]
                distance = getDistance(greyValue)
                printText((column,row),cv_image,str(distance) + "cm")
                #send(datatosend)    

            else:
                print("invalid")
            show_img(depth_cv_image)
            #show_img2(depth_cv_image)

def isSquareValid(column: int, row: int, width: int, height: int):
    if(column + width//2 < 1220):
        if(row + height//2 < 720):
            return True
    else:
        return False

def enregistrementProfondeur(data):
    global depth_cv_image
    depth_cv_image = bridge.imgmsg_to_cv2(data, "16UC1")


def send(data):
    global  commandPublisher
    # print(data)
    # print(type(data))
    commandPublisher.publish(data)

def getDistance(depthPixel):
    distanceScaling = 3.86363
    return distanceScaling * depthPixel

def printText(bottomLeftCorner, img, text):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 1
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

    
cv2.namedWindow("Image", 1)

rospy.Subscriber('/camera/color/image_raw', Image, detection )
rospy.Subscriber('/camera/aligned_depth_to_color/image_raw', Image, enregistrementProfondeur )

while not rospy.is_shutdown():
    rospy.spin()