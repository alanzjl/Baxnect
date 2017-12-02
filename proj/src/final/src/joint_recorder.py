#!/usr/bin/env python

# Copyright (c) 2013-2015, Rethink Robotics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Rethink Robotics nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Baxter RSDK Joint Position Example: keyboard
"""
import argparse

import rospy

import baxter_interface
import baxter_external_devices

from baxter_interface import CHECK_VERSION

from final.msg import JointPos
'''
arg_fmt = argparse.RawDescriptionHelpFormatter
parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                description=main.__doc__,
                                epilog=epilog)
parser.parse_args(rospy.myargv()[1:])
'''
print("Initializing node... ")
rospy.init_node("joint_reader")
print("Getting robot state... ")
rs = baxter_interface.RobotEnable(CHECK_VERSION)
init_state = rs.state().enabled

pub = rospy.Publisher('currentJointPosition', JointPos, queue_size = 5)

left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
lj = left.joint_names()
rj = right.joint_names()

def pubCurPos():
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
    pub.publish(mes)

def main():
    
    if not init_state:
        print('Baxter not enabled')
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        pubCurPos()
        rate.sleep()
        raw_input()
        array = []
        array.append()


    rospy.on_shutdown(clean_shutdown)

    print("Enabling robot... ")
    rs.enable()

if __name__ == '__main__':
    main()
