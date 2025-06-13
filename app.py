from flask import Flask, request, jsonify, render_template_string
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)
model = joblib.load("irrigation_model.pkl")

log_data = []

@app.route('/')
def home():
    html = '''
    <h2>🌱 ESP32 Smart Irrigation Dashboard</h2>
    <table border="1">
      <tr><th>Timestamp</th><th>Moisture</th><th>Prediction</th></tr>
      {% for row in logs %}
      <tr>
        <td>{{ row.timestamp }}</td>
        <td>{{ row.moisture }}</td>
        <td>{{ "Irrigate" if row.irrigate == 1 else "No Irrigation" }}</td>
      </tr>
      {% endfor %}
    </table>
    '''
    return render_template_string(html, logs=log_data[::-1])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if "moisture" not in data:
        return jsonify({"error": "Missing 'moisture' field"}), 400

    moisture = data["moisture"]
    df = pd.DataFrame([{"moisture": moisture}])
    prediction = int(model.predict(df)[0])

    # Store the prediction and value
    log_data.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "moisture": moisture,
        "irrigate": prediction
    })

    return jsonify({"irrigate": prediction})
