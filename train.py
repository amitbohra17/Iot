import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("irrigation_data_moisture_only.csv")

# Features and target
X = df[['moisture']]
y = df['irrigation_needed']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model to file
joblib.dump(model, "irrigation_model.pkl")

print("✅ Model trained and saved as 'irrigation_model.pkl'")