# cachebox_esp32 — code review + stress test

**Source of requirements:** `cachebox_project_notes.md` (hardware BOM,
power chain, pin assignments, firmware architecture, required libraries,
known build issues, and a reference Arduino sketch).

**Subject:** `cachebox_esp32/cachebox_esp32.ino` (ESP32 firmware — WiFi,
WebSocket dashboard, DHT11 + BMP280 telemetry, MG995 servo + GPIO command
handling).

**Method:** full read of the requirements doc; line-by-line diff of the
actual firmware against the md's embedded reference sketch; manual
static/logic review of every function against the documented pin
assignments and stated behavior. No ESP32 compile toolchain (arduino-cli /
PlatformIO) is installed in this environment, so this is a static review,
not a compiler-verified one — flagged explicitly where that matters.

---

## Fixed in this pass

### 1. File wasn't a valid Arduino sketch at all (structural, FIXED)
`cachebox_esp32` was a bare file with **no extension**, sitting directly
in `cachebox_pcb/` rather than inside a same-named folder. Confirmed via
`file` ("C source, Unicode text") and `ls -la`. Arduino IDE requires a
`.ino` file inside a folder of the same basename to recognize and open a
sketch — this file could not have been opened or compiled as-is. Cross-
checked against the user's other Arduino projects under `~/Arduino/*/*.ino`,
which all follow that convention, confirming this is the expected layout.

**Fix:** moved to `cachebox_esp32/cachebox_esp32.ino`.

### 2. Firmware's own comment told the builder to use the library variant that's documented to break the build (FIXED)
The file's header comment said to install "ESPAsyncWebServer (by me-no-dev
/ lacamera fork for newer cores)". But `cachebox_project_notes.md`'s
"Known Build Issues" section explicitly documents that this exact library
variant fails to build against ESP32 Arduino core 3.x with undeclared
`mbedtls_..._ret` errors, and that the fix is the **ESP32Async** fork.
Diffing against the md's own reference sketch confirmed this drifted from
what the md says elsewhere in the same document — the actual code logic
was otherwise identical to the reference, only this comment (and the
matching `AsyncTCP` comment) had regressed to the wrong instruction.

**Fix:** updated both library comments to name the ESP32Async fork and
restated why, referencing the md's Known Build Issues section directly so
the reason doesn't get lost again.

### 3. Header comment understated what the firmware actually sends (FIXED, cosmetic)
Said "Pushes DHT11 sensor data to browser in real time" — the code (both
before and after this pass) also reads and pushes BMP280 pressure every
cycle. Updated to "DHT11/BMP280" to match actual behavior, and to match
the md's own reference sketch, which already said this correctly.

### 4. `setup()` hangs forever with no recovery path if WiFi never connects (FIXED)
`while (WiFi.status() != WL_CONNECTED) { delay(500); ... }` had no bound.
Stress-testing this path (unreachable AP, wrong password, or the
placeholder `YOUR_WIFI_SSID`/`YOUR_WIFI_PASSWORD` strings left unedited —
which is exactly what a fresh checkout of this file ships with) shows the
board blocks in `setup()` indefinitely: no HTTP/WebSocket server ever
starts, no sensors get read or broadcast, and there is no way to recover
short of a manual power cycle every single time. This is the kind of
failure mode "stress test" is meant to surface — every one of the code's
other error paths (DHT read failure, BMP280 not found, malformed WS
messages) degrades gracefully and keeps running; only this one wedges the
whole board.

**Fix:** added a bounded timeout (`WIFI_CONNECT_TIMEOUT_MS`, 20s). On
timeout, logs a message and calls `ESP.restart()` rather than looping
forever. This doesn't fix a wrong password by itself (nothing in firmware
can), but it keeps the board observably retrying over Serial instead of
silently freezing, and it means a *transient* AP outage self-heals once
the AP comes back instead of requiring a manual reset.

---

