import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

"""
Loads pictures and stores them in a variable
"""

def prep_data (folder, grayscale=False):
    # iterate through folders, assembling feature, label, and classname data objects

    class_id = 0
    features = []
    labels = np.array([])
    classnames = []
    for root, dirs, filenames in os.walk(folder):
        for d in sorted(dirs):
            print("Reading data from", d)
            # use the folder name as the class name for this label
            classnames.append(d)
            files = os.listdir(os.path.join(root,d))
            for f in files:
                # Load the image file
                imgFile = os.path.join(root,d, f)
                img = Image.open(imgFile)
                if grayscale==True:
                    img = img.convert("L")
                img = np.asarray(img)
                # The image array is a multidimensional numpy array
                # - flatten it to a single array of pixel values for scikit-learn
                # - and add it to the list of features
                features.append(img.ravel())
                
                # Add it to the numpy array of labels
                labels = np.append(labels, class_id )
            class_id  += 1
            
    # Convert the list of features into a numpy array
    features = np.array(features)
    
    return features, labels, classnames

def get_dump(upload_folder):
    list_img = os.listdir(upload_folder)
    f_dump = []

    for f in list_img:
        img_file = os.path.join(upload_folder, f)
        img = Image.open(img_file)
        img = np.asarray(img)
        f_dump.append(img.ravel())

    f_dump = np.array(f_dump)
    return f_dump

def get_labels(upload_folder):
    list_names = os.listdir(upload_folder)
    return np.array(list(range(len(list_names)))), np.array(list_names) 