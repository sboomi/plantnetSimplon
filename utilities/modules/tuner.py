max_iter=1000
from sklearn.model_selection import GridSearchCV
def fine_tune_predictor(predictor, grid):
    predictor_cv = GridSearchCV(predictor, grid, cv=10)
    predictor_cv.fit(X_train, y_train)
    print("Tuned hyperparameters :(best parameters) ", predictor_cv.best_params_)
    print("Accuracy :",predictor_cv.best_score_)
 
parameters_svm = {'C':[1, 10, 100],'kernel':['rbf','linear'], 'gamma':[0.1,'auto', 10], 'degree':[3,4,10]}
parameters_rf = {'n_estimators': [10, 100,50], 'min_samples_leaf': [2,4], 'min_samples_split':[2,6],
'bootstrap':[True, False], 'max_depth': [10, 50, 100]}
parameters_lr = {'penalty': ['l1', 'l2'],'C':[0.001,0.01,1,10,100], 'solver':['liblinear', 'saga']}
fine_tune_predictor(LogisticRegression(max_iter=10000), parameters_lr)
fine_tune_predictor(RandomForestClassifier(n_jobs = -1), parameters_rf)
fine_tune_predictor(SVC(), parameters_svm)