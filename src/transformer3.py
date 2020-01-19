'''
This node does the coordinates transformation so that the robot knows the coordinates of objects in
front of it at any time. Then, the it publishes to the topic object_loc to be used by another node  

'''

#!/usr/bin/env python  
import roslib
import tf2_ros
import tf2_geometry_msgs
import rospy
import math
import tf
from gnn.msg import fourstamped
from gnn.msg import fourpose
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler
#import turtlesim.srv

if __name__ == '__main__':
	rospy.init_node('transformer')


	tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
	tf_listener = tf2_ros.TransformListener(tf_buffer)

	pose_1 = Pose()
	pose_1.position.x = 1
	pose_1.position.y = 0
	pose_1.position.z = 0
	pose_1.orientation.x =quaternion_from_euler(0, 0, -1.5707)[0]
	pose_1.orientation.y =quaternion_from_euler(0, 0, -1.5707)[1]
	pose_1.orientation.z =quaternion_from_euler(0, 0, -1.5707)[2]
	pose_1.orientation.w =quaternion_from_euler(0, 0, -1.5707)[3]

	pose_1_stamped = PoseWithCovarianceStamped()
	pose_1_stamped.header.frame_id = rospy.get_param("currentmap")
	pose_1_stamped.header.stamp = rospy.Time(0)

	pose_1_stamped.pose = pose_1


	pose_2 = Pose()
	pose_2.position.x = 2
	pose_2.position.y = 0
	pose_2.position.z = 0
	pose_2.orientation.x =quaternion_from_euler(0, 0, -1.5707)[0]
	pose_2.orientation.y =quaternion_from_euler(0, 0, -1.5707)[1]
	pose_2.orientation.z =quaternion_from_euler(0, 0, -1.5707)[2]
	pose_2.orientation.w =quaternion_from_euler(0, 0, -1.5707)[3]

	pose_2_stamped = PoseWithCovarianceStamped()
	pose_2_stamped.header.frame_id = rospy.get_param("currentmap")
	pose_2_stamped.header.stamp = rospy.Time(0)

	pose_2_stamped.pose = pose_2


	pose_3 = Pose()
	pose_3.position.x = 3
	pose_3.position.y = 0
	pose_3.position.z = 0
	pose_3.orientation.x =quaternion_from_euler(0, 0, -1.5707)[0]
	pose_3.orientation.y =quaternion_from_euler(0, 0, -1.5707)[1]
	pose_3.orientation.z =quaternion_from_euler(0, 0, -1.5707)[2]
	pose_3.orientation.w =quaternion_from_euler(0, 0, -1.5707)[3]

	pose_3_stamped = PoseWithCovarianceStamped()
	pose_3_stamped.header.frame_id = rospy.get_param("currentmap")
	pose_3_stamped.header.stamp = rospy.Time(0)

	pose_3_stamped.pose = pose_3


	pose_4 = Pose()
	pose_4.position.x = 4
	pose_4.position.y = 0
	pose_4.position.z = 0
	pose_4.orientation.x =quaternion_from_euler(0, 0, -1.5707)[0]
	pose_4.orientation.y =quaternion_from_euler(0, 0, -1.5707)[1]
	pose_4.orientation.z =quaternion_from_euler(0, 0, -1.5707)[2]
	pose_4.orientation.w =quaternion_from_euler(0, 0, -1.5707)[3]

	pose_4_stamped = PoseWithCovarianceStamped()
	pose_4_stamped.header.frame_id = rospy.get_param("currentmap")
	pose_4_stamped.header.stamp = rospy.Time(0)

	pose_4_stamped.pose = pose_4


	pub  = rospy.Publisher('object_loc',fourpose,queue_size=10)
	#print pose_stamped
	rate = rospy.Rate(1.0)
	while not rospy.is_shutdown():
		try:
			transform = tf_buffer.lookup_transform(rospy.get_param("currentmap"),
									   'base_footprint', #source frame
									   rospy.Time(0), #get the tf at first available time
									   rospy.Duration(1.0)) #wait for 1 second

			pose_transformed_1 = tf2_geometry_msgs.do_transform_pose(pose_1_stamped, transform)
			pose_transformed_2 = tf2_geometry_msgs.do_transform_pose(pose_2_stamped, transform)
			pose_transformed_3 = tf2_geometry_msgs.do_transform_pose(pose_3_stamped, transform)
			pose_transformed_4 = tf2_geometry_msgs.do_transform_pose(pose_4_stamped, transform)

		#	(trans,rot) = pose_transformed
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue
		posefour = fourpose()
		posefour.pose_1 = pose_transformed_1.pose
		posefour.pose_2 = pose_transformed_2.pose
		posefour.pose_3 = pose_transformed_3.pose
		posefour.pose_4 = pose_transformed_4.pose
		pub.publish(posefour)
		rate.sleep()
