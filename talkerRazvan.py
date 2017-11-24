#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from random import randint #Para generar numeros pseudoaleatorios

def coordGenerator():
    
    
    rospy.init_node('coordinates_generator', anonymous=True)

    pub = rospy.Publisher('turtleAutoMove', Pose, queue_size=10)

    pose = Pose()

    rate = rospy.Rate(0.2) #Cada 5 segundos un mensaje

    rospy.sleep(1) #Con este sleep se evita perder el primer mensaje

    while not rospy.is_shutdown():
    	x = (randint(0,11))
    	y = (randint(0,11))
        hello_str = "Generada nueva posicion con x= %d && y= %d" %(x,y)
        rospy.loginfo(hello_str)
        pose.x = x
        pose.y = y
        rospy.loginfo(pose)
        pub.publish(pose)
        rate.sleep()

if __name__ == '__main__':
    try:
        coordGenerator()
    except rospy.ROSInterruptException:
        pass
