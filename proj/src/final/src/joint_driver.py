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

print("Initializing node... ")
rospy.init_node("joint_driver")
print("Getting robot state... ")
rs = baxter_interface.RobotEnable(CHECK_VERSION)
init_state = rs.state().enabled

left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
left_grip = baxter_interface.Gripper('left', CHECK_VERSION)
right_grip = baxter_interface.Gripper('right', CHECK_VERSION)
lj = left.joint_names()
rj = right.joint_names()

def jointSet(d):
    lcommand = {}
    rcommand = {}
    rjoint = [d.rj0, d.rj1, d.rj2, d.rj3, d.rj4, d.rj5, d.rj6]
    ljoint = [d.lj0, d.lj1, d.lj2, d.lj3, d.lj4, d.lj5, d.lj6]
    for i in range(len(rj)):
        lcommand[lj[i]] = ljoint[i]
        rcommand[rj[i]] = rjoint[i]
    #rospy.loginfo('setting: left    ' + ' '.join(str(e) for e in ljoint))
    #rospy.loginfo('setting: right   ' + ' '.join(str(e) for e in rjoint))
    left.set_joint_positions(lcommand)
    right.set_joint_positions(rcommand)
    if d.lgrip:
        left_grip.open()
    else:
        left_grip.close()
    if d.rgrip:
        right_grip.open()
    else:
        right_grip.close()

def main():

    def clean_shutdown():
        print("\nExiting example...")
        if not init_state:
            print("Disabling robot...")
            rs.disable()
    rospy.on_shutdown(clean_shutdown)

    print("Enabling robot... ")
    rs.enable()

    left_grip.calibrate()
    # right_grip.calibrate()

    rospy.Subscriber("JointFeed", JointPos, jointSet)
    rospy.spin()

    print("Done.")


if __name__ == '__main__':
    main()
