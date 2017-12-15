#!/usr/bin/env python

import argparse

import rospy

import baxter_interface
import baxter_external_devices

from baxter_interface import CHECK_VERSION

from KBHit import KBHit

from final.msg import Mode

from final.msg import JointPos

print("Initializing node... ")
rospy.init_node("joint_reader")

pub = rospy.Publisher('JointFeed', JointPos, queue_size = 5)
pubmode = rospy.Publisher('mode_controller', Mode, queue_size = 5)

left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
lj = left.joint_names()
rj = right.joint_names()

def readPos():
    mes = JointPos()
    for ljoint in lj:
        if ljoint == 'left_s0':
            mes.lj0 = left.joint_angle(ljoint)
        if ljoint == 'left_s1':
            mes.lj1 = left.joint_angle(ljoint)
        if ljoint == 'left_e0':
            mes.lj2 = left.joint_angle(ljoint)
        if ljoint == 'left_e1':
            mes.lj3 = left.joint_angle(ljoint)
        if ljoint == 'left_w0':
            mes.lj4 = left.joint_angle(ljoint)
        if ljoint == 'left_w1':
            mes.lj5 = left.joint_angle(ljoint)
        if ljoint == 'left_w2':
            mes.lj6 = left.joint_angle(ljoint)
    for rjoint in rj:
        if rjoint == 'right_s0':
            mes.rj0 = right.joint_angle(rjoint)
        if rjoint == 'right_s1':
            mes.rj1 = right.joint_angle(rjoint)
        if rjoint == 'right_e0':
            mes.rj2 = right.joint_angle(rjoint)
        if rjoint == 'right_e1':
            mes.rj3 = right.joint_angle(rjoint)
        if rjoint == 'right_w0':
            mes.rj4 = right.joint_angle(rjoint)
        if rjoint == 'right_w1':
            mes.rj5 = right.joint_angle(rjoint)
        if rjoint == 'right_w2':
            mes.rj6 = right.joint_angle(rjoint)
    return mes

def main():
    print "started"

    kb = KBHit()
    mode = Mode()
    mode.mode = 0

    recording = False
    playing = False

    rec = []
    reclength = 0
    recindex = 0
    
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        oldmode = mode.mode
        if recording:
            rec.append(readPos())

        if playing:
            if recindex < len(rec):
                pub.publish(rec[recindex])
                recindex += 1
            else:
                print "playing finished"
                playing = False


        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 49:    #1, double arms
                print "double arm"
                mode.mode = 1
            elif ord(c) == 50:    #2, single arm
                print "single arm"
                mode.mode = 2
            elif ord(c) == 48:    #0 stop
                print "stop"
                mode.mode = 0
            elif ord(c) == 114:    #r, recording
                if recording:
                    print "stop rec"
                    recording = False
                else:
                    print "rec"
                    recording = True
                    rec = []
            elif ord(c) == 112:      #p, play
                if playing:
                    print "stop playing"
                    playing = False
                else:
                    print "playing"
                    playing = True
                    recindex= 0
                    reclength = len(rec)

        if oldmode != mode.mode:
            pubmode.publish(mode)
        rate.sleep()

    rospy.on_shutdown(clean_shutdown)


if __name__ == '__main__':
    main()
