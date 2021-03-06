from tkinter import *
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

X_IMAGE =550
#parent_folder = Path('/home/saeid/ai2thor/Kitchens_AI2Thor/')
#current_folder =Path('/home/saeid/ai2thor/Kitchens_AI2Thor/FloorPlan13')
parent_folder = Path('/home/saeid/gnn/data')
current_folder =parent_folder/'aa/images' 
current_image = current_folder/'DSC_6999.JPG'

root = Tk()

current_canvas = Canvas(root, width=592, height=592)
current_canvas.imageList = []
current_canvas.pack(expand=1, fill=BOTH) # We need these args to move the box
#current_canvas.create_image(400, 0, anchor="nw", image=photo)





all_bbs=defaultdict(set)
relation_dict = {}
relation_list=[]
Lb = []
rectangle1 = []
rectangle2 = []
relation_line = []
obj1_text = ""
obj2_text = ""



def listbox(root):
	global Lb
	#top = Tk()
	count = 0
	Lb = Listbox(root,width=70,height=83, selectmode=SINGLE)
	Lb.width = 80
	#s= " "
	for key in relation_list:
		#print (key)
		Lb.insert(count, key)
		count+=1
	Lb.pack()
	Lb.place(x=10,y=0) # For absolute positioning
	# http://zetcode.com/tkinter/layout/
	Lb.bind('<<ListboxSelect>>',current_relation)
	#top.mainloop()
def res_listbox(root):
	global Lb2
	
	count = 0
	Lb2 = Listbox(root,width=80,height=40, selectmode=SINGLE)
	Lb2.width = 140
	s= "The table is empty <-- nothing on table"
	#for key in relation_list:
	#	#print (key)
	Lb2.insert(count,s)
	#	count+=1
	Lb2.pack()
	Lb2.place(x=1200,y=0) # For absolute positioning
	# http://zetcode.com/tkinter/layout/
	#Lb.bind('<<ListboxSelect>>',current_relation)
	#top.mainloop()


def current_relation(evt):
	global rectangle1,rectangle2,relation_line,obj1_text,obj2_text

	key=str(Lb.get(Lb.curselection()))
	#print (value)
	current_canvas.delete(rectangle1)
	current_canvas.delete(rectangle2)
	current_canvas.delete(relation_line)
	current_canvas.delete(obj1_text)
	current_canvas.delete(obj2_text)
	points_box = relation_dict[key]
	obj1_points =  points_box["obj1"]
	obj2_points =  points_box["obj2"]
	obj1_name = points_box["obj1_name"]
	obj2_name = points_box["obj2_name"]

	
	obj1_text = current_canvas.create_text(((float(obj1_points[2])-float(obj1_points[0])) / 2) + float(obj1_points[0]), (float(obj1_points[1])-10),text=obj1_name,fill='red',font="Times 15 bold")
	obj2_text = current_canvas.create_text(((float(obj2_points[2])-float(obj2_points[0])) / 2) + float(obj2_points[0]), (float(obj2_points[1])-10),text=obj2_name,fill='red',font="Times 15 bold")
	
	
	

	relation_line = current_canvas.create_line(obj1_points[0], (float(obj1_points[1])), obj2_points[0], float(obj2_points[1]), dash=(4, 2), width=5,fill='green')


	rectangle1 = current_canvas.create_rectangle(obj1_points[0], (float(obj1_points[1])),obj1_points[2],(float(obj1_points[3]))\
	,outline='blue',width=2)
	rectangle2 = current_canvas.create_rectangle(obj2_points[0], float(obj2_points[1]), obj2_points[2],float(obj2_points[3]),\
	outline='yellow',width=2)
	current_canvas.move(rectangle1,X_IMAGE,0)
	current_canvas.move(rectangle2,X_IMAGE,0)
	current_canvas.move(relation_line,X_IMAGE,0)
	current_canvas.move(obj1_text,X_IMAGE,0)
	current_canvas.move(obj2_text,X_IMAGE,0)

def update_df_with_index(df):
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

def read_csv(filename):
	global relation_dict
	relation_list.clear()
	relation_dict.clear()
	df = pd.read_csv(filename,delimiter='\t')
	print (df.head())
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
	df = update_df_with_index(df)
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

		relation_dict[relation] = boundingbox_points
		relation_list.append(relation)
	

def panaroma():
	IM_SCALE = 200

	all_images= [e for e in (current_folder).iterdir()]
	tform = [SquarePad(),Resize(IM_SCALE),ToTensor(), ]

	result =Compose(tform)

	im_list=[]
	

	for im in all_images:
		image_unpadded = Image.open(im)
		a=result(image_unpadded)
		b=F.to_pil_image(a)
		im_list.append(b)
	pan_img = get_concat_h(im_list[0], im_list[1],im_list[2],im_list[3],im_list[4],im_list[5]) 	

	return pan_img

def pan_canvas():
	big_image= panaroma()
	photo2 = ImageTk.PhotoImage(image= big_image)
	item2 = pan_canvas.create_image(0, 0,anchor="nw" ,image=photo2)
	pan_canvas.move(item2,X_IMAGE,700) # https://stackoverflow.com/questions/23275445/move-an-image-in-python-using-tkinter
	pan_canvas.imageList.append(photo)


def get_concat_h(im1, im2,im3,im4,im5,im6):
    dst = Image.new('RGB', (im1.width*6, im1.height)) #hardcoded
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.paste(im3, (2*im1.width, 0))
    dst.paste(im4, (3*im1.width, 0))
    dst.paste(im5, (4*im1.width, 0))
    dst.paste(im6, (5*im1.width, 0))
    return dst

	
