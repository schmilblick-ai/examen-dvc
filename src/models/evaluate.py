from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import pickle
import json

import mlflow
import mlflow.sklearn
import yaml
import dagshub

#besoin d'enregistre le modèle, donc avec MlFlow

dagshub.init(repo_owner="schmilblick-ai", repo_name="examen-dvc", mlflow=True)
mlflow.set_experiment("Concentration Silice")

with open("params.yaml") as f:
    params = yaml.safe_load(f)

# Charger ce model entrainé et l'évaluer sur le jeux de test
# on enregistre aussi predictions et metriques
    
X_test_scaled = pd.read_csv('data/processed/X_test_scaled.csv')
y_test = pd.read_csv('data/processed/y_test.csv')

with open('models/trained_model.pkl', 'rb') as f:
    gbr_model = pickle.load(f)

# prédisions
y_pred = gbr_model.predict(X_test_scaled)

# -o Sauvegarde test et predictions
preds_df = pd.DataFrame({'y_test': y_test.values.ravel(), 'y_pred': y_pred})
tgtmodelpreds='models/gbr_preds.csv'
preds_df.to_csv(tgtmodelpreds, index=False)

# Calcule des métriques d'évaluation avec le mean_squared_error
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

scores = {'mse': mse, 'rmse': rmse, 'r2': r2}
tgtscorefile='metrics/scores.json'
with open(tgtscorefile, 'w') as f:
    json.dump(scores, f, indent=4)

print("Les métriques d'évaluation sont :", scores)
print(f"Predictions sauveté {tgtmodelpreds}")
print(f"Scores à la sauvette dans {tgtscorefile}")

#Enregistrement du modèle
with mlflow.start_run():
    # params pour traçabilité
    mlflow.log_params(params["gridsearch"])

    # métriques
    for k,v in scores.items():
        mlflow.log_metric(f"{k} score", v)
    
    # enregistrement du modèle
    mlflow.sklearn.log_model(
        sk_model=gbr_model,
        artifact_path="model",
        registered_model_name="concentration_silice"
    )