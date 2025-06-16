from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)
model = joblib.load("irrigation_model.pkl")

log_data = []

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_result = None

    if request.method == 'POST':
        try:
            moisture = float(request.form['moisture'])
            df = pd.DataFrame([{"moisture": moisture}])
            prediction = int(model.predict(df)[0])

            log_data.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "moisture": moisture,
                "irrigate": prediction
            })

            prediction_result = "💧 Irrigate" if prediction == 1 else "✅ No Irrigation Needed"

        except Exception as e:
            prediction_result = f"Error: {str(e)}"

    html = '''
    <h2>🌱 ESP32 Smart Irrigation Dashboard</h2>

    <form method="POST">
        <label>Enter Moisture Value:</label>
        <input type="number" name="moisture" required>
        <button type="submit">Predict</button>
    </form>

    {% if prediction_result %}
    <h3>Prediction Result: {{ prediction_result }}</h3>
    {% endif %}

    <table border="1" cellpadding="5" cellspacing="0">
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
    return render_template_string(html, logs=log_data[::-1], prediction_result=prediction_result)
