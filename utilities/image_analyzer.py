import modules.grayscaler as gs
import modules.image_loader as il
#import ..directories

"""
Fonction qui appelle les imges contenues dans le dossier /uploads et les fait passer
dans un algorithme de classification.
"""

ROOT_DIR = '../'
UPLOADS_FOLDER = f"{ROOT_DIR}/uploads"
TEST_FOLDER = f"{ROOT_DIR}/uploads/training"

def analyze(file_urls):

    #Preprocessing
    ## Grayscaler
    gs.main(UPLOADS_FOLDER, TEST_FOLDER)
    X, y, y_names, im_dims =il.prep_data(TEST_FOLDER)

    #Classifier
    # Comes with a trained classifier
    #Using the pickle module

    #Prediction
    #Returns something with predictions (list of names, dictionnaries...)

    return ["Null"] * len(file_urls)