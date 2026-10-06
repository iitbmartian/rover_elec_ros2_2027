/*
 * ESP32 Self-Hosted WebSocket Server - ROS bridge (no web UI)
 * - Hosts a WebSocket endpoint (/ws) that a ROS2 node on the RPi5 connects
 *   to over WiFi - NOT a browser dashboard. No HTML/JS is served; the only
 *   thing this board's HTTP server does is the WebSocket upgrade handshake.
 * - Pushes DHT11/BMP280/current-sensor data to the ROS node in real time
 * - True 2-way communication over a single WebSocket connection: ROS node
 *   sends servo commands, ESP32 pushes sensor telemetry
 * - Advertises itself as cachebox.local via mDNS so the ROS node doesn't
 *   need to read a DHCP IP off the Serial Monitor every boot
 *
 * Libraries needed (install via Library Manager):
 *   - ESPAsyncWebServer - use the ESP32Async fork, NOT the unmaintained
 *     me-no-dev/lacamera original. The original fails to build against
 *     ESP32 Arduino core 3.x with undeclared `mbedtls_..._ret` errors -
 *     see cachebox_project_notes.md's "Known Build Issues" section.
 *   - AsyncTCP - matching ESP32Async fork (mixing forks between
 *     ESPAsyncWebServer and AsyncTCP can cause version/ABI mismatches)
 *   - DHT sensor library (by Adafruit) + Adafruit Unified Sensor
 *   - ArduinoJson
 *   - Adafruit BMP280 Library + Adafruit Unified Sensor + Adafruit BusIO
 *   - ESP32Servo (by Kevin Harrington / madhephaestus) - standard Arduino
 *     Servo library does NOT work on ESP32 core, use this instead
 *   - ESPmDNS - bundled with the ESP32 Arduino core, no separate install
 */

#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <ESP32Servo.h>
#include <ESPmDNS.h>

// ---------- CONFIG ----------
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// mDNS hostname - the ROS node connects to ws://cachebox.local/ws instead
// of a DHCP-assigned IP that can change between boots.
#define MDNS_HOSTNAME "cachebox"

#define DHTPIN   22      // D22, matches schematic
#define DHTTYPE  DHT11

// BMP280 I2C pins - remapped off default 21/22 since GPIO22 is used by DHT11
#define BMP_SDA  21
#define BMP_SCL  27
#define BMP_I2C_ADDR 0x76   // 0x76 if SDO tied to GND, 0x77 if tied to 3V3

#define SERVO_PIN 13        // MG995 signal wire

// Placeholder current-sensor input - NOT in cachebox_project_notes.md's BOM
// yet (no current-sense IC/footprint chosen at time of writing). GPIO34 is
// ADC1-only (safe to read alongside WiFi, unlike ADC2 pins) and input-only
// on this package, a reasonable default for an analog current-sensor
// output (e.g. ACS712/INA219 analog pin) once one is actually wired up.
// Sends raw 12-bit ADC counts, no unit conversion - same "raw values, do
// scaling in the consumer" convention as the rest of this firmware.
#define CURRENT_SENSE_PIN 34

// WiFi connect: give up and reboot after this many failed 500ms polls,
// rather than blocking setup() forever if credentials are wrong/unset or
// the AP is unreachable (this board has no other way to recover otherwise).
#define WIFI_CONNECT_TIMEOUT_MS 20000

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp;
bool bmpOk = false;

Servo mg995;
int servoAngle = 90; // start centered

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

unsigned long lastSensorRead = 0;
const unsigned long sensorInterval = 2000; // ms

// ---------- WEBSOCKET EVENT HANDLER ----------
// Protocol (ROS node <-> ESP32), plain text in / JSON out - see
// cachebox_project_notes.md's "Firmware Architecture" section:
//   ROS -> ESP32:  "SERVO:<0-180>"  (plain text, no trailing newline needed)
//   ESP32 -> ROS:  {"temp":.., "hum":.., "pres":.., "current":..} every 2s
void onWsEvent(AsyncWebSocket *server, AsyncWebSocketClient *client,
               AwsEventType type, void *arg, uint8_t *data, size_t len) {
  if (type == WS_EVT_CONNECT) {
    Serial.printf("Client #%u connected\n", client->id());
  } else if (type == WS_EVT_DISCONNECT) {
    Serial.printf("Client #%u disconnected\n", client->id());
  } else if (type == WS_EVT_DATA) {
    AwsFrameInfo *info = (AwsFrameInfo*)arg;
    if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
      String msg = "";
      for (size_t i = 0; i < len; i++) msg += (char)data[i];

      Serial.println("Received: " + msg);

      // ---- Command handling ----
      if (msg.startsWith("SERVO:")) {
        int angle = msg.substring(6).toInt();
        angle = constrain(angle, 0, 180);
        servoAngle = angle;
        mg995.write(servoAngle);
      }
      // Add more command branches here as needed
    }
  }
}

// ---------- SEND SENSOR DATA TO ALL CLIENTS ----------
void broadcastSensorData() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT11");
    return;
  }

  StaticJsonDocument<192> doc;
  doc["temp"] = t;
  doc["hum"]  = h;

  if (bmpOk) {
    doc["pres"] = bmp.readPressure() / 100.0F; // Pa -> hPa
  } else {
    doc["pres"] = "N/A";
  }

  doc["current"] = analogRead(CURRENT_SENSE_PIN); // raw ADC counts, see define comment above

  String json;
  serializeJson(doc, json);
  ws.textAll(json);
}

// ---------- SETUP ----------
void setup() {
  Serial.begin(115200);

  dht.begin();

  // ESP32Servo needs allocated timers before attach() on some cores
  ESP32PWM::allocateTimer(0);
  mg995.setPeriodHertz(50);           // standard 50Hz servo signal
  mg995.attach(SERVO_PIN, 500, 2400); // pulse width range - adjust if MG995 buzzes at extremes
  mg995.write(servoAngle);

  Wire.begin(BMP_SDA, BMP_SCL);
  bmpOk = bmp.begin(BMP_I2C_ADDR);
  if (!bmpOk) {
    Serial.println("BMP280 not found - check wiring/address (tried 0x76)");
  } else {
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                     Adafruit_BMP280::SAMPLING_X2,
                     Adafruit_BMP280::SAMPLING_X16,
                     Adafruit_BMP280::FILTER_X16,
                     Adafruit_BMP280::STANDBY_MS_500);
  }

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  unsigned long wifiStart = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (millis() - wifiStart > WIFI_CONNECT_TIMEOUT_MS) {
      // Wrong/unset credentials or AP unreachable - don't hang setup()
      // forever with no recovery path. Reboot and try again; if ssid/
      // password are still placeholders this repeats indefinitely but at
      // least stays observable/recoverable over Serial rather than
      // silently freezing.
      Serial.println();
      Serial.println("WiFi connect timed out - restarting to retry");
      ESP.restart();
    }
  }
  Serial.println();
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (!MDNS.begin(MDNS_HOSTNAME)) {
    Serial.println("mDNS setup failed - ROS node will need the raw IP above");
  } else {
    MDNS.addService("ws", "tcp", 80);
    Serial.println("mDNS responder started: " MDNS_HOSTNAME ".local");
  }

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);

  server.begin();
  Serial.println("WebSocket server started - no web UI, waiting for ROS node on /ws");
}

// ---------- LOOP ----------
void loop() {
  ws.cleanupClients();

  unsigned long now = millis();
  if (now - lastSensorRead > sensorInterval) {
    lastSensorRead = now;
    broadcastSensorData();
  }
}
