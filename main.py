# Importing required modules
import cv2
import easygui
import numpy as np
import imageio
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import sys
from PIL import ImageTk, Image


# Building a File Box to choose a Particular File
def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    # read the image
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

    # Confirm that image is chosen
    if originalImage is None:
        print("Cannot find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(originalImage, (960, 540))

    # Converting an image to grayscale
    grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))

    # Applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))

    # Retrieving the edges for cartoon effect
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (960, 540))

    # Applying bilateral filter to remove noise
    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))

    #Masking the edge image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (960, 540))

    # Plotting the whole transition
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes=plt.subplots(3,2,figsize=(8,8),subplot_kw={'xticks':[],'yticks':[]},gridspec_kw=dict(hspace=0.1,wspace=0.1))
    for i,ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()

# Functionality of Save Button
# def save(ReSized6, ImagePath):
#     newName = "cartoonfied_Image"
#     path1 = os.path.dirname(ImagePath)
#     extension = os.path.splitext(ImagePath)
#     path = os.path.join(path1, newName+extension)
#     cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
#     I = "Image saved by name" + newName + " at " + path
#     tk.messagebox.showinfo(title = None, message = I)

# Making the main window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify your image! ')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))

# Cartoonify button in main window
upload = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)

#Save Button in main window
# save1 = Button(top, text="Save your Cartoon Image", command=lambda:save(ImagePath, ReSized6), padx=30, pady=5)
# save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
# save1.pack(side=TOP, pady=50)

top.mainloop()