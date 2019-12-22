import roslib
#roslib.load_manifest('kinect_pylistener')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import numpy as np
import message_filters
import time

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    image_sub = message_filters.Subscriber("/camera/rgb/image_raw", Image)
    depth_sub = message_filters.Subscriber("/camera/depth/image_raw", Image)
    self.ts = message_filters.ApproximateTimeSynchronizer([image_sub, depth_sub], 1, 1)
    self.ts.registerCallback(self.callback)
    print "test2"
    self.image_received= False
    self.color_array = None
    self.depth_array = None


  def callback(self,rgb_data, depth_data):
    try:
      image = self.bridge.imgmsg_to_cv2(rgb_data, "bgr8")
      depth_image = self.bridge.imgmsg_to_cv2(depth_data, "passthrough")
      self.depth_array = np.array(depth_image, dtype=np.float32)
      self.color_array = np.array(image, dtype=np.uint8)
      self.depth_array[np.isnan(self.depth_array)] = 0
      cv2.normalize(self.depth_array, self.depth_array, 0, 1, cv2.NORM_MINMAX)
      print "depth_array"
      self.image_received = True
      #self.take_photo()
      print np.max(self.depth_array)
      print np.min(self.depth_array)
      print np.nanmax(self.depth_array)
      print np.nanmin(self.depth_array)
      #cv2.imshow('Depth Image', depth_array)
      #cv2.imshow('Depth Image', color_array)
      #rospy.loginfo(image.shape)
      #cv2.imwrite('/home/saeidfour/camera_rgb.jpg', color_array)
      #cv2.imwrite('/home/saeidfour/camera_depth.pgm', depth_array*255)
      print "test3"
    except CvBridgeError as e:
      print(e)

  def take_photo(self):

    if self.image_received:

      cv2.imwrite('/home/saeidfour/camera_rgb.jpg', self.color_array)
      cv2.imwrite('/home/saeidfour/camera_depth.pgm', self.depth_array*255)
      print "test3"


def main(args):
  print "test1"
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  #try:
  #  rospy.spin()
  #  ic.take_photo()
  #except KeyboardInterrupt:
  #  print("Shutting down")
  #cv2.destroyAllWindows()


  while True and not rospy.is_shutdown():

    img_title = rospy.get_param('~image_title', 'photo_'+str(int(time.time()))+'.jpg')

    if ic.take_photo(img_title):
      rospy.loginfo("Saved image " + img_title)
      #print (camera.x)
      #print (camera.y)
      #f.write(str(camera.x)+','+str(camera.y)+','+img_title+'\n')
    else:
      rospy.loginfo("No images received")

    # Sleep to give the last log messages time to be sent
    time.sleep(5.0-((time.time() -starttime)%5.0))






if __name__ == '__main__':
    main(sys.argv)
