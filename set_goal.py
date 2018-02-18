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
import subprocess
import signal
import sys
import os
import thread
import operator
import time
#Author Enrico BORELLO (enrico.borello@yahoo.it)
#date   February, 2017
from copy import deepcopy
import math
import cmath
import numpy as np
import rospy
import argparse
import struct
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
rospy.set_param('goal_x', -0.18)
rospy.set_param('goal_y', 1.80)
rospy.set_param('virtual_x', -0.18)
rospy.set_param('virtual_y', 1.80)
rospy.set_param('avoid_x', 0)
rospy.set_param('avoid_y', 0)
rospy.set_param('state_straight', True)  #able node state_straight
rospy.set_param('state_scan', False)  #disable node state_scan
rospy.set_param('state_avoid', False) #disable node state_avoid
rospy.set_param('new_goal', True)  
rospy.set_param('turn_dir', True)

rospy.init_node('set_goal', anonymous=True)
def talker():
	#if(0.3<sensor <0.8 || move == FALSE )
	#	while(		
	#	send flag==1
	#	move ==FALSE
	#if(newgoal)
	#	create new line
	#follow the line
	#pubmiro=
	
	#param_name = rospy.search_param('state_straight')
	#rospy.set_param('state_straight', True)
   	#v = rospy.get_param(param_name)
	#pub_platform_control = rospy.Publisher("/miro/rob01/platform/control", platform_control, queue_size=10)
        rate = rospy.Rate(10) # 10hz
	
        while not rospy.is_shutdown():
           #rospy.set_param('state_straight', "false")
           #rospy.loginfo(v)
	   #rospy.loginfo('teta :{} , sin:{}'.format(teta,sin))   #usufull if you want check if the motioncapture works
           #pub.publish(hello_str)
	   #pub_platform_control.publish(q)
           rate.sleep()

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
		
	talker()	
	rospy.spin();	
	#sys.exit(main())
