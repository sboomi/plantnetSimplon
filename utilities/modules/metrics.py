from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

def test_raw_predictor(predictor):
    for item in predictor:
        model = item
        cv_scores = cross_val_score(model, X_train, y_train, cv=10, n_jobs = -1)
        print(str(item).split("(")[0], "Scores:", cv_scores)
        print(str(item).split("(")[0], "Mean:", cv_scores.mean())
        print(str(item).split("(")[0], "Standard deviation:", cv_scores.std())  
        print("\n")
predictor = [LogisticRegression(), RandomForestClassifier(), SVC()]
test_raw_predictor(predictor)