## Reviewed and found correct (no change needed)

- **Pin assignments** all match the documented wiring exactly: `DHTPIN=22`,
  BMP280 `SDA=21`/`SCL=27` via `Wire.begin(BMP_SDA, BMP_SCL)`, `SERVO_PIN=13`.
  None of these are ESP32 strapping pins that would misbehave at runtime.
- **I2C address handling**: `BMP_I2C_ADDR=0x76` matches the documented
  `SDO → GND` wiring; the code logs a clear diagnostic if `bmp.begin()`
  fails rather than crashing, and `bmpOk` correctly gates all later BMP280
  use (no null-pointer/uninitialized-sensor risk).
- **DHT11 read failure**: `broadcastSensorData()` checks `isnan(h)||isnan(t)`
  and returns early rather than sending garbage — graceful degradation,
  matches the "best-effort telemetry" nature of the stated architecture.
- **`StaticJsonDocument<128>` capacity**: comfortably sized for the 3-field
  `{temp,hum,pres}` payload; not a truncation/overflow risk.
- **Servo command parsing**: `SERVO:<angle>` is `constrain()`-ed to
  [0,180] before being written, so a malformed or out-of-range value from
  the browser can't drive the servo past its documented safe travel range.
  A non-numeric or missing angle (`String::toInt()` semantics) silently
  resolves to `0` rather than crashing — acceptable given there's no
  client-side ack/error channel today.
- **WebSocket fragmentation**: the `WS_EVT_DATA` handler only acts on
  `info->final && info->index==0 && info->len==len` (i.e. a complete,
  unfragmented text frame) and silently ignores anything else. Since every
  real command (`LED_ON`, `LED_OFF`, `SERVO:<n>`) is a handful of bytes,
  this is the correct, simple choice — not a bug.
- **Thread-safety**: ESPAsyncWebServer's WS callback and the Arduino
  `loop()`/timer path both call into `mg995.write()`/`digitalWrite()`, but
  neither touches genuinely shared mutable state with a read-modify-write
  race (only `servoAngle`, which is write-only outside the WS callback) —
  not flagged as needing a mutex for this scope.

## Noted but intentionally left unchanged (out of scope for this pass)

- **JSON field type inconsistency**: `doc["pres"]` is a float when the
  BMP280 is present and the string `"N/A"` when it isn't. Functionally
  harmless (the frontend does plain string concatenation either way), but
  a stricter API would use a JSON `null`. Left as-is since it's cosmetic
  and the md doesn't specify a schema contract.
- **No WebSocket authentication**: any device on the same WiFi network can
  connect to `/ws` and issue `SERVO`/`LED` commands. The md doesn't
  mention an auth requirement and this looks like a hobby/LAN-only
  deployment, so this is a note for the project owner to decide on, not a
  code change made unilaterally.
- **MG995 pulse-width range (500–2400µs) and possible buzzing at travel
  extremes**: this is explicitly called out as an open, hardware-dependent
  "Open/To-Verify" item in the md itself (needs testing against the
  physical servo) — nothing to change in code without that hardware
  feedback.
- **No compiler verification**: this environment has no ESP32 toolchain
  installed (no `arduino-cli`/PlatformIO found), so this review is
  static/manual only. The brace/paren counts and raw-string-literal
  delimiters were sanity-checked programmatically and match exactly
  between the original and modified files outside the intended diff
  region, but an actual `arduino-cli compile` pass (with the ESP32Async
  libraries installed) would be the next step to fully validate this
  before flashing hardware.

---

## Net diff

Structural: file moved from a bare `cachebox_esp32` to
`cachebox_esp32/cachebox_esp32.ino`. Content: 4 changes, all in comments
and the WiFi-connect block — no change to pin numbers, sensor logic,
command parsing, or the served HTML/JS. Full unified diff preserved in
`track.md`.

---

## 2026-09-24 update: converted to a ROS-only bridge (no web UI)

