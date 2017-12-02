#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
from math import *
from final.msg import JointPos

import baxter_interface
from baxter_interface import CHECK_VERSION


def quardToRPY(rot):
    q3, q2, q1, q0 = rot
    roll = atan2(2. * (q0 * q1 + q2 * q3), (1. - 2. * (q1**2 + q2 ** 2)))
    pitch = asin(2. * (q0 * q2 - q3 * q1))
    yaw = atan2(2. * (q0 * q3 + q1 * q2), (1. - 2. * (q2 ** 2 + q3 ** 2)))
    return [roll, pitch, yaw]


if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')

    listener = tf.TransformListener()
    left_grip = baxter_interface.Gripper('left', CHECK_VERSION)
    pub = rospy.Publisher('JointFeed', JointPos, queue_size = 10)

    rate = rospy.Rate(10)

    left_grip.calibrate()

    while not rospy.is_shutdown():
        jp = JointPos()


        ''' Left Shoulder Joints '''
        try:
            (trans,rot) = listener.lookupTransform('/neck_1', '/left_shoulder_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        roll, pitch, yaw = quardToRPY(rot)

        jp.lj1 = -1. * roll/ (pi / 2.)
        jp.lj2 = (yaw-1.368) / (pi / 2.) - 3.
        jp.lj0 = -1. * pitch

        
        ''' Right Shoulder Joints '''
        try:
            (trans,rot) = listener.lookupTransform('/neck_1', '/right_shoulder_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        roll, pitch, yaw = quardToRPY(rot)

        #jp.rj1 = 2. * roll/ (pi / 2.)
        if roll > -10:
            left_grip.open()
        else:
            left_grip.close()
        #jp.rj2 = (yaw-1.368) / (pi / 2.) - 3.
        #jp.lj5 = -1. * pitch

        ''' Left Elbow Joints '''
        try:
            (trans,rot) = listener.lookupTransform('/left_shoulder_1', '/left_elbow_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        roll, pitch, yaw = quardToRPY(rot)

        if fabs((fabs(yaw) - pi)) > pi/5.:
            jp.lj3 = pitch
        else:
            jp.lj3 = pi - pitch
        
        ''' Right Elbow Joints '''
        try:
            (trans,rot) = listener.lookupTransform('/right_shoulder_1', '/right_elbow_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        roll, pitch, yaw = quardToRPY(rot)

        if fabs((fabs(yaw) - pi)) > pi/5.:
            jp.lj5 = pitch
        else:
            jp.lj5 = pi - pitch

        ''' Safety '''
        #jp.lj5 = -1.57
        jp.rj5 = -1.57
        if jp.rj0 < 0:
            jp.rj0 = 0
        if jp.lj0 > 0.:
            jp.lj0 = 0.;

        pub.publish(jp)

        rate.sleep()
