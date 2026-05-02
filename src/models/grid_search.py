# load scaled data and choose a model, then apply GridSearchCV to find the best hyperparameters
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
import pandas as pd
import pickle
import yaml


X_train_scaled = pd.read_csv('data/processed/X_train_scaled.csv')
y_train = pd.read_csv('data/processed/y_train.csv')

model = GradientBoostingRegressor(random_state=42)

# Chargement hyperParm de la section gridsearch définit dans le Yaml
with open("params.yaml") as f:
    params = yaml.safe_load(f)["gridsearch"]

# Initialisation du GridSearchCV
grid_search = GridSearchCV(estimator=model
    , param_grid=params["param_grid"]
    , cv=params["cv"]
    , n_jobs=params["n_jobs"], verbose=2)

# Fit GridSearchCV avec les data training mise à l'échèle, 
# avec applatissement continue des valeurs target y_train - le ravel
grid_search.fit(X_train_scaled, y_train.values.ravel())

# on sauve précieusement les meilleurs parametres en fichier pkl 
with open('models/best_params.pkl', 'wb') as f:
    pickle.dump(grid_search.best_params_, f)

# Affichage perdu
print("le meilleur Hyperparms:", grid_search.best_params_)