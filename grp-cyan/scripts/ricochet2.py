#!/usr/bin/python3
import math, rospy, math
import numpy as np
import random as r
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

obs= True
duration = 0.1
sens = 1

# Publish velocity commandes:
def move(data):
    global  commandPublisher
    cmd= Twist()
    if obs :
        cmd.angular.z = 1 * sens       #si obstacle tourne et prend un angle aléatoire
    else :
        cmd.linear.x = 0.7           #sinon avance
    commandPublisher.publish(cmd)


def is_obstacle(data):
    global obs          #Variable d'état : True s'il ya un mur dans le champ de vision, false sinon
    global duration     #Durée de rotation du robot
    global sens         #sens de rotation du robot (1 horaire / -1 anti-horaire)
    duration=0.1 
    obs= False
    angle= data.angle_min

    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 0.5 :
            rospy.loginfo("MUR")
            obs= True
            duration = r.randrange(1,10)
            rospy.loginfo(duration)
            if angle > 0 :
                sens = -1
            else:
                sens = 1
            break
        angle += data.angle_increment


rospy.Subscriber('scan', LaserScan, is_obstacle )

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(duration), move, oneshot=False )
rospy.sleep(duration)

rospy.spin()