import os

from flask import Flask, render_template, request, redirect, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

app = Flask(__name__)
dropzone = Dropzone(app)

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
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

app.config['SECRET_KEY'] = 'plantnet'


"""
Variables globales
"""

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 


"""
Fonctions de l'application
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )
            # append image urls
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request    
    return render_template('index.html')


@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    
    return render_template('results.html', file_urls=file_urls)

# Active le debug
if __name__ == "__main__":
    app.run(debug=True)