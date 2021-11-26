#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry

pub = []
WHEEL_DIA = 0.195
WHEEL_BASE = 0.331

def compute_wheel_vel(v,w):
    w_r = (2*v + w*WHEEL_BASE)/WHEEL_DIA
    w_l = (2*v - w*WHEEL_BASE)/WHEEL_DIA
    return w_l,w_r

def callback(data):
    global pub
    v = data.twist.twist.linear.x
    w = data.twist.twist.angular.z
    w_left, w_right = compute_wheel_vel(v,w)
    msg = Float32MultiArray()
    msg.data = [w_left, w_right]
    pub.publish(msg)
    
def wheel_vel():
    global pub
    rospy.init_node('listener', anonymous=True)
    pub = rospy.Publisher('/wheel_velocities', Float32MultiArray, queue_size=10)
    rospy.Subscriber("/odom", Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    wheel_vel()