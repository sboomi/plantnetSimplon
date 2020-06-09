import pickle
import numpy as np
import os

from PIL import Image, ImageOps
from sklearn.preprocessing import StandardScaler     
from sklearn.decomposition import PCA

import utilities.modules.remove_bg as nobg
import utilities.modules.image_loader as il

"""
Fonction qui appelle les imges contenues dans le dossier /uploads et les fait passer
dans un algorithme de classification.
"""

# ROOT_DIR = '../'
# UPLOADS_FOLDER = f"{ROOT_DIR}uploads"
# TEST_FOLDER = f"{ROOT_DIR}uploads/training"
# SRC_FOLDER = f"{ROOT_DIR}utilities/training_data/raw"

UPLOADS_FOLDER = "uploads"
TEST_FOLDER = "uploads/training"
SRC_FOLDER = "utilities/training_data/raw"

#A changer en fonction du modèle final
MODEL = "utilities/plantnet_model.pkl"

def reduce_features(X, n):
    pca = PCA(n_components=n, svd_solver='randomized', whiten=True)
    scaler = StandardScaler().fit(X)
    Z = scaler.transform(X)
    pca.fit(Z)
    return pca.transform(Z)

def resize_image(folder):
    list_img = os.listdir(folder)
    for img in list_img:
        img_path = os.path.join(folder,img)
        curr_img = Image.open(img_path)
        target_size = (150, 150)
        curr_img = curr_img.resize(target_size)
        curr_img.save(img_path)



def analyze(file_urls, model):

    #Preprocessing

    #Resize pictures
    resize_image(UPLOADS_FOLDER)

    ## Remove background
    nobg.dump_process(UPLOADS_FOLDER, TEST_FOLDER)
    X =il.get_dump(TEST_FOLDER)
    #Get available classnames
    y, y_names = il.get_labels(SRC_FOLDER)

    #Optional: use PCA
    if X.shape[0] >=150 :
        X = reduce_features(X, 150)
    else:
        X = np.sort(X)[:,::-1][:,:150]   

    #Classifier
    #Prediction
    #Returns something with predictions (list of names, dictionnaries...)
    y_pred = model.predict(X)

    #Optional: compute scores

    return [y_names[i] for i in y_pred]
    #return ["Null"] * len(file_urls)