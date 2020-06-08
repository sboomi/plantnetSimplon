from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.model_selection import cross_val_score

"""
Crée une classe ImageClassifier qui fait office d'"usine" à modèle
La classe prend des données X et des données y, propose une division, en-
-registre plusieurs modèles, fait fitter les données, prédit les
données et propose comme options le calcul du score des différents modèles
"""

class ImageClassifier:
    def __init__(self, X_train, y_train, X_test=None, y_test=None):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.clfs = {}
    def split_set(self, n, r=None):
        """
        Propose de diviser le jeu de données avec en arguments
        -n la taille du jeu de données
        -r l'état aléatoire du mélange
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X_train, self.y_train, test_size=n, random_state=r)
    def add_classifier(self, clf):
        """
        Ajoute un classificateur au dictionnaire de classificateurs
        Prend soit en argument :
        -Un seul classificateur
        -Une liste de classificateurs
        """
        if type(clf) is list:
            for c in clf:
                self.clfs[c.__class__.__name__] = c
                print(f"{c.__class__.__name__} model added")
            return f"Added {len(clf)} models."
        else:
            self.clfs[clf.__class__.__name__] = clf
            return f"{clf.__class__.__name__} model added."
    def fit_data(self):
        """
        Utilise la méthode fit de chaque classificateur pour faire correspondre les données
        d'entraînement
        """
        for name in self.clfs.keys():
            self.clfs[name].fit(self.X_train, self.y_train)
            print(f"Fitting data on {name} model done.")
    def predict_data(self):
        """
        Renvoie `y_pred`, le vecteur résultat d'après le fit effectué sur les données
        """
        try:
            y_pred = {name: self.clfs[name].predict(self.X_test) for name in self.clfs.keys()}
        except:
            print("Error. Use the `fit_data` method to first fit all data on the model before predicting")
        return y_pred
    def predict_proba_data(self):
        """
        Renvoie `y_pred`, le vecteur de prédictions d'après le fit effectué sur les données
        _NOTE :_ le SVC ne pourrait pas marcher dessus.
        """
        try:
            y_prob = {name: self.clfs[name].predict_proba(self.X_test) for name in self.clfs.keys()}
        except:
            print("Error. Use the `fit_data` method to first fit all data on the model before predicting")
        return y_prob
    def accuracy(self, y_pred):
        """
        Renvoie le score de précision pour chaque modèle
        """
        return {name: accuracy_score(self.y_test, y_pred[name]) for name in y_pred.keys()}
    def f1(self, y_pred):
        """
        Renvoie le score F1 pour chaque modèle
        """
        return {name: f1_score(self.y_test, y_pred[name]) for name in y_pred.keys()}
    def cm(self, y_pred):
        """
        Renvoie la matrice de confusion pour chaque modèle
        """
        return {name: confusion_matrix(self.y_test, y_pred[name]) for name in y_pred.keys()}
    def ensembler(self, method='voting'):
        """
        Utilise des méthodes d'ensemble pour tous les classificateurs en fonction de la méthode
        Renvoie l'objet correspondant à la méthode
        """
        if method=='voting':
            vot_clf = VotingClassifier(estimators=[(name, self.clfs[name]) for name in self.clfs.keys()])
            vot_clf.fit(self.X_train, self.y_train)
            return vot_clf
        if method=='stacking':
            stack_clf = StackingClassifier(estimators=[(name, self.clfs[name]) for name in self.clfs.keys()])
            stack_clf.fit(self.X_train, self.y_train)
            return stack_clf
    def test_raw_predictor(self):
        """
        Effectue une validation croisée sur tous les modèles
        """
        for name in self.clfs.keys():
            model = self.clfs[name]
            cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=10, n_jobs = -1)
            print(str(item).split("(")[0], "Scores:", cv_scores)
            print(str(item).split("(")[0], "Mean:", cv_scores.mean())
            print(str(item).split("(")[0], "Standard deviation:", cv_scores.std())  
            print("\n")
