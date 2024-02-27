# import
import cv2
import imutils
import easygui 
import imageio 
import sys
import matplotlib.pyplot as plt
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


# Upload
def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)


# Cartoonify
def cartoonify(ImagePath):
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

# check if the image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    ReSized1 = cv2.resize(originalmage, (960, 540))
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))

#applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
#retrieving the edges for cartoon effect
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
      cv2.ADAPTIVE_THRESH_MEAN_C, 
      cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (960, 540))
#applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    #masking 
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (960, 540))

#Plotting
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()

# GUI
top=tk.Tk()
top.geometry('500x500')
top.title('Cartoonify Your Image !')
top.configure(background='#eadbc8')
label=Label(top,background='#eadbc8', font=('ariel',20,'bold'))

# Buttons
upload=Button(top,text="Cartoonify an Image",command=upload,padx=50,pady=10)
upload.configure(background='blue', foreground='white',font=('ariel',10,'bold'))
upload.pack(side=TOP,pady=200)

def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

save1=Button(top,text="Save cartoon image",command=lambda: save(ImagePath, ReSized6),padx=30,pady=5)
save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
save1.pack(side=TOP,pady=50)

top.mainloop()

