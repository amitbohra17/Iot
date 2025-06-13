import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("irrigation_data_moisture_only.csv")
X = df[['moisture']]
y = df['irrigation_needed']

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "irrigation_model.pkl")  # Use your version of sklearn
