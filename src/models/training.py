# Chargement des meilleurs params du gridsearch et entrainement du model GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
import pickle

X_train_scaled = pd.read_csv('data/processed/X_train_scaled.csv')
y_train = pd.read_csv('data/processed/y_train.csv')
with open('models/best_params.pkl', 'rb') as f:
    best_params = pickle.load(f)

# Entraine le model avec les bests params trouvé dans l'exploration GridSearch
model = GradientBoostingRegressor(**best_params, random_state=42)
model.fit(X_train_scaled, y_train.values.ravel())

# Sauvetage du model
tgtmodelpath='models/trained_model.pkl'
with open(tgtmodelpath, 'wb') as f:
    pickle.dump(model, f)

print("Model entrainé avec les params:", best_params)
print(f"model entrainé sauvé dans {tgtmodelpath}")