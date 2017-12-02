import rospy
from final.msg import JointPos

import MotionRecoder

def talker():

    rospy.init_node('talker', anonymous = True)

    pub = rospy.Publisher('currentJointPosition', JointPos, queue_size = 10)

    r = rospy.Rate(10)

    path = os.getcwd() + "/motion"
    
    for i in os.walk(path):
        all_file = i[2]
    
    print("You have record the following listed motions!!!")
    print("")

    for i in range(len(all_file)):
        print(i + 1, all_file[i][ : -4])

    print("")
    print("Please type in the index to choose the motion you want to act!!!")

    index = float("inf")
    while index >= len(all_file):
        index = input()

    file_name = all_file[index - 1]
    fb = open(path + '/'+ file_name,'r')  
    content = list()
    for eachline in fb:  
        content.append(eachline.strip()) 
    
    fb.close()

    content = content[0]
    content = json.loads(content)
    msg_list = list()
    for msg in content:
        msg_list.append(json.loads(msg))

    index = 0

    previous_moment = msg_list[0]['time']

    while not rospy.is_shutdown() and index < len(msg_list):

        pub.publish(MotionRecoder.dict_to_msg(msg_list[0]['msg']))

        index = index + 1

        time_to_wait = msg_list[index]['time'] - previous_moment
        previous_moment = msg_list[index]['time'] 
        
        r.sleep(time_to_wait)  #有疑问

        

if __name__=='__main__':

    try:
        talker()
    except:
        rospy.ROSInterruptException: pass