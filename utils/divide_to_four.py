'''
This file gets a rectangular projected 360 image and diveds it into 4 images 
of front, right, left, and back
'''

import glob
from tkinter import *
from PIL import Image, ImageTk
import os


def resize(path):

    img = Image.open(path)
    print (img.size)

    top = img.size[0]/4
    bottom =top + img.size[1]/2
    print (bottom)
    direction='front'    

    left = img.size[0]/2 - img.size[0]/4
    print ('left ', left)
    right= img.size[0]/2 + img.size[0]/4
    print ('right  ', right)
    result = img.crop((left,top,right,bottom))
    result.save(direction+'-'+path) 


    direction='back'
     
    left = img.size[0]/2 + img.size[0]/4
    print ('left ', left)
    right= img.size[0]
    print ('right  ', right)
    img1 = img.crop((left,top,right,bottom))


    left = 0
    print ('left ', left)
    right= img.size[0]/2 - img.size[0]/4
    print ('right  ', right)
    img2= img.crop((left,top,right,bottom))

    (width1, height1) = img1.size
    (width2, height2) = img2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=img1, box=(0, 0))
    result.paste(im=img2, box=(width1, 0))

    result.save(direction+'-'+path)

    direction='right'
     
    left = img.size[0]/2
    print ('left ', left)
    right= img.size[0] 
    print ('right  ', right)
    result= img.crop((left,top,right,bottom))
    result.save(direction+'-'+path)

    direction='left'
    
    left = 0
    print ('left ', left)
    right= img.size[0]/2
    print ('right  ', right)
   
    result= img.crop((left,top,right,bottom))
        
    result.save(direction+'-'+path)


all_images = sorted(glob.glob('*.jpg'),key=os.path.getmtime)


for image in all_images:

	resize(image)

