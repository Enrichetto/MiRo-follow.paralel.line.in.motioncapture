#!/usr/bin/env python

#Author Enrico BORELLO (enrico.borello@yahoo.it)
#date   February, 2017

import subprocess
import signal
import sys
import os
import thread
import operator
import time
from copy import deepcopy
import math
import cmath
import numpy as np
import rospy
import argparse
import struct
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from miro_msgs.msg import platform_sensors,platform_control
#import baxter_interface
#from straightmiro.msg import straightmiro as Miro
from straightmiro.msg import Miro   #it dosn work, i change the name of the pytofile that had the same name of the folder. when i lunch rosrun he create a new file straighmiro.py that should not exist. 
from std_msgs.msg import UInt16MultiArray, Bool
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header


rospy.init_node('straightmiro', anonymous=True)

tetha=0   #yaw angle
nangle=-250
x= None
y= None
ox=0;
oy=0;
oz=0;
ow=0;

#quat = Quaternion(q)
goalx=-0.18
goaly= 1.80
IR=0
virtualx=goalx
virtual=goaly

v=False
n=True	
IR=0
roll = pitch = yaw = 0.0

start_x=0
start_y=0

#this function allow to find the rotatio that the miro need to do to be alline with the gool frame. The x of goal frame is the line the pass trought the actual miro position and the goal position
def miroline():
		global tetha,start_x,start_y
		
		param_name = rospy.search_param('virtual_x')
		VX = rospy.get_param(param_name)
		param_name = rospy.search_param('virtual_y')
		VY = rospy.get_param(param_name)
		
		start_x=VX   #i take this information for fix the miro position is move out of the straight line
		start_y=VY  

		
		ax =float(x)  #actual position of miro
		ay =float(y)  #actual position of miro
		#rospy.loginfo('ax :{} , ay:{}'.format(ax, ay))
		px= ax-float((ay*(VX-ax)/(VY-ay))) #this point corrispont to the size of the side of the triangole that is along x
		py= ay-float((ax*(VY-ay)/(VX-ax)))
		#rospy.loginfo('ax :{} , ay:{}'.format(px, py))
		sq=px**2+ py**2
		py = math.sqrt(sq) # py became the other side of the triangle
		if px != 0 : #& py!=0 :
			tetha = math.acos(px/py)
		#rospy.loginfo('roll :{} , pitch:{},yaw :{}'.format(tetha, px, py))

def listenerMiro():
	def callbackss(data):
		global IR		
		IR= data.sonar_range.range
		rospy.loginfo(IR)
		#check in rosmsg show ... how is define the distance (distance from infrared)
		
	rospy.Subscriber('/miro/rob01/platform/sensors', platform_sensors, callbackss)
def listenerMotion():
	def callback(msg):
		global x,y,ox,oy,oz,ow,quat
		x= msg.pose.position.x
		y= msg.pose.position.y
		global roll, pitch, yaw
    		orientation_q = msg.pose.orientation
    		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    		(roll, pitch, yaw) = euler_from_quaternion (orientation_list)
		
    		
	rospy.Subscriber('/miro/pose', PoseStamped, callback)
	
	
	#pub = rospy.Publisher('Mirostraight',Miro)
	#rate = rospy.Rate(10) # 10hz	
	#rospy.init_node('bax', anonymous=True)
	#rospy.Subscriber(listener_topic_name, PoseStamped, callback)
	#rate = rospy.Rate(10) # 10hz

