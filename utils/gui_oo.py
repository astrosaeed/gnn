import glob
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import os
import csv
from PIL import Image, ImageTk
import argparse
import torch
from PIL import Image
from torch.utils.data import Dataset
from image_transforms import SquarePad, Grayscale, Brightness, Sharpness, Contrast,RandomOrder, Hue, random_crop
from torchvision.transforms import Resize, Compose, ToTensor, Normalize
import torchvision.transforms.functional as F
from torch.autograd import Variable
import numpy as np
import os
import pandas as pd
from pathlib import Path
from collections import defaultdict
import re
import glob
from ta_env import init_tr, init_cord, NUM_LOCS

all_bbs=defaultdict(set)
#parent_folder = Path('/home/saeid/Dropbox/gnn/data')
parent_folder = Path('../gnn/data')
all_folders = [e for e in parent_folder.iterdir() if e.is_dir()]
current_csv = parent_folder/'ta_area/front/rels/0.csv'
im_ext= 'JPG'
X_IMAGE =50
annot_shift = 592+50
#parent_folder = Path('/home/saeid/ai2thor/Kitchens_AI2Thor/')
#current_folder =Path('/home/saeid/ai2thor/Kitchens_AI2Thor/FloorPlan13')

current_folder =parent_folder/'ta_area' 
#current_folder =parent_folder/'home' 
current_image = current_folder/('0.'+im_ext)

