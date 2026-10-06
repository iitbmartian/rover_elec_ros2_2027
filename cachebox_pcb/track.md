# Track: cachebox_esp32 review + stress test

Running log of every step taken during this review/modification pass.

## 2026-09-23

- Task: read `cachebox_project_notes.md` (the documented hardware/firmware requirements), then grill, stress-test, and modify `cachebox_esp32` (the actual firmware) as needed to comply with those requirements. Unlike the earlier rover_mobility review, this task explicitly authorizes modifying the file.
- Read `cachebox_project_notes.md` in full: ESP32 + DHT11 + BMP280 + MG995 servo, self-hosted WebSocket dashboard, documented pin assignments (DHT11 DATA=GPIO22, BMP280 SDA=GPIO21/SCL=GPIO27, servo signal=GPIO13), documented library requirements (ESPAsyncWebServer **ESP32Async fork**, not me-no-dev original - explicitly called out as a known build-breaking issue on ESP32 core 3.x), and a full reference Arduino sketch embedded in the md.
- Read the actual `cachebox_esp32` file. Found it is a **bare file with no extension**, sitting directly in `cachebox_pcb/` (not inside a same-named folder) - confirmed via `file` (reports "C source, Unicode text") and `ls -la`. Checked the user's other Arduino projects under `~/Arduino/*/*.ino` - all follow the classic Arduino IDE convention (folder name == sketch basename, `.ino` extension). `~/.arduino15` (Arduino IDE 2.x config dir) exists; no `arduino-cli`/`platformio` on PATH. **This means the file as committed cannot be opened or compiled as an Arduino sketch at all** - first concrete finding.
- Diffed the actual firmware's code against the md's embedded reference sketch (`diff -u`): the only differences were in the top-of-file comment block - the actual code logic is otherwise byte-identical to the reference. The comment differences matter: the actual file's comment says to use "ESPAsyncWebServer (by me-no-dev / lacamera fork for newer cores)" - this is exactly the library variant the md's own "Known Build Issues" section says causes `mbedtls_md5_starts_ret` undeclared errors on ESP32 core 3.x. The file's own documentation was telling whoever builds it to hit a known, already-diagnosed build failure.
- Static code review beyond the diff (pins, power chain, sensor wiring, message handling, error paths) - see `cachebox_esp32_review.md` for the full findings list.
- Decision: fixed (a) the sketch-folder/extension structural issue, (b) the wrong library-fork comment (directly contradicts documented requirement), (c) a stale comment claiming only DHT11 data is pushed (code also pushes BMP280 pressure), and (d) added a bounded WiFi connection retry/reboot instead of an indefinite hang, since stress-testing the "bad/unset WiFi credentials" path showed `setup()` blocks forever with no recovery - a real robustness gap surfaced by the stress-test framing of this task. Left several lower-severity/cosmetic findings as report-only recommendations rather than code changes (see review doc) to keep the diff minimal and clearly justified.
- No compile toolchain available in this environment (no arduino-cli/platformio installed) - review is static/manual, not compiler-verified. Noted as a limitation.
- Restructured: `mv cachebox_esp32 cachebox_esp32.orig.bak && mkdir cachebox_esp32`, wrote the fixed content to `cachebox_esp32/cachebox_esp32.ino`, verified brace/paren counts match (33/33, 114/114) and the raw HTML string literal delimiters are intact, diffed old vs new to confirm only the intended lines changed, then removed the `.orig.bak` once the diff was captured here.
- Wrote `cachebox_esp32_review.md` with the full findings list (4 fixed, several reviewed-and-correct, several intentionally left as report-only notes to keep the diff minimal and justified).

## Final diff (old flat file -> new cachebox_esp32/cachebox_esp32.ino)

