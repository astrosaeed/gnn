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


current_canvas = []
relation_dict = {}
relation_list=[]
Lb = []
rectangle1 = []
rectangle2 = []
relation_line = []
obj1_text = ""
obj2_text = ""
'''
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = Image.open("test.JPG")
        width, height = load.size
        load = load.resize((592, 592), Image.ANTIALIAS)
        print ('width')
        print (width)
        print ('height')
        print (height)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=20, y=0)
'''
def listbox(root):
    global Lb
	#top = Tk()
    count = 0
    Lb = Listbox(root,width=50,selectmode=SINGLE)
    Lb.width = 50
    for key in relation_list:
        #print (key)
        Lb.insert(count, key)
        count+=1
    Lb.pack()
    Lb.bind('<<ListboxSelect>>',current_relation)
	#top.mainloop()

def current_relation(evt):
    global rectangle1,rectangle2,relation_line,obj1_text,obj2_text
    global current_canvas
    value=str(Lb.get(Lb.curselection()))
    #print (value)
    current_canvas.delete(rectangle1)
    current_canvas.delete(rectangle2)
    current_canvas.delete(relation_line)
    current_canvas.delete(obj1_text)
    current_canvas.delete(obj2_text)
    points_box = relation_dict[value]
    obj1_points =  points_box["obj1"].split("|");
    obj2_points =  points_box["obj2"].split("|");
    obj1_name = points_box["obj1_name"]
    obj2_name = points_box["obj2_name"]

    #obj1_text = current_canvas.create_text(((float(obj1_points[2])-float(obj1_points[0])) / 2) + float(obj1_points[0]), (float(obj1_points[1])*1.5)-10,text=obj1_name,fill='red',font="Times 15 bold")
    #obj2_text = current_canvas.create_text(((float(obj2_points[2])-float(obj2_points[0])) / 2) + float(obj2_points[0]), (float(obj2_points[1])*1.5)-10,text=obj2_name,fill='red',font="Times 15 bold")

    obj1_text = current_canvas.create_text(((float(obj1_points[2])-float(obj1_points[0])) / 2) + float(obj1_points[0]), (float(obj1_points[1])-10),text=obj1_name,fill='red',font="Times 15 bold")
    obj2_text = current_canvas.create_text(((float(obj2_points[2])-float(obj2_points[0])) / 2) + float(obj2_points[0]), (float(obj2_points[1])-10),text=obj2_name,fill='red',font="Times 15 bold")
    
    
    #relation_line = current_canvas.create_line(obj1_points[0], (float(obj1_points[1])*1.5), obj2_points[0], float(obj2_points[1])*1.5, dash=(4, 2), width=5,fill='green')

    relation_line = current_canvas.create_line(obj1_points[0], (float(obj1_points[1])), obj2_points[0], float(obj2_points[1]), dash=(4, 2), width=5,fill='green')


    rectangle1 = current_canvas.create_rectangle(obj1_points[0], (float(obj1_points[1])),obj1_points[2],(float(obj1_points[3]))\
    ,outline='blue',width=2)
    rectangle2 = current_canvas.create_rectangle(obj2_points[0], float(obj2_points[1]), obj2_points[2],float(obj2_points[3]),\
    outline='yellow',width=2)
    '''
    rectangle1 = current_canvas.create_rectangle(obj1_points[0], (float(obj1_points[1])*1.5),obj1_points[2],(float(obj1_points[3])*1.6)\
    ,outline='blue',width=2)
    rectangle2 = current_canvas.create_rectangle(obj2_points[0], float(obj2_points[1])*1.5, obj2_points[2],float(obj2_points[3])*1.6,\
    outline='yellow',width=2)
    '''
def canvas(root):

	#master = Tk()
	w = Canvas(root)
	w.pack()
	canvas_height=200
	canvas_width=200
	y = int(canvas_height / 2)
	w.create_line(0, y, canvas_width,y)
	#mainloop()

def read_csv(filename):
    global relation_dict
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\t')
        current_line = 0
        for row in readCSV:
            if current_line ==0:
                current_line = current_line + 1
            else:
                obj1_coordinates = []
                obj2_coordinates = []
                boundingbox_points = {}
                o1_coordinates = row[5]+"|"+row[6]+"|"+row[7]+"|"+row[8]
                o2_coordinates = row[9]+"|"+row[10]+"|"+row[11]+"|"+row[12]
                boundingbox_points["obj1"] = o1_coordinates
                boundingbox_points["obj2"] = o2_coordinates
                boundingbox_points["obj1_name"] = row[1]
                boundingbox_points["obj2_name"] = row[3]
                relation = "The "+row[1]+" is "+row[2]+" the "+row[3]
                relation_dict[relation] = boundingbox_points
                relation_list.append(relation)
                current_line = current_line + 1
    #print (relation_set)
def custom(filename):

    IM_SCALE = 592

    image_unpadded = Image.open(filename)

    tform = [SquarePad(),Resize(IM_SCALE),ToTensor(), ]

    result =Compose(tform)

        #print (image_unpadded.siz
    a=result(image_unpadded)
    b=F.to_pil_image(a)
    print (type(b))
    #b.save('resized.jpg')
    c = Variable(a.view(-1,3,592,592))
    w, h = image_unpadded.size
    img_scale_factor = IM_SCALE/max(w,h)
    im_size = (IM_SCALE, int(w*img_scale_factor), img_scale_factor)
    return b



    

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
    background = custom(FLAGS_image)
    csvfile = FLAGS_csvfile
    print (background)
    print (csvfile)
    root = Tk()
    #background = 'test1.jpg'
    #background = 'test1.jpg'

    photo = ImageTk.PhotoImage(image= background)
    current_canvas = Canvas(root, width=592, height=592)
    current_canvas.imageList = []
    current_canvas.pack()
    current_canvas.create_image(0, 0, anchor="nw", image=photo)
    current_canvas.imageList.append(photo)

    read_csv(csvfile)
    # app = Window(root)
    app2 = listbox(root)
    app3 = canvas(root)
    root.wm_title("Tkinter window")
    root.geometry("2048x1024")
    root.mainloop()
