#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
from math import *
from final.msg import JointPos

def quardToRPY(rot):
    q3, q2, q1, q0 = rot
    roll = atan2(2. * (q0 * q1 + q2 * q3), (1. - 2. * (q1**2 + q2 ** 2)))
    pitch = asin(2. * (q0 * q2 - q3 * q1))
    yaw = atan2(2. * (q0 * q3 + q1 * q2), (1. - 2. * (q2 ** 2 + q3 ** 2)))
    return [roll, pitch, yaw]


if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')

    listener = tf.TransformListener()
    pub = rospy.Publisher('JointFeed', JointPos, queue_size = 10)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        jp = JointPos()

        ''' Shoulder Joints '''
        try:
            (trans,rot) = listener.lookupTransform('/neck_1', '/left_shoulder_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        roll, pitch, yaw = quardToRPY(rot)

        jp.lj2 = (yaw-1.368) / (pi / 2.) - 3.
        jp.lj1 = -1. * roll/ (pi / 2.)

        ''' Elbow Joints '''
        try:
            (trans,rot) = listener.lookupTransform('/left_shoulder_1', '/left_elbow_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        roll, pitch, yaw = quardToRPY(rot)

        if fabs((fabs(yaw) - pi)) > pi/5.:
            jp.lj3 = pitch
        else:
            jp.lj3 = pi - pitch

        pub.publish(jp)

        rate.sleep()
