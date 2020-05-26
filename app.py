from flask import Flask

app = Flask(__name__)

"""
BUT DE L'APPLICATION

-L'utilisateur doit arriver sur le menu principal, accueilli par une 
"""

@app.route("/")
def index(): 
	return render_template("index.html")

if __name__ == "__main__":
    main()