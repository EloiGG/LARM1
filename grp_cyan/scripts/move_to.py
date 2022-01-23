#!/usr/bin/python3
import math, rospy, tf
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

goal= 0
tfListener=0


# Initialize ROS::node
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    local_goal= tfListener.transformPose("/base_footprint", goal)

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/goal", PoseStamped, callback)

    rospy.spin()


if __name__ == '__main__':

    rospy.init_node('move', anonymous=True)
    tfListener = tf.TransformListener()
    #publisher:
    commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
    )
    #subscribers:
    rospy.Subscriber('scan', PoseStamped, listener )
    #timers:
    rospy.Timer( rospy.Duration(0.1), callback, oneshot=False )

    rospy.spin()
