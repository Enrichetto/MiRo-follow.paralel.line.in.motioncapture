#!/usr/bin/env python
import rospy
from miro_msgs.msg import platform_control
from miro_msgs.msg import platform_state
from miro_msgs.msg import core_config
from miro_constants import miro
import time

# Check if body move is underway
move_underway = False
move_complete = False
counter=1

def callback_state(msg):

	global move_underway, move_complete
	underway = (msg.P2U_R_signals & miro.MIRO_P2U_R_BODY_MOVE_UNDERWAY) > 0
	if underway:
		move_underway = True
	if move_underway:
		if not underway:
			move_complete = True

def location_miro():

	# get relative destination
	# param_name = rospy.search_param('virtual_x')
	# x_dist = rospy.get_param(param_name)
	# param_name2 = rospy.search_param('virtual_y')
	# y_dist = rospy.get_param(param_name2)	

	param_name = rospy.search_param('turn_dir')
   	kak = rospy.get_param(param_name)
	# robot target
	robot = '/miro/rob01'

	# initialise ROS node
	rospy.init_node('location_miro', anonymous=True)

	# topic publishers
	pub = rospy.Publisher(robot + '/platform/control', platform_control, queue_size=10)
	pub2 = rospy.Publisher(robot + '/core/config', core_config, queue_size=10)

	# topic subscribers
	sub = rospy.Subscriber(robot + '/platform/state', platform_state, callback_state)

	# intialise rate object
	rate = rospy.Rate(10)

	# sleep to let the ROS node start up, or our config message
	# will not make it through
	time.sleep(1)

	# configure core to enable BODY module
	q = core_config()
	q.msg_flags = core_config.FLAG_UPDATE_SIGNALS
	q.P2U_W_body_signals = miro.MIRO_P2U_W_BODY_ENABLE
	pub2.publish(q)

	# create control message
	q = platform_control()
	#q.body_move.x = x_dist
	#q.body_move.y = y_dist
	
	if kak:
		q.body_move.x = 600	#in mm, positive to go forward
		q.body_move.y = -800	#negative to go to the right, positive to the left
		q.body_move.theta = 0
		rospy.set_param('turn_dir',False)
	else:
		q.body_move.x = 600	#in mm, positive to go forward
		q.body_move.y = 800	#negative to go to the right, positive to the left
		q.body_move.theta = 0
		rospy.set_param('turn_dir',True)
	# close eyes and hope for the best!
	q.eyelid_closure = 1

	# main loop
	count = 1
	while not rospy.is_shutdown():
	
		# add if condition here to check for state_avoid parameter
		# configure move flags
		if count >= 2:
			q.body_move_flags = miro.MIRO_BODY_MOVE_CONTINUE
		if count == 2:
			q.body_move_flags |= miro.MIRO_BODY_MOVE_START
		
		# publish control message
		pub.publish(q)
		
		# postamble
		rospy.loginfo("@" + str(count) + ", move_underway=" + str(move_underway))
		rate.sleep()
		count += 1
		print count
		# exit
		if move_complete:
			#global counter
			rospy.set_param('state_straight', True)
			rospy.set_param('state_avoid', False)
			#counter=2
			break;
			#rospy.set_param('new_goal',true)
			

if __name__ == '__main__':
    try:
	param_name = rospy.search_param('state_avoid')
   	n = rospy.get_param(param_name)
	print n
	if n:
        	location_miro()
    except rospy.ROSInterruptException:
        pass




