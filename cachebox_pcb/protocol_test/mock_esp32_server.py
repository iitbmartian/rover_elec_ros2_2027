"""
mock_esp32_server.py

A Python re-implementation of cachebox_esp32.ino's WebSocket protocol,
faithful enough to stress-test the PROTOCOL (message shapes, command
parsing edge cases, multi-client broadcast, failure fallbacks) without
needing real ESP32 hardware or a compiler - neither is available in this
environment. This does NOT test the C++/Arduino code itself; it tests
whether a ROS-side client built against this protocol description will
actually work against the real firmware's documented behavior.

Protocol mirrored from cachebox_esp32.ino:
  ROS -> ESP32:  plain text "SERVO:<angle>"
    - only messages starting with the literal prefix "SERVO:" are handled
      (mirrors `msg.startsWith("SERVO:")`)
    - the angle is parsed with Arduino String::toInt() semantics: parses
      a leading optional '-' plus digits, stops at the first non-digit,
      and returns 0 if there are no leading digits at all (mirrored by
      _arduino_to_int() below - Python's int() is NOT a drop-in
      replacement, it raises on trailing garbage instead of truncating)
    - clamped to [0, 180] (mirrors `constrain(angle, 0, 180)`)
  ESP32 -> ROS:  JSON, broadcast to ALL connected clients every ~2s
    {"temp": <float>, "hum": <float>, "pres": <float or "N/A">, "current": <int>}
    - skipped entirely for a cycle if the (simulated) DHT11 read fails
      (mirrors the real firmware's `if (isnan(h) || isnan(t)) return;`)
"""
import asyncio
import json

import websockets


LONG_MAX = 2147483647    # ESP32 `long` is 32-bit
LONG_MIN = -2147483648


def arduino_to_int(s: str) -> int:
    """Mirrors Arduino's String::toInt(), which is backed by strtol():
    parse an optional leading '-' followed by digits, stop at the first
    non-digit, return 0 if there are no leading digits at all, and
    SATURATE (not raise, not wrap) at a 32-bit long's range on overflow -
    strtol()'s real, well-defined behavior for a pathologically long
    digit string. Digit-by-digit with early saturation, rather than
    building the full substring and converting it in one shot: Python's
    own int() has an arbitrary-precision-conversion guard (raises
    ValueError past ~4300 digits) that a real C parser doesn't have, so a
    naive int(s) here would diverge from firmware behavior in the exact
    oversized-input case this mock exists to stress-test."""
    i = 0
    n = len(s)
    sign = 1
    if i < n and s[i] in '+-':
        if s[i] == '-':
            sign = -1
        i += 1
    start = i
    value = 0
    saturated = False
    while i < n and s[i].isdigit():
        if not saturated:
            value = value * 10 + int(s[i])
            if value > LONG_MAX:
                saturated = True
                value = LONG_MAX
        i += 1
    if i == start:
        return 0
    result = sign * value
    return max(LONG_MIN, min(LONG_MAX, result))


class MockCacheboxServer:
    """Mirrors cachebox_esp32.ino's onWsEvent()/broadcastSensorData()
    loop. Test code can inject sensor failures/values via the
    dht_fails/bmp_ok/sensor_values attributes between broadcasts."""

    def __init__(self):
        self.servo_angle = 90  # matches the firmware's `int servoAngle = 90;`
        self.clients = set()
        self.commands_received = []
        self.dht_fails = False
        self.bmp_ok = True
        self.sensor_values = {'temp': 24.5, 'hum': 55.0, 'pres': 1013.2, 'current': 512}
        self._server = None
        self._broadcast_task = None

    async def _handler(self, websocket):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                self.commands_received.append(message)
                if message.startswith('SERVO:'):
                    angle = arduino_to_int(message[len('SERVO:'):])
                    angle = max(0, min(180, angle))
                    self.servo_angle = angle
                # anything not starting with "SERVO:" is silently ignored,
                # mirroring the real firmware's onWsEvent()
        finally:
            self.clients.discard(websocket)

    async def _broadcast_loop(self, interval_s):
        while True:
            await asyncio.sleep(interval_s)
            await self.broadcast_once()

    async def broadcast_once(self):
        """Broadcasts one telemetry frame right now (bypassing the
        interval timer) - used by tests that want deterministic timing
        instead of waiting on the real 2s cadence."""
        if self.dht_fails:
            return  # mirrors `if (isnan(h) || isnan(t)) return;` - no frame sent
        payload = {
            'temp': self.sensor_values['temp'],
            'hum': self.sensor_values['hum'],
        }
        payload['pres'] = self.sensor_values['pres'] if self.bmp_ok else 'N/A'
        payload['current'] = self.sensor_values['current']
        frame = json.dumps(payload)
        stale = []
        for client in self.clients:
            try:
                await client.send(frame)
            except websockets.exceptions.ConnectionClosed:
                stale.append(client)
        for client in stale:
            self.clients.discard(client)

    async def start(self, host='127.0.0.1', port=0, broadcast_interval_s=2.0):
        self._server = await websockets.serve(self._handler, host, port)
        self._broadcast_task = asyncio.create_task(self._broadcast_loop(broadcast_interval_s))
        return self._server.sockets[0].getsockname()

    async def stop(self):
        if self._broadcast_task:
            self._broadcast_task.cancel()
            try:
                await self._broadcast_task
            except asyncio.CancelledError:
                pass
        if self._server:
            self._server.close()
            await self._server.wait_closed()
