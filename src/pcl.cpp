#include <signal.h> 
#include <vector>
#include <string>
#include <ros/ros.h>

#include <ros/package.h>

#include <sensor_msgs/PointCloud2.h>


#include <pcl/conversions.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/console/parse.h>
#include <pcl/point_types.h>
#include <pcl/visualization/pcl_visualizer.h>    
#include <pcl/io/openni_grabber.h>
#include <pcl/sample_consensus/sac_model_plane.h>
#include <pcl/people/ground_based_people_detection_app.h>
#include <pcl/common/time.h>
#include <pcl/filters/crop_box.h>


//some custom functions
#include "utils/file_io.h"
//#include "utils/viz_utils.h" 
//#include "utils/pcl_utils.h"
// Mutex: //
boost::mutex cloud_mutex;
bool new_cloud_available_flag = false;

typedef pcl::PointXYZRGB PointT;
typedef pcl::PointCloud<PointT> PointCloudT;
PointCloudT::Ptr cloud (new PointCloudT);

using namespace std;

//true if Ctrl-C is pressed
bool g_caught_sigint=false;

void sig_handler(int sig)
{
  g_caught_sigint = true;
  ROS_INFO("caught sigint, init shutdown sequence...");
  ros::shutdown();
  exit(1);
};



void 
cloud_cb (const sensor_msgs::PointCloud2ConstPtr& input)
{
	cloud_mutex.lock (); 
	
	//convert to PCL format
	pcl::fromROSMsg (*input, *cloud);

	//state that a new cloud is available
	new_cloud_available_flag = true;
	ROS_INFO("inside the callback");
	
	cloud_mutex.unlock ();
}



int main (int argc, char** argv)
{
	// Initialize ROS
	ros::init (argc, argv, "gnn_localizer");
	ros::NodeHandle nh;

	
	const std::string param_topic = "/camera/depth_registered/points"; 
	//nh.param<std::string>(std::string("background_person_detector/rgbd_topic"), param_topic, data_topic);

	// Create a ROS subscriber for the input point cloud
	ros::Subscriber sub = nh.subscribe (param_topic, 1, cloud_cb);


	//refresh rate
	double ros_rate = 10.0;

	ros::Rate r(ros_rate);




	while (!g_caught_sigint && ros::ok())
	{
		//collect messages
		ros::spinOnce();
		
		r.sleep();
		
		if (new_cloud_available_flag && cloud_mutex.try_lock ())    // if a new cloud is available
		{

			ROS_INFO("inside while");


		}
	}
}