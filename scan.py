#!/usr/bin/env python
import rospy

from miro_constants import miro
import time



#Miro
import miro_msgs
from miro_msgs.msg import platform_config,platform_sensors,platform_state,platform_mics,platform_control,core_state,core_control,core_config,bridge_config,bridge_stream

import math
import numpy
#import time
import sys
from miro_constants import miro

from datetime import datetime

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)

#to do
# change the config file
# find neck state/control and tune angle max/min
# check Compute_x
#Initialise global variable
sonar_value=0.8
yaw_angle=0.0
safety=0.15 #15 cm
Angle_max_right= -1.0
Angle_max_left= 1.0





def Compute_x(a,b,d):
	b=(2*a*b)/(a**2+1)
	c=(b**2-d**2)/(a**2+1)
	delta=b**2-4*c
	if(delta<0):
		return 0 #error
	elif(delta==0):
		return -1*b/(2*a)
	elif(a>=0):
		return (-1*b+math.sqrt(delta))/(2*a)
	else:
		return (-1*b-math.sqrt(delta))/(2*a)



#-----------------------Callback functions---------------------------------
def listenerMiro():
	def callbackss(data):
		global sonar_value,yaw_angle		
		sonar_value= data.sonar_range.range
		yaw_angle= data.joint_state.position[2] 

	rospy.Subscriber('/miro/rob01/platform/sensors', platform_sensors, callbackss)


	

def MiroScan():
	rate = rospy.Rate(100)
	global sonar_value,yaw_angle

	#-------------------------------------------------------
	#	Publishers
	#Neck joints
	pub_control_neck = rospy.Publisher("/miro/rob01/platform/control",platform_control)

	#-------------------------------------------------------

	q = platform_control()
	q.body_config_speed = [0, 0,-1,0]
	#Taking the distance to the obstacle
	d=sonar_value
	theta_r=Angle_max_right	
	theta_l=Angle_max_left	
	i=0			
	

    
	
	while(yaw_angle>=Angle_max_right):
		q.body_config = [0, 0, -3.14, 0]
		pub_control_neck.publish(q)


		rate.sleep()			
		
	



	
	#turn head back to middle


	while(yaw_angle<-0.08):
		q.body_config = [0, 0, 0, 0]	
		pub_control_neck.publish(q)
		rate.sleep()
		#do nothing
	

    	
	i=0
	while(yaw_angle<=Angle_max_left):
		q.body_config = [0, 0, 3.14, 0]
		pub_control_neck.publish(q)
		#To be sure it's not just a false value of the sonar we will need 3 values of 0.0

		
		rate.sleep()
		
					

	#turn head back to middle

	while(yaw_angle>0.08):
		q.body_config = [0, 0, 0, 0]	
		pub_control_neck.publish(q)
		rate.sleep()

	
	
	rospy.set_param("state_avoid",True)
	rospy.set_param("state_scan",False)


		
			
def loop ():
	i=0
	while not rospy.is_shutdown():
		listenerMiro()
		name_param = rospy.search_param('state_scan')
		if(rospy.get_param(name_param)):
			print i		
			i+=1	
			MiroScan()

		
		
	
def init():
	
	# report
	rospy.loginfo("test")
	print("initialising...")
	print(sys.version)
	print(datetime.time(datetime.now()))
	rospy.init_node('scan', anonymous=True)
	


		
		
					
			
if __name__ == "__main__":
	rospy.loginfo("test")
	init()
	loop()
	
