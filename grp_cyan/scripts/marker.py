#!/usr/bin/python3
from visualization_msgs.msg import Marker
import rospy
from geometry_msgs.msg import PoseStamped


# var. global:
###############
i = 0
publisher= None

# call back:
###############

def CreateMarker( posx, posy, posz):
    global i
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time()
    marker.ns = "ns"
    marker.id = i
    marker.type = Marker.CUBE
    marker.action = Marker.ADD
    marker.lifetime = rospy.Duration()
    marker.pose.position.x = posx
    marker.pose.position.y = posy
    marker.pose.position.z = posz
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1
    marker.color.a = 1.0 
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    
    return marker

def func(data: PoseStamped):
    global publisher
    global i
    i+=1
    
    marker = CreateMarker(data.pose.position.x,data.pose.position.y,data.pose.position.z)
    publisher.publish(marker)


# Script:
###############

rospy.init_node('Maker', anonymous=True)

i = 0
publisher = rospy.Publisher("/Marker", Marker, queue_size=10)
rospy.Subscriber('/BottleGlobalCoords', PoseStamped, func )

rospy.spin()