#!/usr/bin/python3
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Initialize ROS::node
rospy.init_node('detector', anonymous=True)
bridge = CvBridge()
var2 =0

def show_img(image: Image):
    global var2 
    var2 = var2 + 1
    if(var2 % 5 == 0):
        cv2.imshow("Image", image)
        cv2.waitKey(3)

def detection(data: Image):

    #while True:
        frame = data
        
        try:
            cv_image = bridge.imgmsg_to_cv2(data, "passthrough")
        except CvBridgeError:
          rospy.logerr("CvBridge Error") 

        
        image=cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('/home/gabriel.harivel/Bureau/Data/cascade.xml')

        detected_faces = face_cascade.detectMultiScale(image, scaleFactor=1.10, minNeighbors=3)

        for (column, row, width, height) in detected_faces:
            cv2.rectangle(cv_image ,( column, row) , (column + width, row + height) , (0, 255, 0) , 2)
            rospy.loginfo("detection")
        
        show_img(cv_image)


        #if cv2.waitKey(1)&0xFF==ord('q'):
            #break
cv2.namedWindow("Image", 1)

rospy.Subscriber('/camera/color/image_raw', Image, detection )
while not rospy.is_shutdown():
    rospy.spin()