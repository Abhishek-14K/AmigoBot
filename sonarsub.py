#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import PointCloud
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.points)
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("sonar", PointCloud, callback)
# spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
if __name__ == '__main__':
    listener()