import json
import os
import time

from final.msg import JointPos

class msg_with_time:
    def __init__(self, msg, time):
        self.msg = msg
        self.time = time

class Linear_filter():
    def __init__(self, alpha):
        self.alpha = alpha
        self.previous = None

    def clean_previous(self):
        self.previous = None

    def act(self, target):
        temp_result = dict()
        if self.previous == None:
            self.previous = json.loads(json.dumps(target, default = lambda obj: obj.__dict__))
            return target
        else:
            for key in self.previous.keys():
                temp_result[key] = self.previous[key] * self.alpha + target.__dict__[key] * (1 - self.alpha)
            self.previous = temp_result
            return dict_to_msg(temp_result) 

filter = Linear_filter(0.5)

def dict_to_msg(input_dict):
    mes = JointPos()
    mes.lj0 = input_dict['left_s0']
    mes.lj1 = input_dict['left_s1']
    mes.lj2 = input_dict['left_e0']
    mes.lj3 = input_dict['left_e1']
    mes.lj4 = input_dict['left_w0']
    mes.lj5 = input_dict['left_w1']
    mes.lj6 = input_dict['left_w2']

    mes.rj0 = input_dict['right_s0']
    mes.rj1 = input_dict['right_s1']
    mes.rj2 = input_dict['right_e0']
    mes.rj3 = input_dict['right_e1']
    mes.rj4 = input_dict['right_w0']
    mes.rj5 = input_dict['right_w1']
    mes.rj6 = input_dict['right_w2']

    return mes

'''
def dict_to_msg(input_dict):
    #a = input_dict[input_dict.keys()[0]]
    mes = Message(input_dict['aa'], input_dict['bb'])
    return mes
'''

def Execute(function):
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

    print(msg_list)

    ref_time = time.time()
    i = 0
    while i < len(content):
        print(msg_list[i]['time'])
        i = i + 1
        function()

    
class Recorder():
    path = os.getcwd()
    folder = "motion"

    def __init__(self, MotionName):
        self.File = MotionName + ".txt"
        self.records = list()
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder) 
        fp = open(self.path + "/" + self.folder +"/" + self.File, 'w')
        fp.close()
        filter.clean_previous()

    def TakeRecord(self, msg):
        store_msg = msg_with_time(filter.act(msg), time.time())
        store_msg = json.dumps(store_msg, default = lambda obj: obj.__dict__)
        self.records.append(store_msg)

    def Store_txt(self):
        fp = open(self.path + "/" + self.folder +"/" + self.File, 'w')
        fp.write(json.dumps(self.records))
        fp.close()

class Message():
    def __init__(self, jointpos):
        self.msg = jointpos
    
    def go():
        print("213123")

test1 = JointPos()
test1.lj1 = 1;
test2 = JointPos()
test2.lj1 = 1;


recorder = Recorder("xadfadsfae")
recorder.TakeRecord(Message(test1))
recorder.TakeRecord(Message(test2))
recorder.Store_txt()

def function():
    print("AXIMA")
Execute(function)
