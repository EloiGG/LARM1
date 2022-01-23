import cv2
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker

# Initialize ROS::node
rospy.init_node('detector', anonymous=True)

marker_list=[]

def markerCreator(data):
    global marker_list

    marker = Marker()
    marker.id = len(marker_list)
    marker.pose.position.x=data.pose.position.x
    marker.pose.position.y=data.pose.position.y
    marker.pose.position.z=data.pose.position.z
    marker_list.append(marker)

rospy.Subscriber('/Bottle', PoseStamped, markerCreator )

rospy.spin()