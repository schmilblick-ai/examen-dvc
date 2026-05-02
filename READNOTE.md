Projet exament dvc 

nom: GONTIER
prénom: Lionel
email: lionel [dot] gontier [at] gmail [dot] com
dagshub: https://dagshub.com/schmilblick-ai/examen_dvc


1. Mise en place de l'environement
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
