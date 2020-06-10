import pickle
import numpy as np
import os

from PIL import Image, ImageOps
from sklearn.preprocessing import StandardScaler     
from sklearn.decomposition import PCA

import utilities.modules.remove_bg as nobg
import utilities.modules.image_loader as il

FLOWER_NAMES = [
    'Cichorium intybus L.',
    'Leucanthemum vulgare (Vaill.) Lam.',
    'Malva sylvestris L.',
    'Papaver rhoeas L.',
    'Ranunculus bulbosus L.'
]

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



def resized_image(src_image, size=(200,200), bg_color="white"): 
    
    # resize the image so the longest dimension matches our target size
    src_image.thumbnail(size, Image.ANTIALIAS)
    
    # Create a new square background image
    new_image = Image.new("RGB", size, bg_color)
    
    # Paste the resized image into the center of the square background
    new_image.paste(src_image, (int((size[0] - src_image.size[0]) / 2), int((size[1] - src_image.size[1]) / 2)))
    # return the resized image
    return new_image
    
def resize_image(folder):
    """
    Prend l'image chargée et la redimensionne à 150x150
    """
    list_img = os.listdir(folder)
    for img in list_img:
        img_path = os.path.join(folder,img)
        curr_img = Image.open(img_path)
        target_size = (150, 150)
        curr_img = resized_image(curr_img.copy(), target_size, "black")
        curr_img.save(img_path)

def analyze(file_urls, model):

    #Preprocessing

    #Resize pictures
    resize_image(UPLOADS_FOLDER)

    ## Remove background
    nobg.dump_process(UPLOADS_FOLDER, TEST_FOLDER)
    X =il.get_dump(TEST_FOLDER)
    #Get available classnames
    y_names = np.array(FLOWER_NAMES)
    y = np.array(list(range(len(y_names))))

    # #Optional: use PCA
    # if X.shape[0] >=150 :
    #     X = reduce_features(X, 150)
    # else:
    #     X = np.sort(X)[:,::-1][:,:150]   

    #Classifier
    #Prediction
    #Returns something with predictions (list of names, dictionnaries...)
    y_pred = model.predict(X)

    #Optional: compute scores
    return list(y_names[y_pred.astype(int)])
    #return ["Null"] * len(file_urls)