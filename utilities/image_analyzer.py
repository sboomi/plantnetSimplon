import pickle

import modules.remove_bg as nobg
import modules.image_loader as il
#import ..directories

"""
Fonction qui appelle les imges contenues dans le dossier /uploads et les fait passer
dans un algorithme de classification.
"""

ROOT_DIR = '../'
UPLOADS_FOLDER = f"{ROOT_DIR}/uploads"
TEST_FOLDER = f"{ROOT_DIR}/uploads/training"

#A changer en fonction du modèle final
MODEL = "model.pkl"

def analyze(file_urls):

    #Preprocessing
    ## Remove background
    nobg.img_process(UPLOADS_FOLDER, TEST_FOLDER)
    X, y, y_names, im_dims =il.prep_data(TEST_FOLDER)

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