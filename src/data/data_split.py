import pandas as pd
from sklearn.model_selection import train_test_split
import yaml

data = pd.read_csv( 'data/raw_data/raw.csv')
with open("params.yaml") as f:
    params = yaml.safe_load(f)["split"]

target_column = params["target_column"]

X = data.drop([target_column, 'date'], axis=1)
y = data[target_column]

X_train, X_test, y_train, y_test = train_test_split(X, y
    , test_size=params["test_size"]
    , random_state=params["random_state"])

X_train.to_csv('data/processed/X_train.csv', index=False)
X_test.to_csv('data/processed/X_test.csv', index=False)
y_train.to_csv('data/processed/y_train.csv', index=False)
y_test.to_csv('data/processed/y_test.csv', index=False)

print("Training size:", X_train.shape[0])
print("Testing size:", X_test.shape[0])