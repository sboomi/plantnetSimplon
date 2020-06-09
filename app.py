import os
from joblib import load

from flask import Flask, render_template, request, redirect, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

from utilities.image_analyzer import analyze

app = Flask(__name__)
dropzone = Dropzone(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))     
# set file directory path

pipeline = load('utilities/pipeline_model.joblib') 

"""
BUT DE L'APPLICATION

-L'utilisateur doit arriver sur le menu principal, accueilli par une barre où on peut
transférer un fichier

-Le fichier en question doit être une image (.png, .jpeg, .bmp, etc...)
stocké dans la variable img_flower

-Une fois mise en ligne, on applique le modèle de classification
par la méthode show_flower et on renvoie
soit une probabilité, soit une classification en dur

Notes: le dropzone provient de ce tutorial
https://medium.com/@dustindavignon/upload-multiple-images-with-python-flask-and-flask-dropzone-d5b821829b1d
"""


"""
Configuration de l'application
"""
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True #Permet de lâcher plusieurs images
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True 
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*' #Ne tolère que les images
app.config['DROPZONE_REDIRECT_VIEW'] = 'results' #Renvoie les résultats sur la page

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads' #Stocke les images dans '/uploads'

app.config['SECRET_KEY'] = 'plantnet'


"""
Variables globales
"""

photos = UploadSet('photos', IMAGES) #Ensemble des images avec extension spécifiée
configure_uploads(app, photos) #Stocke la configuration des images dans l'application
patch_request_class(app) #Limite la taille des images selon 'MAX_CONTENT_LENGTH'


"""
Fonctions de l'application
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # Installe une session dans l'application si elle n'existe pas
    if "file_urls" not in session:
        session['file_urls'] = []
    # file_urls = stocke les URLS des images de la session
    # Liste vide si ça commence
    file_urls = session['file_urls']
    # Gère les images uploadées sur la dropzone
    if request.method == 'POST':
        file_obj = request.files #Prend tous les fichiers chargés
        for f in file_obj:
            file = request.files.get(f)
            
            # sauvegarde le fichier 
            filename = photos.save(
                file,
                name=file.filename    
            )
            # Stocke dans la liste
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
    # Renvoie à la page avec la dropzone   
    return render_template('index.html')

def interprocessing(model):
    if "analysis_results" not in session:
        session["analysis_results"] = []
    analysis_results = session['analysis_results']
    file_urls = session['file_urls']

    analysis_results = analyze(file_urls, model)

    session['analysis_results'] = analysis_results
    return "Results done!"



@app.route('/results')
def results():
    
    # Redirige sur le menu principal si il n'y aucune image
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))

    print("Processing pictures.")   
    interprocessing(pipeline)
    # Règle la variable file_urls et retire la session en cours
    file_urls = session['file_urls']
    session.pop('file_urls', None)

    analysis_results = session['analysis_results']
    session.pop('analysis_results', None)

    dict_result = {file_urls[i]: analysis_results[i] for i in range(len(file_urls)) }
    
    return render_template('results.html', dict_result=dict_result)

# Active le debug
if __name__ == "__main__":
    app.run(debug=True)