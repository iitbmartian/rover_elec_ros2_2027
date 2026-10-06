# CacheBox PCB — Project Notes

## Overview
ESP32-based board that hosts a WebSocket server for 2-way communication with a ROS2 node running on the RPi5 (no web UI/browser dashboard - see "Firmware Architecture" below): live sensor telemetry (temperature, humidity, atmospheric pressure, current-sensor placeholder) pushed to the ROS node, servo commands sent back from it. Powered from a 12V battery pack stepped down to 5V.

## Bill of Materials / Components
- **U1** — ESP32-DEVKIT-V1
- **U2** — DHT11 (temperature/humidity)
- **U3** — LM2596S-5 (fixed 5V buck regulator)
- **U4** — BMP280 (barometric pressure, I2C breakout)
- **R1** — 10kΩ (DHT11 data line pull-up)
- **C1** — small ceramic/tantalum, input-side filtering near LM2596S-5
- **C2/C3** — 100µF bulk cap near regulator output
- **Servo cap** — 470–1000µF electrolytic across MG995 power connector (buffers inrush current spikes)
- **J1** — Conn_01x03_Pin (MG995 servo header — footprint: PinHeader_1x03_P2.54mm_Vertical)
- **J2** — Screw_Terminal_01x02 (battery input)
- **J3** — Conn_01x03_Pin (DHT11 header)
- **J4** — Conn_01x06_Pin (BMP280 header)
- **Battery** — 3S Li-ion (11.1V nominal, 12.6V full) with BMS, or 12V SLA as a heavier/simpler alternative
- **Servo** — MG995, 180° standard servo (500–900mA typical, up to 2A+ stall)

## Power Chain
Battery (12V) → J2 → LM2596S-5 VIN → OUT (5V) → ESP32 VIN, servo VCC, all downstream rails
ESP32 3V3 → DHT11 VDD, BMP280 VDD

### LM2596S-5 wiring
- FB → OUT (external jumper required — not internally tied on this variant)
- ON/OFF → GND (enables regulator; verify active-low/active-high polarity against actual breakout datasheet)
- VIN → battery+ (through fuse, ~1A resettable)
- GND → battery− / common ground

## Sensor Wiring

### DHT11 (single-wire)
- VDD → 3V3
- GND → GND
- DATA → ESP32 GPIO22, with 10kΩ pull-up (R1) from DATA to 3V3

### BMP280 (I2C mode)
- VDD → 3V3
- GND → GND
- CSB → 3V3 (forces I2C mode instead of SPI)
- SDO → GND (sets I2C address to 0x76; tie to 3V3 instead for 0x77)
- SCK → ESP32 GPIO27 (acting as SCL)
- SDI → ESP32 GPIO21 (acting as SDA)
- I2C remapped off default 21/22 pins since GPIO22 is used by DHT11
- Board has inbuilt I2C pull-ups — no external resistors needed

### Current sensor (placeholder - not yet in the BOM)
- No current-sense IC/footprint has been chosen yet. Firmware reserves
  **GPIO34** (ADC1-only, input-only on this package, safe to read
  alongside WiFi unlike ADC2 pins) for a future analog current-sensor
  output (e.g. ACS712/INA219). Sends raw 12-bit ADC counts today - update
  this section with the real part/pin once one is selected and wired.

### MG995 Servo
- VCC → 5V rail (regulator OUT)
- GND → GND
- Signal → ESP32 GPIO13
- Bulk cap (470–1000µF) across VCC/GND at connector to prevent brownout on stall current
- Connector: male 0.1" pitch 3-pin header (PinHeader_1x03_P2.54mm) to mate with servo's female JR-style lead

## Firmware Architecture
- ESP32 hosts a WebSocket endpoint (`/ws`) for machine-to-machine use — **no web UI**. No HTML/CSS/JS is served; the underlying `AsyncWebServer` only exists to perform the WebSocket upgrade handshake. The sole client is a ROS2 node running on the RPi5, not a browser.
- ESP32 advertises itself via mDNS as `cachebox.local` (`ESPmDNS`, bundled with the core) so the ROS node connects to `ws://cachebox.local/ws` without needing the DHCP IP read off the Serial Monitor each boot (that IP is still logged at 115200 baud as a fallback).
- 2-way messages, same hybrid format as before: ESP32 pushes JSON `{temp, hum, pres, current}` every 2s; ROS node sends plain-text `SERVO:<angle>` commands. (The `LED_ON`/`LED_OFF` placeholder command from the earlier browser-dashboard version was removed — it wasn't part of the ROS integration's requirements.)
- WiFi stays in station (STA) mode, joining the existing network (same as before) — the ESP32 and RPi5 must be on the same WiFi network for both the WebSocket connection and mDNS resolution to work.

### Required Libraries
- **ESPAsyncWebServer** — use the **ESP32Async** fork (not the unmaintained me-no-dev original), required for ESP32 Arduino core 3.x compatibility (original fails with `mbedtls_md5_starts_ret` undeclared errors)
- **AsyncTCP** — matching ESP32Async fork
- **DHT sensor library** (Adafruit) + Adafruit Unified Sensor
- **ArduinoJson**
- **Adafruit BMP280 Library** + Adafruit BusIO
- **ESP32Servo** (Kevin Harrington/madhephaestus) — standard Arduino `Servo.h` does not work on ESP32 core
- **ESPmDNS** — bundled with the ESP32 Arduino core, no separate Library Manager install

### Known Build Issues
- Old ESPAsyncWebServer + new ESP32 core 3.x → mbedtls `_ret` function errors. Fix: switch to ESP32Async fork, or downgrade board package to core 2.0.x (not recommended).

## PCB Layout Notes
- Ground plane / power plane layer swap done via **Edit → Swap Layers** in KiCad PCB Editor (F.Cu ↔ B.Cu), followed by **re-filling zones** (press B) and running DRC — this is a pure layer remap, connectivity unaffected.
- **Edge.Cuts "malformed outline" DRC error** — board outline must be a fully closed loop on the Edge.Cuts layer. Fix: draw a closed rectangle (Rectangle tool, guaranteed closed) or verify/close gaps in existing Line-tool outline; re-run DRC after.
- Capacitor footprint check: axial THT footprints (e.g. `CP_Axial_L10.0mm_D4.5mm`) are only sized for smaller-value electrolytics; a 1000µF/16V cap typically needs ~8–10mm diameter — use a radial footprint (`CP_Radial_D10.0mm_P5.00mm` or similar) instead if using a standard radial electrolytic part.
- 3-pin headers for servo/sensor connections should use **Connector_PinHeader_2.54mm** library (`PinHeader_1x03_P2.54mm_Vertical`), not the bare `Connector_Pin` library.

## Open / To-Verify Items
- Confirm LM2596S-5 module's actual current rating vs. combined draw of ESP32 + DHT11 + BMP280 + MG995 (stall current risk of brownout)
- Confirm ON/OFF pin polarity on actual LM2596 breakout in hand
- Confirm battery connector gender/pinout matches chosen footprint before ordering
- Confirm MG995 pulse width range (500–2400µs set in code) doesn't cause buzzing at travel extremes; narrow if needed

## Full Arduino Sketch (ESP32 firmware)
```cpp
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
```
