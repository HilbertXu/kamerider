#!/usr/bin/env python

"""
     colour_tracker_2.py - robot will rotate to follow the color desired

"""

import roslib; roslib.load_manifest('cmvision')
import rospy
from cmvision.msg import Blobs
from geometry_msgs.msg import Twist

blob_position_x = 0
turn = 0.0

class Colour_Tracker:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

	# publish twist messages to /cmd_vel
    	self.vel = rospy.Publisher('/mobile_base/commands/velocity', Twist)

    	# subscribe to the robot sensor state
    	rospy.Subscriber('/blobs', Blobs, self.callback)

	# a user defined variable which is type Twist()
	self.message = Twist()

	# robot will only rotate to find colour
        self.message.linear.x = 0; self.message.linear.y = 0; self.message.linear.z = 0

    	while not rospy.is_shutdown():
            self.message.angular.x = 0.0; self.message.angular.y = 0; self.message.angular.z = turn

            # send the message and delay
            self.pub.publish(self.message)
	    rospy.Rate(4).sleep()

	    rospy.loginfo("blob is at x: %s"%blob_position_x)

    def callback(self, data):
        if(len(data.blobs)):
	    global blob_position_x

	    blob_position_x = 0

	    for obj in data.blobs:
	      blob_position_x = blob_position_x + obj.x

	    blob_position_x = blob_position_x/len(data.blobs)

	    # assume camera image size is 640x320 and we only focus on x-axis
	    # assume user want robot to locate colour blob at centre
	    # turn right if colour blob at right
	    if( blob_position_x > 330 ):
	        turn = -0.4
	    # turn left if colour blob at left
	    elif( blob_position_x < 310 ):
	        turn = 0.4

	    elif( blob_position_x >= 310 and blob_position_x <= 330):
	        turn = 0.0

    def cleanup(self):
        rospy.loginfo("Shutting down color tracking...")

if __name__=="__main__":
    rospy.init_node('colour_tracker')
    try:
        Colour_Tracker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

