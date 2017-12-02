import rospy
from final.msg import JointPos
import MotionRecoder
import Keyboard

def callback(message):

    recorder.TakeRecord(message)
    
    """
    Need some code to interupt to jump out of the loop
    """
    if(Keyboard.heardEnter()):
        recorder.Store_txt()
        rospy.shutdown()

def listener():

    rospy.init_node('listener', anonymous = True)

    rospy.Subscriber('currentJointPosition', JointPos, callback)

    rospy.spin()

if __name__== '__main__':
    
    print("Type in the name you want to record")

    record_name = input()

    recorder = MotionRecoder.Recorder(record_name)
    
    print('Press ENTER to stop record the motion')

    listener()