See `track.md`'s 2026-09-24 entry for the full design discussion and the
confirmed decisions. Summary of what changed and what was newly found:

### Changed
- Removed `index_html`, the `server.on("/", ...)` HTTP route, and all
  browser JS — the WebSocket server (`/ws`) is now the only interface,
  intended for a ROS2 node on the RPi5, not a browser.
- Removed the `LED_ON`/`LED_OFF` placeholder command (not part of the
  stated requirement — servo control only).
- Added a placeholder current-sensor ADC input (`CURRENT_SENSE_PIN`,
  GPIO34 — ADC1-only, safe to read alongside WiFi) and a 4th `"current"`
  field in the telemetry JSON, raw ADC counts, no unit conversion. No
  real current-sense IC is in the BOM yet — this reserves the pin and
  wire format the same way `LED_PIN` was previously a documented
  placeholder.
- Added mDNS (`cachebox.local`) so the ROS node has a stable hostname to
  connect to instead of reading a DHCP IP off Serial Monitor each boot.
  WiFi stays in station mode (joins the existing network), unchanged.
- Kept the hybrid protocol (plain-text `SERVO:<angle>` in, JSON telemetry
  out) — no protocol-shape change beyond the new `current` field.
- `cachebox_project_notes.md` updated to match throughout (Overview,
  Sensor Wiring, Firmware Architecture, Required Libraries, and the
  embedded reference sketch — re-verified byte-identical to the real
  `.ino` file via `diff`, same discipline that caught a real bug in the
  first pass of this review).

### New finding (NOT fixed — report-only, out of today's scope)

**Unbounded per-frame heap growth in `onWsEvent()`.** Surfaced by an
oversized-input stress-test scenario (a 50KB single WebSocket text
frame): the handler builds `String msg` by appending one byte at a time
with no cap on `len`:
```cpp
String msg = "";
for (size_t i = 0; i < len; i++) msg += (char)data[i];
```
On a memory-constrained ESP32, a large frame — accidental (a buggy
client) or malicious (anyone on the same WiFi network, since there's no
WS auth — see the earlier "No WebSocket authentication" note above,
which now matters slightly more since the client population changed from
"whoever's on your LAN with a browser" to "should only ever be the RPi5's
ROS node") — forces repeated heap reallocations while building `msg`.
Not fixed here: it predates today's changes, wasn't part of the stated
requirement, and there's no hardware in this environment to verify a safe
cap against. If this becomes a real concern, the fix is a simple length
guard (drop or truncate frames beyond a small max, since real commands
are a handful of bytes) — flagging with the exact repro (see
`protocol_test/stress_test.py` Scenario 10) rather than guessing at the
right cap value.

### How this was verified

No ESP32 toolchain is available in this environment (same limitation as
the first pass), so the C++ firmware itself remains manually reviewed,
not compiler-verified. What *is* newly, genuinely verified: the **wire
protocol** the firmware and a ROS-side client would speak to each other.
`protocol_test/mock_esp32_server.py` re-implements `onWsEvent()`'s and
`broadcastSensorData()`'s exact logic in Python (including replicating
Arduino `String::toInt()`/`strtol()`'s digit-parsing-with-saturating-
overflow behavior, not just `int()` — this distinction caught a real
divergence during testing, see `track.md`), and
`protocol_test/stress_test.py` runs it through 10 scenarios / 17 checks:
telemetry JSON shape, in-range and out-of-range servo commands, a
non-numeric angle, confirming the removed LED command is now a true
no-op, simulated DHT11/BMP280 failures, multi-client broadcast, a rapid
20-cycle reconnect storm, and the oversized-frame case above. **All 17
pass.** `protocol_test/example_ros_client.py` is a minimal reference
client demonstrating the exact connect/send/receive sequence a real
ROS2 node would use, run live end-to-end against the mock server as a
demo (separate process, real TCP/WebSocket connection).
