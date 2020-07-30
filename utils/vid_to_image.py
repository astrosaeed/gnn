import cv2
from PIL import Image
import glob
import psutil
import time


def extract():

	
	vidcap = cv2.VideoCapture('2020-01-21 12-08-54.mp4')
	success,image = vidcap.read()
	count = 0
	while success:
	  vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
	  cv2.imwrite("%d_frame.jpg" % count, image)     # save frame as JPEG file      
	  success,image = vidcap.read()
	  print('Read a new frame: ', success)
	  count += 5



def read_single_image():
	all_images = sorted(glob.glob('*.jpg'))
	print (all_images[0:6])
	for path in all_images:
	  
	
		img = Image.open(path)
		print (img.size)
		top = 0
		left = img.size[0]/2 - img.size[0]/4
		bottom =top + img.size[1]
		right= left + img.size[0]/2
		
		front = img.crop((left,top,right,bottom))

		
		
		front.show()

		user_input = input('Enter the command:\n')	
		if user_input =='k':
			close_window()
	

def close_window():
	for proc in psutil.process_iter():
		if proc.name() == "display":
			proc.kill()




if __name__ == '__main__':
	extract()