```diff
4c4
<  * - Pushes DHT11 sensor data to browser in real time
---
>  * - Pushes DHT11/BMP280 sensor data to browser in real time
8,9c8,13
<  *   - ESPAsyncWebServer (by me-no-dev / lacamera fork for newer cores)
<  *   - AsyncTCP (dependency of ESPAsyncWebServer)
---
>  *   - ESPAsyncWebServer - use the ESP32Async fork, NOT the unmaintained
>  *     me-no-dev/lacamera original. The original fails to build against
>  *     ESP32 Arduino core 3.x with undeclared `mbedtls_..._ret` errors -
>  *     see cachebox_project_notes.md's "Known Build Issues" section.
>  *   - AsyncTCP - matching ESP32Async fork (mixing forks between
>  *     ESPAsyncWebServer and AsyncTCP can cause version/ABI mismatches)
30c34
< #define DHTPIN   22      // D22, matches your schematic
---
> #define DHTPIN   22      // D22, matches schematic
40a45,49
> // WiFi connect: give up and reboot after this many failed 500ms polls,
> // rather than blocking setup() forever if credentials are wrong/unset or
> // the AP is unreachable (this board has no other way to recover otherwise).
> #define WIFI_CONNECT_TIMEOUT_MS 20000
>
205a215
>   unsigned long wifiStart = millis();
208a219,228
>     if (millis() - wifiStart > WIFI_CONNECT_TIMEOUT_MS) {
>       // Wrong/unset credentials or AP unreachable - don't hang setup()
>       // forever with no recovery path. Reboot and try again; if ssid/
>       // password are still placeholders this repeats indefinitely but at
>       // least stays observable/recoverable over Serial rather than
>       // silently freezing.
>       Serial.println();
>       Serial.println("WiFi connect timed out - restarting to retry");
>       ESP.restart();
>     }
```

(Note: the `DHTPIN` comment line diff, "matches your schematic" -> "matches schematic", was an incidental artifact of the source .ino's wording never having drifted from the md's reference sketch on that one line - not a deliberate fix, just confirming the file matches the md reference exactly there.)

## Review complete

Deliverables: `track.md` (this file), `cachebox_esp32_review.md` (findings
report), `cachebox_esp32/cachebox_esp32.ino` (fixed, restructured
firmware). 4 issues fixed (sketch structure, wrong library-fork
instruction, stale comment, unbounded WiFi-hang); several more reviewed
and confirmed correct; a few intentionally left as report-only
recommendations to keep the change minimal and justified.

## 2026-09-24 — convert to a ROS-only WebSocket bridge (no web UI)

- Task: rewrite `cachebox_esp32.ino` so it has no browser-facing web UI at
  all - it should just host a WebSocket server that a ROS2 node on the
  RPi5 connects to over WiFi, forwarding DHT11/BMP280/current-sensor
  telemetry one way and servo commands the other way. User explicitly
  asked me to describe the plan and confirm before editing, since several
  parts of the request needed a concrete design decision.
- Flagged one factual gap before proposing anything: `cachebox_project_notes.md`'s
  BOM has no current sensor at all (only DHT11 + BMP280 + MG995 servo) -
  the user's requirement mentioned "current sensor" data alongside
  DHT11/BMP280. Surfaced this rather than assuming, plus three other real
  design forks (network discovery mode, message protocol shape, and
  whether to keep the pre-existing LED_ON/LED_OFF placeholder command)
  via `AskUserQuestion` before writing any code.
- Decisions confirmed by the user:
  1. Add a **placeholder current-sensor ADC input** (no real sensor
     chosen yet, mirrors how `LED_PIN` was already a documented
     placeholder) - reserved **GPIO34** (ADC1-only, input-only, safe
     alongside WiFi unlike ADC2 pins).
  2. **Keep WiFi station mode** (join the existing network, unchanged)
     and **add mDNS** (`cachebox.local` via `ESPmDNS`, bundled with the
     ESP32 core) so the ROS node doesn't need a DHCP IP read off the
     Serial Monitor every boot.
  3. **Keep today's hybrid protocol** (plain-text `SERVO:<angle>` in,
     JSON telemetry out) rather than switching to JSON both ways -
     smaller diff, protocol behavior otherwise unchanged from the
     browser-dashboard version.
  4. **Remove** the `LED_ON`/`LED_OFF` placeholder command entirely - not
     part of the stated requirement (servo control only).
