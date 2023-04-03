"""
Image extractor from pdf
   1. extract images to a folder that the pdf resides and name it with pdf name
   2. Limit smallest size of image to 10K(for reducing icons, and other small images)

@Author: Emmanuel

Version 0.0
   + does not support extract of vector graphics
   + Folder to export to is determined by pdf location and name
   + Images are autonamed image{x}.ext with x starting at x
"""
# Import the required Libraries
from tkinter import *
from tkinter import ttk, filedialog,Button
# import tkMessageBox

from tkinter.filedialog import askopenfile
import os
# https://www.tutorialspoint.com/how-to-get-the-absolute-path-of-a-file-using-tkfiledialog-tkinter
# Create an instance of tkinter frame

import fitz
import io
from PIL import Image

import os
path = "pythonprog"
# Check whether the specified path exists or not

def makedir(path):
   """
      Make directory if does not exist given a dir_path
      assumes correct dir name format
   """
   isExist = os.path.exists(path)
   if not isExist:

      # Create a new directory because it does not exist
      os.makedirs(path)


# file path you want to extract images from
file = ""
def extract(file=file):
   """
   Loop for pdf and get every image and write to a folder
   """
   # open the file
   pdf_file = fitz.open(file)

   # iterate over PDF pages
   i = 0
   for page_index in range(len(pdf_file)):

      # get the page itself
      page = pdf_file[page_index]
      # print(page)
      image_list = page.get_images()
      for image_index, img in enumerate(page.get_images(), start=1):

         # get the XREF of the image
         xref = img[0]

         # extract the image bytes
         base_image = pdf_file.extract_image(xref)
         image_bytes = base_image["image"]
         # get the image extension
         image_ext = base_image["ext"]
         smallest = 10000 # Smallest size of image
         if (len(image_bytes)>smallest):
               base = file.replace(".pdf", "\\")
               makedir(base)
               imgout = open(f"{base}image{str(i)}.{image_ext}", "wb")
               print("Image size ", len(image_bytes),f"image{str(i)}.{image_ext}")

               imgout.write(image_bytes)
               imgout.close()
               i+=1

         print(image_ext)

win = Tk()

# Set the geometry of tkinter frame
win.geometry("700x350")

def open_file():
   global file
   file = filedialog.askopenfile(mode='r', filetypes=[('PDF', '*.pdf')])
   if file:
      filepath = os.path.abspath(file.name)
      file = filepath
      Label(win, text="The File is located at : " + str(filepath), font=('Aerial 11')).pack()

# Add a Label widget
label = Label(win, text="Click the Button to browse the Files", font=('Georgia 13'))
label.pack(pady=10)

def extract_image():
   print("file > ", file)
   extract(file)

# Create a Button
ttk.Button(win, text="Browse", command=open_file).pack(pady=20)

B = Button(win, text ="Extract Images to folder", command = extract_image)
B.pack()


win.mainloop()