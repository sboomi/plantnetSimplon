import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

"""
BUT DE L'APPLICATION

-L'utilisateur doit arriver sur le menu principal, accueilli par une barre où on peut
transférer un fichier

-Le fichier en question doit être une image (.png, .jpeg, .bmp, etc...)
stocké dans la variable img_flower

-Une fois mise en ligne, on applique le modèle de classification
par la méthode show_flower et on renvoie
soit une probabilité, soit une classification en dur
"""

"""
Variables globales
"""
UPLOAD_FOLDER = 'uploads'
img_flower = []
img_name = []

"""
Configuration de l'application
"""

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
Fonctions de l'application
"""

@app.route("/", methods=['GET', 'POST'])
def show_flower(): 
    global img_flower, img_name
    if request.method == "POST":
        img_flower = request.files.getlist("imgflower") 
        img_name = [secure_filename(img.filename) for img in img_flower ]
        for i in range(len(img_flower)):
            img_flower[i].save(os.path.join(app.config['UPLOAD_FOLDER'], img_name[i]))    
    return render_template("index.html", img_flower=[f'<img src="{UPLOAD_FOLDER}/{name}" alt="{name}">' for name in img_name])
    

# Active le debug
if __name__ == "__main__":
    app.run(debug=True)