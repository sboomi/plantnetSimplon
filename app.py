from flask import Flask, render_template, request

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
img_flower = []

"""
Fonctions de l'application
"""

@app.route("/", methods=['GET', 'POST'])
def show_flower(): 
    if request.method == "POST":
        img_flower = request.form.get("imgflower") 
	return render_template("index.html", img_flower=img_flower)

if __name__ == "__main__":
    main()