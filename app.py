from flask import Flask, request, jsonify, render_template_string
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)
model = joblib.load("irrigation_model.pkl")

# Store data in a list (you can switch to file or DB later)
log_data = []

# Home page → Display table
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
    return render_template_string(html, logs=log_data[::-1])  # Show newest first

# API for ESP32
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if "moisture" not in data:
        return jsonify({"error": "Missing 'moisture' field"}), 400

    moisture = data["moisture"]
    df = pd.DataFrame([{"moisture": moisture}])
    prediction = int(model.predict(df)[0])

    # Log this entry
    log_data.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "moisture": moisture,
        "irrigate": prediction
    })

    return jsonify({"irrigate": prediction})

if __name__ == '__main__':
    app.run(debug=True)
