#! /usr/bin/env python3
from itertools import count
import rospy
from std_msgs.msg import String
import cv2
from sensor_msgs.msg import Image

from gazebo_msgs.msg import ModelStates
from cv_bridge import CvBridge
import os
from tf.transformations import euler_from_quaternion

global carPos, boxPos

def doMsg(msg):
    #rospy.loginfo("I heard:%s",msg.pose[2])
    global carPos, boxPos
    mycarIndex = msg.name.index('mycar')
    myboxIndex = msg.name.index('mybox')
    carPos = msg.pose[mycarIndex]
    boxPos = msg.pose[myboxIndex]
    #rospy.loginfo()

def doImg(msg):
    #rospy.loginfo("I heard:%s",msg.pose[2])
    #pos = msg.pose[2]
    global bridge, cnt
    cnt = cnt + 1
    if cnt % 10 == 0:
        cv_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imwrite("pic/" + str(cnt) + '.jpg', cv_img)
        #rospy.loginfo("I heard:%s", carPos)
        
        
        carX = float( str(carPos).split('\n')[1].split(':')[1])
        carY = float( str(carPos).split('\n')[2].split(':')[1])
        carX_ = float( str(carPos).split('\n')[5].split(':')[1])
        carY_ = float( str(carPos).split('\n')[6].split(':')[1])
        carZ_ = float( str(carPos).split('\n')[7].split(':')[1])
        carW_ = float( str(carPos).split('\n')[8].split(':')[1])

        boxX = float( str(boxPos).split('\n')[1].split(':')[1])
        boxY = float( str(boxPos).split('\n')[2].split(':')[1])
        boxX_ = float( str(boxPos).split('\n')[5].split(':')[1])
        boxY_ = float( str(boxPos).split('\n')[6].split(':')[1])
        boxZ_ = float( str(boxPos).split('\n')[7].split(':')[1])
        boxW_ = float( str(boxPos).split('\n')[8].split(':')[1])
        #print(carY)
        carE = euler_from_quaternion([carX_, carY_, carZ_, carW_])
        boxE = euler_from_quaternion([carX_, carY_, carZ_, carW_])
        
        print(carY)
        

        fil = open('posture/car.csv', 'a+')
        fil.write("%f, %f, %f\n"%(carX, carY, carE[2]) )
        fil.close()

        fil = open('posture/box.csv', 'a+')
        fil.write("%f, %f, %f\n"%(boxX, boxY, boxE[2]) )
        fil.close()

        #rospy.loginfo("I heard:%s")

    else:
        pass

    #cv2.imread(msg)
    

if __name__ == "__main__":
    
    os.mkdir("posture")
    os.mkdir("pic")

    fil = open('posture/car.csv', 'a+')
    fil.write("x, y, pitch\n")
    fil.close()

    fil = open('posture/box.csv', 'a+')
    fil.write("x, y, pitch\n")
    fil.close()
    

    #2.初始化 ROS 节点:命名(唯一)
    rospy.init_node("listener_p")
    #3.实例化 订阅者 对象
    rospy.loginfo("I heard\n")
    global bridge, cnt
    cnt = 0
    bridge = CvBridge()
    sub1 = rospy.Subscriber("/gazebo/model_states",ModelStates,doMsg,queue_size=10)
    sub2 = rospy.Subscriber("/camera/image_raw",Image,doImg,queue_size=10)
    #4.处理订阅的消息(回调函数)
    #5.设置循环调用回调函数
    rospy.spin()
    #fil.close()