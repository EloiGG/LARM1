#!/usr/bin/python3
import cv2, tf
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped

# var. global:
###############
tfListener = None
publisher = None

# call back:
###############

def transformation(data):
    global_coords= tfListener.transformPose("map", data)
    print(global_coords)
    publisher.publish(global_coords)
    

# Script:
###############

rospy.init_node("tfTransform", anonymous=True)
tfListener = tf.TransformListener()
publisher = rospy.Publisher(
    "/BottleGlobalCoords", PoseStamped, queue_size=10
)

rospy.Subscriber('/BottleRelativeCoords', PoseStamped, transformation )

rospy.spin()