import pickle
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

ROOT_DIR = '../'
UPLOADS_FOLDER = f"{ROOT_DIR}uploads"
TEST_FOLDER = f"{ROOT_DIR}uploads/training"
SRC_FOLDER = f"{ROOT_DIR}utilities/training_data/raw"

#A changer en fonction du modèle final
MODEL = "model.pkl"

def reduce_features(X, n):
    pca = PCA(n_components=n)
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
        curr_img.saveas(img_path)



def analyze(file_urls):

    #Preprocessing

    #Resize pictures
    resize_image(UPLOADS_FOLDER)

    ## Remove background
    nobg.dump_process(UPLOADS_FOLDER, TEST_FOLDER)
    X =il.get_dump(TEST_FOLDER)
    #Get available classnames
    _, y, y_names = il.prep_data(SRC_FOLDER)

    #Optional: use PCA
    #X = reduce_features(X, 0.77)

    #Classifier
    # Comes with a trained classifier
    #Using the pickle module
    clf_pkl = open(MODEL,'rb')
    clf = pickle.load(clf_pkl)

    #Prediction
    #Returns something with predictions (list of names, dictionnaries...)
    y_pred = clf.predict(X)

    #Optional: compute scores

    #return [y_names[i] for i in y_pred]
    return ["Null"] * len(file_urls)