def custom(filename):

	IM_SCALE = 592

	image_unpadded = Image.open(filename)

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

def appear_photo(image, csvfile):

	background = custom(image)
	photo = ImageTk.PhotoImage(image= background)
	item = current_canvas.create_image(0, 0,anchor="nw" ,image=photo)
	current_canvas.move(item,X_IMAGE,0) # https://stackoverflow.com/questions/23275445/move-an-image-in-python-using-tkinter
	current_canvas.imageList.append(photo)    	

	read_csv(csvfile)
	
def next_folder(root):
	b = Button(root, text="next folder", command=next_folder_handler)
	b.pack(side='left')

def next_folder_handler():
	next_folder = all_folders[(all_folders.index(current_folder)+1)%len(all_folders)] 
	all_images= [e for e in next_folder.iterdir()]
	background=all_images[0]
   # print (background)
	csvfile=FLAGS_csvfile
	appear_photo(background,csvfile)

def next_photo(root):
	b = Button(root, text="<-- Left", command=next_photo_handler)
	#b.pack(side='left')
	b.pack()
	b.place(x=650,y=580)

def previous_photo(root):
	b = Button(root, text="Right -->", command=previous_photo_handler)
	#b.pack(side='left')
	b.pack()
	b.place(x=800,y=580)

def next_photo_handler():
	global current_image ,current_csv
	all_images= [e for e in sorted(current_folder.iterdir())]
	all_csvs= [e for e in sorted((parent_folder/'aa/rels').iterdir())]
	
	idx= (all_images.index(current_image)+1)%len(all_images)
	
	next_image=all_images[(all_images.index(current_image)+1)%len(all_images)] 
	next_csv = all_csvs[(all_csvs.index(current_csv)+1)%len(all_csvs)]
	current_image = next_image
	#print (background)
	current_csv = next_csv
	print (current_csv)
	Lb.delete(0,'end')
	Lb2.delete(0,'end')
	appear_photo(current_image,current_csv)
	count = 0
	print (relation_list[0:2])
	for key in relation_list:
		#print (key)
		Lb.insert(count, key)
		count+=1
	if '7001' in current_image.as_posix():
		Lb2.insert(0, "table is crowded <-- books and laptop on table")
	elif '7005' in current_image.as_posix():
		Lb2.insert(0, "Man is busy <-- holding book")
		Lb2.insert(1, "Man is a student <-- bag")
		Lb2.insert(2, "It might be warm < -- wearing short")
		Lb2.insert(3, "Man with the hat is sitting on the chair next to a bag and holding a book")
	elif '6999' in current_image.as_posix():
		Lb2.insert(0, "The table is empty <-- nothing on table")

def previous_photo_handler():
	global current_image ,current_csv
	all_images= [e for e in sorted(current_folder.iterdir())]
	all_csvs= [e for e in sorted((parent_folder/'aa/rels').iterdir())]
	
	idx= (all_images.index(current_image)-1)%len(all_images)
	
	prev_image=all_images[(all_images.index(current_image)-1)%len(all_images)] 
	prev_csv = all_csvs[(all_csvs.index(current_csv)-1)%len(all_csvs)]
	current_image = prev_image
	#print (background)
	current_csv = prev_csv
	print (current_csv)
	Lb.delete(0,'end')
	Lb2.delete(0,'end')
	appear_photo(current_image,current_csv)
	count = 0
	#print (relation_list[0:2])
	for key in relation_list:
		#print (key)
		Lb.insert(count, key)
		count+=1
	if '7001' in current_image.as_posix():
		Lb2.insert(0, "table is crowded")
	elif '7005' in current_image.as_posix():
		Lb2.insert(0, "Man is busy (<-- holding book)")
		Lb2.insert(1, "Man is a student <-- bag")
		Lb2.insert(2, "It might be warm")
		Lb2.insert(3, "Man with the hat is sitting on the chair next to a bag and holding a book")
	elif '6999' in current_image.as_posix():
		Lb2.insert(0, "The table is empty <-- nothing on table")

	#update_listbox()

'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--image', type=str, required=True,
						help="image")
	parser.add_argument('--csvfile', type=str, required=True,
						help="ralations file")
	args = parser.parse_args()
	for k, v in vars(args).items():
		globals()['FLAGS_%s' % k] = v
	#main()
'''
#current_folder =Path('/home/saeid/ai2thor/Kitchens_AI2Thor/FloorPlan13') 


#print (csvfile)




all_folders = [e for e in parent_folder.iterdir() if e.is_dir()]
current_csv = parent_folder/'aa/rels/final_outputs_DSC_6999.JPG.csv'

appear_photo(current_image,current_csv)
#pan_canvas()
#pan_canvas = Canvas(root, width=1200, height=400)
#pan_canvas.pack()
#pan_canvas.imageList = []
#pan_canvas.pack(expand=1, fill=BOTH)

#big_image = Image.open('panaroma.jpg')
#big_image.thumbnail((600,200), Image.ANTIALIAS)
#photo2 = ImageTk.PhotoImage(image= big_image)

#item2 = current_canvas.create_image(0, 500,anchor="nw" ,image=photo2)
#pan_canvas.move(item2,500,800) # https://stackoverflow.com/questions/23275445/move-an-image-in-python-using-tkinter
#pan_canvas.imageList.append(photo2)




# app = Window(root)
app2 = listbox(root)
app3=next_photo(root)
app4=previous_photo(root)
app5 = res_listbox(root)
root.wm_title("Tkinter window")
root.geometry("2048x1024")
root.mainloop()
