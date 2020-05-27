"""
The raw data is provided in the ../training_data/raw folder in 5 
subfolders named after the plant name (image category). This data will be 
processed and the processed versions of the image files will be saved in 
the ../training_data/training folder, retaining the same structure of subfolders 
for each category of image.
"""

src_folder = "../training_data/raw"
train_folder = "../training_data/training"

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Helper function to grayscale an image
def rgb2gray(rgb_image):
    # Separate the RGB channels
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    # Transform every pixel to gray
    gray_image = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray_image

# Create the output folder if it doesn't already exist
if os.path.exists(train_folder):
    shutil.rmtree(train_folder)

# Loop through each subfolder in the input folder
for root, folders, files in os.walk(src_folder):
    for sub_folder in folders:
        print('processing folder ' + sub_folder)
        # Create a matching subfolder in the output dir
        save_folder = os.path.join(train_folder,sub_folder)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        # Loop through the files in the subfolder
        file_names = os.listdir(os.path.join(root,sub_folder))
        for file_name in file_names:
            # Open the file
            file_path = os.path.join(root,sub_folder, file_name)
            print("reading " + file_path)
            image = Image.open(file_path)
            # Create a gray version and save it
            gray_image = rgb2gray(image)
            save_as = os.path.join(save_folder, file_name)
            print("writing " + save_as)
            gray_image.save(save_as)

# Create a new figure
fig = plt.figure(figsize=(12,12))

# loop through the subfolders in the input directory
image_num = 0
for root, folders, filenames in os.walk(src_folder):
    for folder in folders:
        # Get the first image in the subfolder and add it to a plot that has two columns and row for each folder
        file = os.listdir(os.path.join(root,folder))[0]
        src_file = os.path.join(src_folder,folder, file)
        src_image = Image.open(src_file)
        image_num += 1
        a=fig.add_subplot(len(folders), 2, image_num)
        imgplot = plt.imshow(src_image)
        a.set_title(folder)
        # The next image is the grayscaled counterpart - load and plot it
        gray_file = os.path.join(train_folder,folder, file)
        gray_image = Image.open(gray_file)
        image_num += 1
        b=fig.add_subplot(len(folders), 2, image_num)
        imgplot = plt.imshow(gray_image)
        b.set_title('grayscale ' + folder)