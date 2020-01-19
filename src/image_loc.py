'''
This node takes rgb and depth images at the same time. Also, it saves the information (coordinates)
of the objects in a csv file that is save in the /metadata folder and later used by the database.
It subsribes to the object_loc topic
'''

#!/usr/bin/env python
import os
import roslib
#roslib.load_manifest('kinect_pylistener')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
from gnn.msg import fourpose
import numpy as np
import message_filters
import time
import datetime
import config

abs_path=config.abs_path
class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    image_sub = message_filters.Subscriber("/camera/rgb/image_raw", Image)
#    image_sub = message_filters.Subscriber("/usb_cam/image_raw", Image)
    depth_sub = message_filters.Subscriber("/camera/depth/image_raw", Image)
    self.ts = message_filters.ApproximateTimeSynchronizer([image_sub, depth_sub], 1, 1)
    self.ts.registerCallback(self.callback)
    print ("test2")
    self.image_received= False
    self.color_array = None
    self.depth_array = None
    self.x1= 0
    self.y1=0
    self.x2= 0
    self.y2=0
    self.x3= 0
    self.y3=0
    self.x4= 0
    self.y4=0

  def callback(self,rgb_data, depth_data):
    try:
      image = self.bridge.imgmsg_to_cv2(rgb_data, "bgr8")
      depth_image = self.bridge.imgmsg_to_cv2(depth_data, "passthrough")
      self.depth_array = np.array(depth_image, dtype=np.float32)
      self.color_array = np.array(image, dtype=np.uint8)
      self.depth_array[np.isnan(self.depth_array)] = 0
      cv2.normalize(self.depth_array, self.depth_array, 0, 1, cv2.NORM_MINMAX)
      #print "depth_array"
      self.image_received = True
      #self.take_photo()
      #print np.max(self.depth_array)
      #print np.min(self.depth_array)
      #print np.nanmax(self.depth_array)
      #print np.nanmin(self.depth_array)
      #cv2.imshow('Depth Image', depth_array)
      #cv2.imshow('Depth Image', color_array)
      #rospy.loginfo(image.shape)
      #cv2.imwrite('/home/saeidfour/camera_rgb.jpg', color_array)
      #cv2.imwrite('/home/saeidfour/camera_depth.pgm', depth_array*255)
      #print "test3"
    except CvBridgeError as e:
      print(e)

  def take_photo(self, img_title,foldername):

    if self.image_received:

      cv2.imwrite(abs_path+'input_images/'+foldername+'/rgb_'+img_title+'.jpg', self.color_array)
      cv2.imwrite(abs_path+'input_images/'+foldername+'/depth_'+img_title+'.pgm', self.depth_array*255)
      print ("test3")
      return True
    else:
      return False

  def amclcallback(self,data):

    #print ('inside callback')
    #print (rospy.get_param('~image_title'))
    self.x1 = data.pose_1.position.x
    #sprint self.x1
    self.y1= data.pose_1.position.y
    self.x2 = data.pose_2.position.x
    self.y2= data.pose_2.position.y
    self.x3 = data.pose_3.position.x
    self.y3= data.pose_3.position.y
    self.x4 = data.pose_4.position.x
    self.y4= data.pose_4.position.y
    #print 'hi'

if __name__ == '__main__':
#def main(args):
  print ("test1")
  ic = image_converter()
  rospy.init_node('image_loc', anonymous=True)
  #try:
  #  rospy.spin()
  #  ic.take_photo()
  #except KeyboardInterrupt:
  #  print("Shutting down")
  #cv2.destroyAllWindows()
  starttime =int(time.time())
  current_date = datetime.datetime.today()
  image_folder_name = str(current_date.year)+'-'+str(current_date.month)+'-'+str(current_date.day)+'-'+str(current_date.hour)+'-'+str(current_date.minute) 
  os.mkdir(abs_path+'input_images/'+image_folder_name)
  #os.mkdir(abs_path+'metadata/'+image_folder_name)

  image_freq = rospy.get_param("image_freq")
  with open(abs_path+'metadata/'+'loc_im_'+image_folder_name+".csv","a+") as f:

      while True and not rospy.is_shutdown():
        rospy.Subscriber("object_loc",fourpose,ic.amclcallback)

        img_title = rospy.get_param('~image_title', str(int(time.time())))

        if ic.take_photo(img_title,image_folder_name):
          print ('hi')
          rospy.loginfo("Saved image " + img_title)
          #print (ic.x1)
          #print (ic.y1)
          line = img_title+','+str(ic.x1)+','+str(ic.y1)+','+str(ic.x2)+','+str(ic.y2)+','+str(ic.x3)+','+str(ic.y3)+','+str(ic.x4)+','+str(ic.y4)+'\n'
          print line
          f.write(line)
        else:
          rospy.loginfo("No images received")

        # Sleep to give the last log messages time to be sent
        time.sleep(image_freq-((time.time() -starttime)%image_freq))






#if __name__ == '__main__':
#    main(sys.argv)
