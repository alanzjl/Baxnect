#!/usr/bin/python
#########################################################################
# File Name: camera.py
# Description: 
# Author: Jialiang Zhao
# Mail: alanzjl@163.com
# Created_Time: 2017-11-27 20:57:31
# Last modified: 2017-11-27 20:57:1511845051
#########################################################################
import baxter_interface
import rospy
from sensor_msgs.msg import Image

rospy.init_node("my_cam")
dpub = rospy.Publisher('/robot/xdisplay', Image, queue_size=10)

def repub(msg):
    dpub.publish(msg)
#lcam = baxter_interface.CameraController("left_hand_camera")
#lcam.close()
hcam = baxter_interface.CameraController("head_camera")
hcam.resolution=(960,600)
cname = "head_camera"
sub = rospy.Subscriber("/cameras/head_camera/image", Image, repub)
rospy.spin()