class Application(tk.Frame):

	def __init__(self, master,current_image,current_csv):
		tk.Frame.__init__(self, master)
		self.all_bbs=defaultdict(set)
		self.relation_dict = {}
		self.relation_list=[]
		#self.Lb = []
		self.rectangle1 = []
		self.rectangle2 = []
		self.relation_line = None
		self.obj1_text = ""
		self.obj2_text = ""
		self.current_image= current_image
		self.current_csv= current_csv
		self.tr = init_tr(NUM_LOCS)
		self.current_cord= (0,0)
		self.cord= init_cord()

	

	def create_listbox(self):
		self.listbox = dict() # lower case for variable name 
		#global Lb
		#top = Tk()
		count = 0
		self.listbox['0'] = Listbox(root,width=40,selectmode=SINGLE)
		
		#self.Lb.width = 50
		'''
		for key in all_images:
			#print (key)
			Lb.insert(count, key)
			count+=1
		'''
		self.listbox['0'].insert(0,'ss')
		self.listbox['0'].pack(side='left')   # shows the position of the widget
		
		
		for key in self.relation_list:
			#print (key)
			self.listbox['0'].insert(count, key)
			count+=1
		self.listbox['0'].pack()
		self.listbox['0'].place(x=5,y=600) # For absolute positioning
		# http://zetcode.com/tkinter/layout/
		self.listbox['0'].bind('<<ListboxSelect>>',self.current_relation)

		self.listbox['1'] = Listbox(root,width=30,selectmode=SINGLE)
		self.listbox['1'].pack()
		self.listbox['1'].place(x=5,y=800) # For absolute positioning
		self.listbox['1'].insert(0, 'LOG')
		self.listbox['1'].insert(1, 'current state: '+str(self.current_cord))

	def create_canvas(self):

		self.canvas = dict()
		self.canvas['0'] = Canvas(root, width=592, height=592)
		self.canvas['0'].imageList = []
		self.canvas['0'].pack(expand=1, fill=BOTH) # We need these args to move the box


	def current_relation(self,evt):
		

		key=str(self.listbox['0'].get(self.listbox['0'].curselection()))
		#print (value)
		self.canvas['0'].delete(self.rectangle1)
		self.canvas['0'].delete(self.rectangle2)
		self.canvas['0'].delete(self.relation_line)
		self.canvas['0'].delete(self.obj1_text)
		self.canvas['0'].delete(self.obj2_text)
		
		points_box = self.relation_dict[key]
		obj1_points =  points_box["obj1"]
		obj2_points =  points_box["obj2"]
		obj1_name = points_box["obj1_name"]
		obj2_name = points_box["obj2_name"]

		
		self.obj1_text = self.canvas['0'].create_text(((float(obj1_points[2])-float(obj1_points[0])) / 2) + float(obj1_points[0]), (float(obj1_points[1])-10),text=obj1_name,fill='red',font="Times 15 bold")
		self.obj2_text = self.canvas['0'].create_text(((float(obj2_points[2])-float(obj2_points[0])) / 2) + float(obj2_points[0]), (float(obj2_points[1])-10),text=obj2_name,fill='red',font="Times 15 bold")
		
		
		

		self.relation_line = self.canvas['0'].create_line(obj1_points[0], (float(obj1_points[1])), obj2_points[0], float(obj2_points[1]), dash=(4, 2), width=5,fill='green')


		self.rectangle1 = self.canvas['0'].create_rectangle(obj1_points[0], (float(obj1_points[1])),obj1_points[2],(float(obj1_points[3]))\
		,outline='blue',width=2)
		self.rectangle2 = self.canvas['0'].create_rectangle(obj2_points[0], float(obj2_points[1]), obj2_points[2],float(obj2_points[3]),\
		outline='yellow',width=2)
		self.canvas['0'].move(self.rectangle1,annot_shift,0)
		self.canvas['0'].move(self.rectangle2,annot_shift,0)
		self.canvas['0'].move(self.relation_line,annot_shift,0)
		self.canvas['0'].move(self.obj1_text,annot_shift,0)
		self.canvas['0'].move(self.obj2_text,annot_shift,0)


	def resize(self,img,direction):

	#img = Image.open(path)
		#print (img.size)

		top = img.size[0]/6
		bottom =top + img.size[1]/2
		#print (bottom)
		if direction=='front':    

			left = img.size[0]/2 - img.size[0]/8
			#print ('left ', left)
			right= img.size[0]/2 + img.size[0]/8
			#print ('right  ', right)
			result = img.crop((left,top,right,bottom))

		elif direction=='back':
		 
			left = 0
			#print ('left ', left)
			right= img.size[0]/2 - img.size[0]/8 - img.size[0]/4
			#print ('right  ', right)
			img1 = img.crop((left,top,right,bottom))

			left = img.size[0]/2 + img.size[0]/8 + img.size[0]/4
			#print ('left ', left)
			right= img.size[0]
			#print ('right  ', right)
			img2= img.crop((left,top,right,bottom))

			(width1, height1) = img1.size
			(width2, height2) = img2.size

			result_width = width1 + width2
			result_height = max(height1, height2)

			result = Image.new('RGB', (result_width, result_height))
			result.paste(im=img2, box=(0, 0))
			result.paste(im=img1, box=(width1, 0))
		
		elif direction=='right':
		 
			left = img.size[0]/2 + img.size[0]/8
			#print ('left ', left)
			right= img.size[0]/2 + img.size[0]/8 + img.size[0]/4 
			#print ('right  ', right)
			result= img.crop((left,top,right,bottom))

		elif direction=='left':
			left = img.size[0]/2 - img.size[0]/8 - img.size[0]/4
			#print ('left ', left)
			right= img.size[0]/2 - img.size[0]/8
			#print ('right  ', right)
		   
			result= img.crop((left,top,right,bottom))
		'''    
		result_width = width1
		result_height = 3*height2

		result = Image.new('RGB', (result_width, result_height))
		result.paste(im=result_front, box=(0, 0))
		result.paste(im=result_back, box=(0, 2*height2))
		'''

		return result

	def read_csv(self, filename):
		#global relation_dict
		
		df = pd.read_csv(filename,delimiter='\t')
		#print (df.head())
		df['obj1_x_mean'] = df[['obj1_1','obj1_3']].mean(axis=1).astype('int').astype('str')
		df['obj1_y_mean'] = df[['obj1_2','obj1_4']].mean(axis=1).astype('int').astype('str')
		df['obj2_x_mean'] = df[['obj2_1','obj2_3']].mean(axis=1).astype('int').astype('str')
		df['obj2_y_mean'] = df[['obj2_2','obj2_4']].mean(axis=1).astype('int').astype('str')

		df= df[df['prob']>0.1]
		df = df[df.obj2 != "house" ]
		df = df[df.obj2 != "room"]
		df = df[df.obj2 != "leg"]
		df = df[df.obj1 != "leg"]
		df = df[df.obj1 != "window"]
		df = df[df.obj2 != "window"]
		df = df[df.obj1 != "tile"]
		df = df[df.obj2 != "tile"]
		df = self.update_df_with_index(df)
		for index, row in df.iterrows():
			obj1_coordinates = []
			obj2_coordinates = []
			boundingbox_points = {}
			boundingbox_points["obj1"]  = [row['obj1_1'],row['obj1_2'],row['obj1_3'],row['obj1_4']]
			boundingbox_points["obj2"] = [row['obj2_1'],row['obj2_2'],row['obj2_3'],row['obj2_4']]
			boundingbox_points["obj1_name"] = row['obj1']
			boundingbox_points["obj2_name"] = row['obj2']
			#relation = str(index)+"- "+row['obj1_x_mean']+","+ row['obj1_y_mean']+"    "+row['obj1']+ "     "\
			#+row['predicate']+"     "+row['obj2'] +"     ("+row['obj2_x_mean']+","+row['obj2_x_mean']+")    "+ str(round(float(row['prob']),2))
			relation = str(index)+"- "+row['obj1']+ "     "\
			+row['predicate']+"      "+row['obj2'] +"      "+ str(round(float(row['prob']),2))

			self.relation_dict[relation] = boundingbox_points
			self.relation_list.append(relation)

	def custom(self, filename,direction):

		IM_SCALE = 592


		image = Image.open(filename)

		image_unpadded = self.resize(image,direction)

		tform = [SquarePad(),Resize(IM_SCALE),ToTensor(), ]

		result =Compose(tform)

			#print (image_unpadded.siz
		a=result(image_unpadded)
		b=F.to_pil_image(a)
		#print (type(b))
		#b.save('resized.jpg')
		c = Variable(a.view(-1,3,592,592))
		w, h = image_unpadded.size
		img_scale_factor = IM_SCALE/max(w,h)
		im_size = (IM_SCALE, int(w*img_scale_factor), img_scale_factor)
		return b

	def appear_photo(self, image, csvfile):

		self.image = image 
		self.csvfile =csvfile
		front = self.custom(image,'front')
		print ('front size', front.size)
		back = self.custom(image,'back')
		right = self.custom(image,'right')
		left = self.custom(image,'left')

		result_width = 3*front.size[0]+8
		result_height = 2*front.size[1]

		result = Image.new('RGB', (result_width, result_height))
		result.paste(im=front, box=(front.size[0]+4, 0))
		result.paste(im=back, box=(front.size[0]+4, int(front.size[0])+3 ))
		result.paste(im=right, box=(2*front.size[0]+8,0))
		result.paste(im=left, box=(0, 0))

		photo = ImageTk.PhotoImage(image= result)
		item = self.canvas['0'].create_image(0, 0,anchor="nw" ,image=photo)
		self.canvas['0'].move(item,X_IMAGE,0) # https://stackoverflow.com/questions/23275445/move-an-image-in-python-using-tkinter
		self.canvas['0'].imageList.append(photo)

		self.relation_list.clear()
		self.relation_dict.clear()    	
		self.read_csv(csvfile)

	def left_photo(self,root):
		b = Button(root, text="<-- Left", command=self.left_photo_handler)
		#b.pack(side='left')
		b.pack()
		b.place(x=400,y=680)

	def forward_photo(self,root):
		b = Button(root, text="Forward", command=self.forward_photo_handler)
		#b.pack(side='left')
		b.pack()
		b.place(x=475,y=650)

	def back_photo(self,root):
		b = Button(root, text="Backward", command=self.back_photo_handler)
		#b.pack(side='left')
		b.pack()
		b.place(x=475,y=710)

	def right_photo(self,root):
		b = Button(root, text="Right -->", command=self.right_photo_handler)
		#b.pack(side='left')
		b.pack()
		b.place(x=550,y=680)

	def left_photo_handler(self):
		# 0 front 1 left 2 right 3 back

		x,y = self.current_cord
		if  (x+1,y) in self.cord.keys():
			if self.tr[1,self.cord[(x,y)],self.cord[(x+1,y)]]:
				
				self.current_cord = (x+1,y)
				self.listbox['1'].delete(1, 2)
				self.listbox['1'].insert(1, 'current state: '+str(self.current_cord))
				#all_images= [e for e in sorted(current_folder.iterdir())]
				#all_csvs= [e for e in sorted((parent_folder/'aa/rels').iterdir())]
				self.current_cord = (x+1,y)
				#idx= (all_images.index(self.current_image)+1)%len(all_images)
				#idx = current_image.stem
				new_idx = str(self.cord[(x+1,y)]) 
				#next_image=all_images[(all_images.index(self.current_image)+1)%len(all_images)] 
				#next_csv = all_csvs[(all_csvs.index(self.current_csv)+1)%len(all_csvs)]
				self.current_image = current_folder/(str(new_idx)+'.'+im_ext)
				#print (background)
				#self.current_csv = next_csv
				print (self.current_csv)
				#Lb.delete(0,'end')
				#Lb2.delete(0,'end')
				self.appear_photo(self.current_image, self.current_csv)
			else:
				print ('No transition')
				self.listbox['1'].delete(2, 3)
				self.listbox['1'].insert(2, 'error message: No transition')
		else:
			print ('Not in env')
			self.listbox['1'].delete(2, 3)
			self.listbox['1'].insert(2, 'error message: Not in env')
	def forward_photo_handler(self):
		x,y = self.current_cord
		if  (x,y+1) in self.cord.keys():
			if self.tr[0,self.cord[(x,y)],self.cord[(x,y+1)]]:
				
				self.current_cord = (x,y+1)
				self.listbox['1'].delete(1, 2)
				self.listbox['1'].insert(1, 'current state: '+str(self.current_cord))
				#all_images= [e for e in sorted(current_folder.iterdir())]
				all_csvs= [e for e in sorted((parent_folder/'aa/rels').iterdir())]
				
				#idx= (all_images.index(self.current_image)+1)%len(all_images)
				#idx = current_image.stem
				new_idx = str(self.cord[(x,y+1)]) 
				#next_image=all_images[(all_images.index(self.current_image)+1)%len(all_images)] 
				#next_csv = all_csvs[(all_csvs.index(self.current_csv)+1)%len(all_csvs)]
				self.current_image = current_folder/(str(new_idx)+'.'+im_ext)
				#print (background)
				#self.current_csv = next_csv
				print (self.current_csv)
				#Lb.delete(0,'end')
				#Lb2.delete(0,'end')
				self.appear_photo(self.current_image, self.current_csv)
			else:
				print ('No transition')
				self.listbox['1'].delete(2, 3)
				self.listbox['1'].insert(2, 'error message: No transition')
		else:
			print ('Not in env')
			self.listbox['1'].delete(2, 3)
			self.listbox['1'].insert(2, 'error message: Not in env')
		
	def back_photo_handler(self):
		x,y = self.current_cord
		if  (x,y-1) in self.cord.keys():
			if self.tr[2,self.cord[(x,y)],self.cord[(x,y-1)]]:
				
				self.current_cord = (x,y-1)
				self.listbox['1'].delete(1, 2)
				self.listbox['1'].insert(1, 'current state: '+str(self.current_cord))
				#all_images= [e for e in sorted(current_folder.iterdir())]
				#all_csvs= [e for e in sorted((parent_folder/'aa/rels').iterdir())]
				
				#idx= (all_images.index(self.current_image)+1)%len(all_images)
				#idx = current_image.stem
				new_idx = str(self.cord[(x,y-1)]) 
				#next_image=all_images[(all_images.index(self.current_image)+1)%len(all_images)] 
				#next_csv = all_csvs[(all_csvs.index(self.current_csv)+1)%len(all_csvs)]
				self.current_image = current_folder/(str(new_idx)+'.'+im_ext)
				#print (background)
				#self.current_csv = next_csv
				print (self.current_csv)
				#Lb.delete(0,'end')
				#Lb2.delete(0,'end')
				self.appear_photo(self.current_image, self.current_csv)
			else:
				print ('No transition')
				self.listbox['1'].delete(2, 3)
				self.listbox['1'].insert(2, 'error message: No transition')
		
		else:
			print ('Not in env')
			self.listbox['1'].delete(2, 3)
			self.listbox['1'].insert(2, 'error message: Not in env')

	def right_photo_handler(self):
		
		x,y = self.current_cord
		print ('x,y is:',x,y)
		if  (x-1,y) in self.cord.keys():
			if self.tr[3,self.cord[(x,y)],self.cord[(x-1,y)]]:
				
				self.current_cord = (x-1,y)
				self.listbox['1'].delete(1, 2)
				self.listbox['1'].insert(1, 'current state: '+str(self.current_cord))
				#all_images= [e for e in sorted(current_folder.iterdir())]
				#all_csvs= [e for e in sorted((parent_folder/'aa/rels').iterdir())]
				
				#idx= (all_images.index(self.current_image)+1)%len(all_images)
				#idx = current_image.stem
				new_idx = str(self.cord[(x-1,y)]) 
				#next_image=all_images[(all_images.index(self.current_image)+1)%len(all_images)] 
				#next_csv = all_csvs[(all_csvs.index(self.current_csv)+1)%len(all_csvs)]
				self.current_image = current_folder/(str(new_idx)+'.'+im_ext)
				#print (background)
				#self.current_csv = next_csv
				#print (self.current_csv)
				#Lb.delete(0,'end')
				#Lb2.delete(0,'end')
				self.appear_photo(self.current_image, self.current_csv)
			else:
				print ('No transition')
				self.listbox['1'].delete(2, 3)
				self.listbox['1'].insert(2, 'error message: No transition')

		else:
			print ('Not in env')
			self.listbox['1'].delete(2, 3)
			self.listbox['1'].insert(2, 'error message: Not in env')

	def update_df_with_index(self,df):
	#df = df.copy(deep=True)
		for index, row in df.iterrows():

			all_bbs[row['obj1']].add((row['obj1_1'],row['obj1_2'],row['obj1_3'],row['obj1_4']))
			#all_bbs[(row['obj1_1'],row['obj1_2'],row['obj1_3'],row['obj1_4'])]+=1
			df.loc[index,'obj1']= str(row['obj1'])+'_'+ str(len(all_bbs[row['obj1']]))
			#print (df.loc[index,'obj1_1'])
			#print (df.head())
			#input()
			#all_bbs[(row['obj2_1'],row['obj2_2'],row['obj2_3'],row['obj2_4'])]+=1
			all_bbs[row['obj2']].add((row['obj2_1'],row['obj2_2'],row['obj2_3'],row['obj2_4']))
			df.loc[index,'obj2']= str(row['obj2'])+'_'+ str(len(all_bbs[row['obj2']]))
	#input()
		return df




root = tk.Tk()
app = Application(root,current_image,current_csv)

app.create_canvas()
app.appear_photo(current_image,current_csv)
app.create_listbox()
app.left_photo(root)
app.right_photo(root)
app.forward_photo(root)
app.back_photo(root)
root.title("Output Formats")
root.geometry("2048x1024")
app.mainloop()