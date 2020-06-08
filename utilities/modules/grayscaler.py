"""
The raw data is provided in the ../training_data/raw folder in 5 
subfolders named after the plant name (image category). This data will be 
processed and the processed versions of the image files will be saved in 
the ../training_data/training folder, retaining the same structure of subfolders 
for each category of image.
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import concurrent.futures

ROOT_DIR = "../.."

SRC_FOLDER = f"{ROOT_DIR}/utilities/training_data/raw"
TRAIN_FOLDER = f"{ROOT_DIR}/utilities/training_data/training"

def grayscale_img_folder(sub_folder):
    print('processing folder ' + sub_folder)
    root = '../training_data/raw'
    # Create a matching subfolder in the output dir
    save_folder = os.path.join(train_folder,sub_folder)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    # Loop through the files in the subfolder
    file_names = os.listdir(os.path.join(root,sub_folder))
    for file_name in file_names:
        # Open the file
        file_path = os.path.join(root,sub_folder, file_name)
        #print("reading " + file_path)
        image = Image.open(file_path)
        # Create a gray version and save it using PIL's 
        # luminosity method
        gray_image = image.convert('L')
        save_as = os.path.join(save_folder, file_name)
        #print("writing " + save_as)
        gray_image.save(save_as)

def main(src_folder="../training_data/raw",train_folder="../training_data/training"):
    # Create the output folder if it doesn't already exist
    if os.path.exists(train_folder):
        shutil.rmtree(train_folder)

    folderlist = []
    # Loop through each subfolder in the input folder
    for root, folders, files in os.walk(src_folder):
        folderlist.extend(folders)

    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(grayscale_img_folder, folderlist)

    

if __name__=='__main__':
    main(SRC_FOLDER, TRAIN_FOLDER)