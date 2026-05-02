
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# chargement données splité
X_train = pd.read_csv('data/processed/X_train.csv')
X_test = pd.read_csv('data/processed/X_test.csv')

# Initialisation du StandardScaler
scaler = StandardScaler()

# Fit le scaler sur data train et transform les deux training et testing data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Export dvc par le stage
pd.DataFrame(X_train_scaled).to_csv('data/processed/X_train_scaled.csv', index=False)
pd.DataFrame(X_test_scaled).to_csv('data/processed/X_test_scaled.csv', index=False)
# on sauve aussi le standard scaller fité
with open('data/processed/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("Data normalization completed. Scaled training and testing sets saved.")