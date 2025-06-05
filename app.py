from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load trained model
model = joblib.load("irrigation_model.pkl")

app = Flask(__name__)

@app.route('/')
def home():
    return "🌱 ESP32 Smart Irrigation API is running."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Check if moisture value is present
    if "moisture" not in data:
        return jsonify({"error": "Missing 'moisture' field"}), 400

    df = pd.DataFrame([data])  # e.g., {"moisture": 1850}
    prediction = model.predict(df)[0]

    return jsonify({"irrigate": int(prediction)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)