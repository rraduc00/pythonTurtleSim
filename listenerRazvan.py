#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, sqrt, atan2
import numpy

x= 0
y= 0
theta = 0

velocityPublisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

def callback(data): 
    rospy.loginfo('Mis coordenadas antes de recibir las nuevas son x= %.9f && y= %.9f' %(x, y))
    rospy.loginfo(rospy.get_caller_id() + 'I heard coordinates x= %.9f && y= %.9f' %(data.x, data.y))
    vel_msg = Twist()

    #Primer publish a cmd_vel
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0

    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    zAngle = getAngle(x, y, data.x, data.y) - theta
    rospy.loginfo('angulo resultante = %f' % zAngle)
    vel_msg.angular.z = zAngle

    velocityPublisher.publish(vel_msg)
    rospy.loginfo(vel_msg)
    
    #Se duerme el proceso para que la tortuga gire
    rospy.sleep(1.5)
    
    #Segundo publish a cmd_vel
    vel_msg.linear.x = euclidean_distance(x, y, data.x, data.y)
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0

    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    velocityPublisher.publish(vel_msg)
    rospy.loginfo(vel_msg)


def euclidean_distance(x1, y1, x2, y2):
    return sqrt(pow(x2-x1,2) + pow(y2-y1,2)) # pow(x, y) es lo mismo que x**y

def getAngle(x1, y1, x2, y2):
    xDiff = x2 - x1
    yDiff = y2 - y1
    return atan2(yDiff, xDiff)

#Es necesario obtener la posición de la tortuga para tener en cuenta el
#angulo theta en todo momento.
def obtainGlobalParams(data):
    global x
    global y
    global theta

    x = data.x
    y = data.y
    theta = data.theta


def listener():

    rospy.init_node('coordinates_receiver_and_turtle_pusher', anonymous=True)
    
    rospy.Subscriber('turtle1/pose', Pose, obtainGlobalParams)
    rospy.Subscriber('turtleAutoMove', Pose, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
