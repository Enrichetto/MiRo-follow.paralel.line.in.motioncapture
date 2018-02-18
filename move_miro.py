#!/usr/bin/env python
import rospy
from miro_msgs.msg import platform_control
from std_msgs.msg import Header
from miro_msgs.msg import core_config
from miro_constants import miro


def move_miro():
	
	#publishing topics
	pub = rospy.Publisher('/miro/rob01/platform/control', platform_control, queue_size=10)
	pub2 = rospy.Publisher('/miro/rob01/core/config', core_config, queue_size=10)

	#initiation
	rospy.init_node('move_miro', anonymous=True)
	rate = rospy.Rate(10)
	q = platform_control()
	q2 = core_config()
	count = 0

	#core config flag setup
	q2.msg_flags = core_config.FLAG_UPDATE_SIGNALS
	q2.P2U_W_body_signals = miro.MIRO_P2U_W_BODY_ENABLE
	pub2.publish(q2)

	while not rospy.is_shutdown():

		#q.body_vel.linear.x = 240
		#q.body_vel.linear.y = 240
		#q.body_vel.angular.z = 0

		q.body_config_speed = [0, -1,-1,0]
		q.body_config = [0, -3.14, 0, 0]
		pub.publish(q)
		rospy.loginfo(count)
		rate.sleep()
		count +=1
		
    

if __name__ == '__main__':
    try:
        move_miro()
    except rospy.ROSInterruptException:
        pass


# note, no rospy.spin() used since only publishing now
