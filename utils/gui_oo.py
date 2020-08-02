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


class Application(tk.Frame):

	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.all_bbs=defaultdict(set)
		self.relation_dict = {}
		self.relation_list=[]
		#self.Lb = []
		self.rectangle1 = []
		self.rectangle2 = []
		self.relation_line = []
		self.obj1_text = ""
		self.obj2_text = ""



	def create_listbox(self):
		self.listbox = dict() # lower case for variable name 
		#global Lb
		#top = Tk()
		count = 0
		self.listbox['0'] = Listbox(root,width=30,selectmode=SINGLE)
		
		#self.Lb.width = 50
		'''
		for key in all_images:
			#print (key)
			Lb.insert(count, key)
			count+=1
		'''
		self.listbox['0'].insert(0,'ss')
		self.listbox['0'].pack(side='left')   # shows the position of the widget
		self.listbox['1'] = Listbox(root,width=30,selectmode=SINGLE)
		
		#self.Lb.width = 50
		'''
		for key in all_images:
			#print (key)
			Lb.insert(count, key)
			count+=1
		'''
		self.listbox['1'].insert(0,'ss')
		self.listbox['1'].pack(side='right')   # shows the position of the widget
		#Lb.bind('<<ListboxSelect>>',handler)













root = tk.Tk()
app = Application(root)
app.create_listbox()
root.title("Output Formats")
root.geometry("2048x1024")
app.mainloop()