def talker():
	pub = rospy.Publisher('Mirostraight', Bool, queue_size=10)
	pub_platform_control = rospy.Publisher("/miro/rob01/platform/control", platform_control, queue_size=10)
	
	rate = rospy.Rate(10) # 10hz
	q = platform_control()
	#rospy.loginfo(v)
	
	
	while not rospy.is_shutdown():
	   global v
	   if 0.1< IR <0.5 :
	    	if v:
			q.body_vel.linear.x=0
			q.body_vel.linear.y=0
			pub_platform_control.publish(q)
	   		rate.sleep()
			rospy.set_param('state_straight', False)
	    		rospy.set_param('state_scan', True)
		
		
	   #listenerMotion()
           ####################all this are to caalculate how much the miro is out on the straight line
	   #param_name = rospy.search_param('virtual_x')
	   #VX = rospy.get_param(param_name)
	   #param_name = rospy.search_param('virtual_y')
	   #VY = rospy.get_param(param_name)
	   #outofline = ((x-start_x)/(VX-start_x))-((y-start_y)/(VY-start_y))
	   #if outofline > 0.5
		#rospy.set_param('avoid_x', 5)
		#rospy.set_param('avoid_y', 5)
		#rospy.set_param('state_straight', False)
		#rospy.set_param('state_avoid', True)
	   ############################################################################
	
	   
	   param_name = rospy.search_param('new_goal')
   	   n = rospy.get_param(param_name)
	   if  x != None and y != None and n:
		global tetha
		miroline()
		
		rospy.set_param('new_goal', False)
		param_name = rospy.search_param('new_goal')
   	   	n = rospy.get_param(param_name)
	   	rospy.loginfo(n)
          
	   if v:  #if it dosnt work check the subscriver and the callback
			
		q.body_vel.linear.x = 250  #+ 250  #* math.cos(teta)    #this allow to go straight to the goal( follow the line could be weird)
		q.body_vel.linear.y=0   #+250  #* math.sin(teta)
		#rospy.loginfo('theta :{} , yaw:{}'.format(tetha, yaw))
		if  tetha-yaw >0.3 :
			q.body_vel.angular.z = +1.5 #+3.14   #tetha-yaw
			rospy.loginfo('theta :{} , yaw:{}'.format(tetha, yaw))
		elif tetha-yaw < -0.3 :		
			q.body_vel.angular.z = -1.5 #+3.14   #tetha-yaw
			rospy.loginfo('theta :{} , yaw:{}'.format(tetha, yaw))
		else:			
			q.body_vel.angular.z=0			
			#print 'on my wayyyyyyyyyyyyyyyyyyyy'	   
		#global nangle		
		#nangle = -1 * nangle
		#quaternion = quaternion_from_euler(0, 0, -180)
		
		#q.body_config_speed= [quaternion[0], quaternion[1], quaternion[2],quaternion[3]]
		#q.body_config_speed= [0.0, 0.296705961227417, -1.0471975803375244, -0.20943951606750488] #-1.0471975803375244		
	   	pub_platform_control.publish(q)
	   	rate.sleep()
			
		#q.body_config= [0.0, 0.296705961227417, -1.0471975803375244, -0.20943951606750488] # 3 for rotation, should look at right the miro, i don t know why it dosn t receive the information q.body_config_speed

		#q.ear_rotate =[0.5, 0.0]
		hello_str = 4   #this is not important
	   #if quat != None:
		    #euler = tf.transformations.euler_from_quaternion(quat)
		    #rospy.loginfo(quat)
	   param_name = rospy.search_param('state_straight')
   	   v = rospy.get_param(param_name)
	   #rospy.loginfo(euler)
	   #rospy.loginfo(q.body_vel.linear)
	   #rospy.loginfo('roll :{} , pitch:{},yaw :{}'.format(roll, pitch, yaw))   #usufull if you want check if the motioncapture works
	   #pub.publish(hello_str)
	   
#def main():
if __name__ == '__main__':
	""" RLAC- ros leapmotion AR10 controller

	This script will listen to data from LM
	and map the hand position to AR10 joints' position
	Make AR10 move along with hands.

	Calibration need to be performed before launching the application.

	Follow the instructions and we will perform calibration for
	open/close state for each hand.

	"""
	
	print "Executing main()"
	listenerMiro()
	listenerMotion()
	talker()	
	rospy.spin();	
	#sys.exit(main())	
	
	
