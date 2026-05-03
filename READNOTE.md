# Projet exament dvc 
```
 nom: GONTIER
 prénom: Lionel
 email: lionel [dot] gontier [at] gmail [dot] com
 dagshub: https://dagshub.com/schmilblick-ai/examen-dvc
```

## 1. Mise en place de l'environement
juste une branche master, un fork classique
git clone git@github.com:schmilblick-ai/examen-dvc.git .

uv init
uv venv
source .venv/bin/activate
création READMENOTE.md
load de raw.csv et config .gitignore dans raw_data

définition des noms de programmes et de dataset
dans l'arborescence

```bash       
├── examen-dvc          
│   ├── data       
│   │   ├── processed     
│   │   └── raw      
│   ├── metrics       
│   ├── models      
│   │   ├── data      
│   │   └── models        
│   ├── src       
│   └── README.md.py       

first git add
```

## 2. Résumé des actions entreprises et notes

## 0. install
uv add dvc
uv add "dvc[s3]"
dvc init
dvc config core.analytics false
#un point important pour éviter de copier, symlink semble ne pas exister
dvc config cache.type symlink
#dvc checkout truc.csv ira du cache à la restoration du lien original

## 1. Connection de dvc à dagshub
Définition d'un repos github et connection via dagshub

read -s DAT
y mettre la DAT 827040d2beaa9454cbee6d5951a99eba9e63817a  Default Access Token

dvc remote add origin s3://dvc
dvc remote modify origin endpointurl https://dagshub.com/schmilblick-ai/examen-dvc.s3
dvc remote modify origin --local access_key_id $DAT
dvc remote modify origin --local secret_access_key $DAT
dvc remote default origin

 dvc dag
 tree -d
 dvc add data/raw
 git rm -r --cached 'data/raw'
 git rm -f -r --cached 'data/processed'
 dvc add data/raw
 dvc add data/processed/
 dvc remove normalize
 dvc add data/processed

### pas necessaire de créer les ressources model intermédiaire cela sera pris en charge par dvc
INUTILE touch models/gbrt_model.pkl
INUTILE dvc add models/gbrt_model.pkl


## 2. Pipeline DVC
À l'aide des commandes DVC vues dans le cours, mettez en place une pipeline qui reproduira le workflow de votre modèle. 
Il faudra bien utiliser les scripts que vous avez mis en place lors de l'étape 1.

#note sur le tracking fin des parametres avec -p pour le split de params
#et l'effet du changement induit dans params avec dvc exp run --set-param split.test_size=0.25

### 1. ajout des fichiers sources non pris en charge par le staging dvc
dvc add data/raw/raw.csv

# Attention à bien source .venv/bin/activate en cas de relance du serveur !!

### 2. dvc stage pour la suite
```
dvc stage add --force  -n split \
  -d data/raw/raw.csv \
  -d src/data/data_split.py \
  -p params.yaml:split \
  -o data/processed/X_train.csv \
  -o data/processed/y_train.csv \
  -o data/processed/X_test.csv \
  -o data/processed/y_test.csv \
  python src/data/data_split.py

dvc repro split

dvc stage add --force -n normalize \
  -d src/data/normalize.py \
  -d data/processed/X_train.csv \
  -d data/processed/X_test.csv \
  -o data/processed/X_train_scaled.csv \
  -o data/processed/X_test_scaled.csv \
  -o data/processed/scaler.pkl \
  python src/data/normalize.py

dvc repro normalize
dvc dag

dvc stage add --force -n gridsearch \
  -d src/models/grid_search.py \
  -p params.yaml:gridsearch \
  -d data/processed/X_train_scaled.csv \
  -d data/processed/y_train.csv \
  -o models/best_params.pkl \
  python src/models/grid_search.py

dvc repro gridsearch

dvc stage add --force -n training \
  -d src/models/training.py \
  -d data/processed/X_train_scaled.csv \
  -d data/processed/y_train.csv \
  -d models/best_params.pkl \
  -o models/trained_model.pkl \
  python src/models/training.py

dvc repro training 

dvc stage add -n evaluate \
  -d src/models/evaluate.py \
  -d data/processed/X_test_scaled.csv \
  -d data/processed/y_test.csv \
  -d models/trained_model.pkl \
  -o models/gbr_preds.csv \
  -M metrics/scores.json \
  python src/models/evaluate.py
dvc repro evaluate 

dvc metrics show
==> dvc metrics show
Path                 mse      r2       rmse                                                                                                         
metrics/scores.json  0.76303  0.23763  0.87352  


git status

git add data/processed.dvc models/trained_model.joblib.dvc

git add metrics/accuracy.json dvc.lock dvc.yaml .gitignore
git commit -m "Pipeline : Trained and evaluated RF, n_estimators = 200, criterion = entropy, accuracy = 0.779"
dvc commit
dvc push
git push origin HEAD:accidents_v2 
```


Finalisation

màj READNOTE.md

ajout  https://dagshub.com/licence.pedago

Une petite partie mlflow fut ajouté pour register le model sur dagshub/mlflow.
  
  Je vais voir cette partie du cours plus en détail maintenant.
  
  j'ai eu besoin de mettre à jour evaluate.py pour enregistrer le model via une expériment.

