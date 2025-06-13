#include <WiFi.h>
#include <HTTPClient.h>

// Wi-Fi credentials
const char* ssid = "Remdi 13 5g";              // Replace with your Wi-Fi name
const char* password = "not@v@il@ble";         // Replace with your Wi-Fi password

// API endpoint (make sure to use /predict)
const char* serverName = "https://iot-proj-zgwa.onrender.com/predict";

// Hardware pins
const int moisturePin = 34;  // Analog pin connected to moisture sensor
const int relayPin = 13;     // Digital pin connected to relay

void setup() {
  Serial.begin(115200);
  delay(1000);  // Wait for Serial Monitor to start

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);  // Keep pump OFF initially (HIGH = OFF for active LOW relay)

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Connected to Wi-Fi");
}

void loop() {
  int moisture = analogRead(moisturePin);
  Serial.print("📟 Soil Moisture: ");
  Serial.println(moisture);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);  // Use your deployed endpoint
    http.addHeader("Content-Type", "application/json");

    // Format the JSON payload
    String jsonPayload = "{\"moisture\":" + String(moisture) + "}";

    Serial.println("📤 Sending data to AI model...");
    int httpResponseCode = http.POST(jsonPayload);
    String response = http.getString();

    Serial.print("🌐 Server Response: ");
    Serial.println(response);

    // Interpret AI response
    if (response.indexOf("\"irrigate\":1") != -1) {
      Serial.println("✅ AI says: IRRIGATE → Turning ON pump");
      digitalWrite(relayPin, LOW);  // Relay ON (Pump ON)
    } else {
      Serial.println("❌ AI says: DO NOT IRRIGATE → Turning OFF pump");
      digitalWrite(relayPin, HIGH); // Relay OFF (Pump OFF)
    }

    http.end(); // End HTTP connection
  } else {
    Serial.println("❌ Wi-Fi disconnected! Retrying...");
    WiFi.begin(ssid, password);
  }

  delay(10000);  // Wait 10 seconds before next reading
}
