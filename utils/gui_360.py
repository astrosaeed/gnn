import glob
from tkinter import *
from PIL import Image, ImageTk
import os

relation_list = ['frame_0.jpg','frame_100.jpg']

root = Tk()

current_canvas = Canvas(root, width=1500, height=1200)
current_canvas.imageList = []
current_canvas.pack(side='right')

all_images = sorted(glob.glob('union/*.jpg'),key=os.path.getmtime)

def listbox(root):
    global Lb
    #top = Tk()
    count = 0
    Lb = Listbox(root,width=30,selectmode=SINGLE)
    Lb.width = 50
    for key in all_images:
        #print (key)
        Lb.insert(count, key)
        count+=1
    Lb.pack(side='left')   # shows the position of the widget
    Lb.bind('<<ListboxSelect>>',handler)
  


def resize(path, direction):

    img = Image.open(path)
    print (img.size)

    top = img.size[0]/6
    bottom =top + img.size[1]/2
    print (bottom)
    if direction=='front':    

        left = img.size[0]/2 - img.size[0]/4
        print ('left ', left)
        right= img.size[0]/2 + img.size[0]/4
        print ('right  ', right)
        result = img.crop((left,top,right,bottom))

    elif direction=='back':
     
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

    elif direction=='right':
     
        left = img.size[0]/2
        print ('left ', left)
        right= img.size[0] 
        print ('right  ', right)
        result= img.crop((left,top,right,bottom))

    elif direction=='left':
        left = 0
        print ('left ', left)
        right= img.size[0]/2
        print ('right  ', right)
       
        result= img.crop((left,top,right,bottom))
        

    return result

def handler(evt):

    value=str(Lb.get(Lb.curselection()))
    print (value)
    appear_photo(value,'front')

def canvas(root):

    #master = Tk()
    w = Canvas(root)
    w.pack()
    canvas_height=200
    canvas_width=200
    y = int(canvas_height / 2)
    w.create_line(0, y, canvas_width,y)
    #mainloop()

def back_button(root):
    b = Button(root, text="Back", command=back_handler)
    b.pack(side='left')

def right_button(root):
    b = Button(root, text="Right", command=right_handler)
    b.pack(side='left')

def left_button(root):
    b = Button(root, text="Left", command=left_handler)
    b.pack(side='left')

def back_handler():
    value=str(Lb.get(Lb.curselection()))
    print (value)
    appear_photo(value,'back')

def right_handler():
    value=str(Lb.get(Lb.curselection()))
    print (value)
    appear_photo(value,'right')
def left_handler():
    value=str(Lb.get(Lb.curselection()))
    print (value)
    appear_photo(value,'left')

def appear_photo(filename,direction):
    image_unpadded = resize(filename,direction)

    photo = ImageTk.PhotoImage(image=image_unpadded)
    #photo = ImageTk.PhotoImage(file='frame_0.jpg')
    current_canvas.create_image(0, 0, anchor="nw", image=photo)
   
    current_canvas.imageList.append(photo)


appear_photo('union/0_frame.jpg','front')


app2 = listbox(root)

app3=back_button(root)
app3=right_button(root)
app3=left_button(root)
#value=str(Lb.get(Lb.curselection()))
#print (value)

root.wm_title("Tkinter window")
root.geometry("2048x1024")
root.mainloop()