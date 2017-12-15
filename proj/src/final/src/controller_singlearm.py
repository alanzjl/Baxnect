#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
from math import *
from final.msg import JointPos
from final.msg import Mode

start = False


def quardToRPY(rot):
    q3, q2, q1, q0 = rot
    roll = atan2(2. * (q0 * q1 + q2 * q3), (1. - 2. * (q1**2 + q2 ** 2)))
    pitch = asin(2. * (q0 * q2 - q3 * q1))
    yaw = atan2(2. * (q0 * q3 + q1 * q2), (1. - 2. * (q2 ** 2 + q3 ** 2)))
    return [roll, pitch, yaw]

def modeCallBack(msg):
    global start
    if msg.mode == 2:
        start = True
    else:
        start = False


if __name__ == '__main__':
    rospy.init_node('single_arm_controller')

    listener = tf.TransformListener()
    #left_grip = baxter_interface.Gripper('left', CHECK_VERSION)
    pub = rospy.Publisher('JointFeed', JointPos, queue_size = 10)
    rospy.Subscriber('mode_controller', Mode, modeCallBack)

    # left_grip.calibrate()

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if not start:
            continue
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
        print roll
        jp.lj5 = roll * -1.
        '''
        if roll < 0.8:
            jp.lgrip = True
            # left_grip.open()
        else:
            jp.lgrip = False
            # left_grip.close()
        '''
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
        print pitch, yaw
        # jp.lj5 = -1. * pitch
        if pitch < -1 * pi / 5.:
            jp.lgrip = True
        else:
            jp.lgrip = False

        '''
        if fabs((fabs(yaw) - pi)) > pi/5.:
            jp.lj5 = pi + pitch
        else:
            jp.lj5 = pitch - pi/2.
        '''
        ''' Safety '''
        #jp.lj5 = -1.57
        jp.rj5 = -1.57
        if jp.rj0 < 0:
            jp.rj0 = 0
        if jp.lj0 > 0.:
            jp.lj0 = 0.;

        pub.publish(jp)
        rate.sleep()