- Rewrote `cachebox_esp32/cachebox_esp32.ino`: removed the `index_html`
  PROGMEM string, the `server.on("/", HTTP_GET, ...)` handler, and all
  browser-facing JS; removed `LED_PIN` and its setup/command branch;
  added `CURRENT_SENSE_PIN` (GPIO34, raw `analogRead()`, no unit
  conversion - same "raw values, scale in the consumer" convention as the
  rest of this firmware and the STM32 boards reviewed earlier this
  session); added `#include <ESPmDNS.h>` and `MDNS.begin("cachebox")` +
  `MDNS.addService("ws", "tcp", 80)` after a successful WiFi connect;
  bumped the `StaticJsonDocument` capacity from 128 to 192 bytes for the
  new 4th telemetry field; updated the header comment block to describe
  the new architecture. Verified brace/paren balance (20/20, 92/92) and
  zero leftover `LED`/`index_html`/`<script>` references after the edit.
- Updated `cachebox_project_notes.md` to match: Overview, a new "Current
  sensor (placeholder - not yet in the BOM)" subsection under Sensor
  Wiring, the "Firmware Architecture" section (no web UI, mDNS hostname,
  updated protocol description, LED removal noted), the Required
  Libraries list (added ESPmDNS), and spliced the embedded "Full Arduino
  Sketch" reference block to be byte-identical to the real `.ino` file
  again (verified via `diff`) - same discipline as the first review,
  which flagged a real bug when this reference sketch and the real file
  had drifted apart.
- **Stress-tested the protocol** (not the C++ compile - still no
  arduino-cli/hardware in this environment, same limitation as before):
  wrote `protocol_test/mock_esp32_server.py`, a Python
  asyncio WebSocket server that faithfully re-implements the firmware's
  exact message handling, INCLUDING replicating Arduino `String::toInt()`/
  `strtol()` semantics (leading-digit parsing, 32-bit `long` saturation on
  overflow) rather than just using Python's `int()` - this distinction
  actually mattered: a naive `int()` on a 50,000-digit stress-test input
  hit Python 3.10's own arbitrary-precision-conversion guard and crashed
  the mock's connection handler, which would NOT be what the real C
  firmware does (`strtol` saturates, it doesn't raise) - caught and fixed
  by hand-rolling digit-by-digit parsing with overflow saturation,
  verified against the real 32-bit `LONG_MAX`/`LONG_MIN` bounds.
  `protocol_test/stress_test.py` runs 17 checks across 10 scenarios (JSON
  schema shape, in-range and clamped servo commands, non-numeric angle
  parsing, the removed LED command being a true no-op, simulated DHT11/
  BMP280 failure fallbacks, multi-client broadcast, a 20-cycle rapid
  reconnect storm, and the 50KB-oversized-frame case above) - **all 17
  pass**. `protocol_test/example_ros_client.py` is a minimal reference
  client (plain asyncio, not a full rclpy node - no ROS2 install
  available here to test one against) showing the exact connect/send/
  receive logic a real ROS2 node's callbacks would wrap; ran it live
  against the mock server as an end-to-end demo (separate subprocess,
  real WebSocket connection over a real TCP socket) - servo command sent
  and recorded server-side, three telemetry frames received and parsed
  correctly client-side.
- New finding surfaced by the oversized-frame stress scenario, written up
  in `cachebox_esp32_review.md` rather than silently fixed: the real
  firmware's `onWsEvent()` builds `String msg` by appending one byte at a
  time with no length cap on an incoming `WS_TEXT` frame - a large frame
  (accidental or malicious) would force repeated heap reallocations on a
  memory-constrained ESP32. Flagged as a report-only note, not fixed,
  since it wasn't part of today's ask and there's no hardware here to
  verify a safe cap against.
- Confirmed the architecture itself needed no fallback/alternative: ESP32
  as a WebSocket server with a RPi5 ROS-side client is directly what the
  existing design already did (for a browser instead of a script), and
  the end-to-end demo proves the mechanism works as stated. The mDNS
  addition is the one genuine practical gap that would otherwise bite a
  real deployment (DHCP IP discovery) - addressed rather than left open.

### Task complete

Deliverables added this pass: updated `cachebox_esp32/cachebox_esp32.ino`
and `cachebox_project_notes.md` (kept in sync, verified byte-identical
where they should match), plus `protocol_test/{mock_esp32_server,
stress_test,example_ros_client}.py`. 17/17 protocol stress-test checks
pass. C++ firmware itself remains compiler-unverified (no toolchain
available) - same disclosed limitation as the first review.
