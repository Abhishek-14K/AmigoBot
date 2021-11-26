#!/usr/bin/env python

import rospy
import time
import math
import tf
from math import sin, cos
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from std_msgs.msg import Float32MultiArray

class Move:
    def wheel_velocity(self, data):
        self.vl = (data.data[0])
        self.vr = (data.data[1])

    def __init__(self):
        self.vl = 0
        self.vr = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.now = time.time()
        self.odom_quat = 0
        self.odom = Odometry()
        self.rate = rospy.Rate(10)
        self.sub = rospy.Subscriber("/wheel_velocities", Float32MultiArray, self.wheel_velocity)
        self.odom_pub = rospy.Publisher("/my_odom", Odometry, queue_size=10)

    def run(self):
        current_time = time.time()
        dt = current_time - self.now
        self.now = time.time()
        dl = self.vl * dt * .0975
        dr = self.vr * dt * .0975
        dc = (dl + dr) / 2
        wheelbase = .331
        phi = (dr - dl) / wheelbase
        self.theta = self.theta + phi
        self.x = self.x + (dc * cos(self.theta))
        self.y = self.y + (dc * sin(self.theta))

        odom_quat = tf.transformations.quaternion_about_axis(self.theta, [0,0,1])

        print(self.vl, self.vr)
        print(odom_quat)
        print(self.x,self.y)

        self.odom.header.frame_id = "odom"
        self.odom.child_frame_id = "base_link"
        self.odom.pose.pose = Pose(Point(self.x, self.y, 0), Quaternion(*odom_quat))

        # publish the message
        self.odom_pub.publish(self.odom)


if __name__ == '__main__':
    rospy.init_node('odometry_publisher')
    odom = Move()
    while not rospy.is_shutdown():
        odom.run()