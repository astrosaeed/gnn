#!/usr/bin/env python  
import roslib
import tf2_ros
import tf2_geometry_msgs
import rospy
import math
import tf
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler
#import turtlesim.srv

if __name__ == '__main__':
	rospy.init_node('transformer')


	tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
	tf_listener = tf2_ros.TransformListener(tf_buffer)
	pose_i = Pose()
	pose_i.position.x = 3
	pose_i.position.y = 0
	pose_i.position.z = 0
	pose_i.orientation.x =quaternion_from_euler(0, 0, -1.5707)[0]
	pose_i.orientation.y =quaternion_from_euler(0, 0, -1.5707)[1]
	pose_i.orientation.z =quaternion_from_euler(0, 0, -1.5707)[2]
	pose_i.orientation.w =quaternion_from_euler(0, 0, -1.5707)[3]

	pose_stamped = PoseWithCovarianceStamped()
	pose_stamped.header.frame_id = '3rdFloor_map'
	pose_stamped.header.stamp = rospy.Time(0)

	pose_stamped.pose = pose_i


	pub  = rospy.Publisher('object_loc',Pose,queue_size=10)
	#print pose_stamped
	rate = rospy.Rate(1.0)
	while not rospy.is_shutdown():
		try:
			transform = tf_buffer.lookup_transform('3rdFloor_map',
									   'base_footprint', #source frame
									   rospy.Time(0), #get the tf at first available time
									   rospy.Duration(1.0)) #wait for 1 second

			pose_transformed = tf2_geometry_msgs.do_transform_pose(pose_stamped, transform)

		#	(trans,rot) = pose_transformed
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue

		print pose_transformed
		pub.publish(pose_transformed.pose)
		rate.sleep()
