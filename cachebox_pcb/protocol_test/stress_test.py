#!/usr/bin/env python3
"""
stress_test.py

Exercises the cachebox_esp32.ino <-> ROS-node WebSocket protocol against
mock_esp32_server.py (a faithful Python re-implementation of the firmware's
message handling - see that file's docstring for exactly what "faithful"
means and its limits). This validates the PROTOCOL a ROS-side client would
be built against; it does not compile or run the actual C++ firmware (no
arduino-cli/hardware available in this environment).

Run: python3 stress_test.py
"""
import asyncio
import json
import sys

import websockets

from mock_esp32_server import MockCacheboxServer

PASS = []
FAIL = []


def check(name, condition, detail=''):
    if condition:
        PASS.append(name)
        print(f'  PASS  {name}')
    else:
        FAIL.append(name)
        print(f'  FAIL  {name}  {detail}')


async def recv_json(ws, timeout=1.0):
    raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
    return json.loads(raw)


async def expect_no_message(ws, timeout=0.3):
    try:
        raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
        return False, raw
    except asyncio.TimeoutError:
        return True, None


async def main():
    server = MockCacheboxServer()
    host, port = await server.start(broadcast_interval_s=999)  # manual broadcast_once() for determinism
    uri = f'ws://{host}:{port}/ws'
    print(f'mock cachebox server listening at {uri}\n')

    # ---- Scenario 1: normal telemetry frame shape ----
    print('Scenario 1: telemetry JSON schema')
    async with websockets.connect(uri) as ws:
        await server.broadcast_once()
        data = await recv_json(ws)
        check('has temp/hum/pres/current keys',
              set(data.keys()) == {'temp', 'hum', 'pres', 'current'}, data)
        check('temp is a number', isinstance(data['temp'], (int, float)), data)
        check('hum is a number', isinstance(data['hum'], (int, float)), data)
        check('current is an int (raw ADC counts)', isinstance(data['current'], int), data)

    # ---- Scenario 2: servo command, normal range ----
    print('\nScenario 2: SERVO command, in-range')
    async with websockets.connect(uri) as ws:
        await ws.send('SERVO:45')
        await asyncio.sleep(0.1)
        check('servo_angle set to 45', server.servo_angle == 45, server.servo_angle)

    # ---- Scenario 3: out-of-range clamping ----
    print('\nScenario 3: SERVO command clamping (constrain(angle, 0, 180))')
    async with websockets.connect(uri) as ws:
        await ws.send('SERVO:999')
        await asyncio.sleep(0.1)
        check('SERVO:999 clamps to 180', server.servo_angle == 180, server.servo_angle)

        await ws.send('SERVO:-999')
        await asyncio.sleep(0.1)
        check('SERVO:-999 clamps to 0', server.servo_angle == 0, server.servo_angle)

    # ---- Scenario 4: non-numeric angle (Arduino toInt() -> 0) ----
    print('\nScenario 4: SERVO command with non-numeric angle')
    async with websockets.connect(uri) as ws:
        server.servo_angle = 77  # known starting value
        await ws.send('SERVO:abc')
        await asyncio.sleep(0.1)
        check('SERVO:abc parses as 0 (Arduino toInt() semantics), clamped to 0',
              server.servo_angle == 0, server.servo_angle)

    # ---- Scenario 5: unrecognized command is silently ignored ----
    print('\nScenario 5: unrecognized / removed command (LED_ON) is ignored')
    async with websockets.connect(uri) as ws:
        server.servo_angle = 33
        await ws.send('LED_ON')
        await asyncio.sleep(0.1)
        check('LED_ON has no effect (command was intentionally removed)',
              server.servo_angle == 33, server.servo_angle)
        check('LED_ON was received but produced no state change',
              server.commands_received[-1] == 'LED_ON')

    # ---- Scenario 6: DHT11 read failure -> no telemetry frame sent ----
    print('\nScenario 6: simulated DHT11 failure suppresses the broadcast')
    async with websockets.connect(uri) as ws:
        server.dht_fails = True
        await server.broadcast_once()
        no_msg, raw = await expect_no_message(ws)
        check('no frame sent while DHT11 read fails (matches isnan() early-return)',
              no_msg, raw)
        server.dht_fails = False

    # ---- Scenario 7: BMP280 not found -> "pres":"N/A" ----
    print('\nScenario 7: BMP280 unavailable falls back to "pres":"N/A"')
    async with websockets.connect(uri) as ws:
        server.bmp_ok = False
        await server.broadcast_once()
        data = await recv_json(ws)
        check('pres is the string "N/A" when BMP280 is not found',
              data.get('pres') == 'N/A', data)
        server.bmp_ok = True

    # ---- Scenario 8: multiple simultaneous clients all get the broadcast ----
    print('\nScenario 8: broadcast reaches multiple simultaneous clients (ws.textAll semantics)')
    async with websockets.connect(uri) as ws_a, websockets.connect(uri) as ws_b:
        await server.broadcast_once()
        data_a = await recv_json(ws_a)
        data_b = await recv_json(ws_b)
        check('both clients received a frame', data_a is not None and data_b is not None)
        check('both clients received the SAME frame', data_a == data_b, (data_a, data_b))

    # ---- Scenario 9: rapid reconnect doesn't wedge the server ----
    print('\nScenario 9: rapid connect/disconnect cycling')
    ok = True
    try:
        for _ in range(20):
            ws = await websockets.connect(uri)
            await ws.send('SERVO:10')
            await ws.close()
    except Exception as e:
        ok = False
        print(f'    exception during rapid reconnect: {e!r}')
    check('20 rapid connect/send/disconnect cycles complete without server error', ok)
    async with websockets.connect(uri) as ws:
        await server.broadcast_once()
        data = await recv_json(ws)
        check('server still broadcasts normally after reconnect storm', data is not None)

    # ---- Scenario 10: oversized single-frame message ----
    # NOTE ON FIRMWARE (not just this mock): the real onWsEvent() builds
    # `String msg` by appending one char at a time with no length cap:
    #   String msg = ""; for (size_t i = 0; i < len; i++) msg += (char)data[i];
    # An oversized WS_TEXT frame (accidental or malicious) would grow that
    # String with repeated heap reallocations on a memory-constrained
    # ESP32 - a real robustness gap worth knowing about, flagged in the
    # review doc rather than silently "fixed" here (out of today's asked
    # scope, and no hardware to verify a safe cap against).
    print('\nScenario 10: oversized single-frame message does not crash the server')
    async with websockets.connect(uri) as ws:
        huge = 'SERVO:1' + ('0' * 50000)  # ~50KB single text frame
        await ws.send(huge)
        await asyncio.sleep(0.2)
        check('server survived a 50KB frame and clamped the parsed angle',
              server.servo_angle == 180, server.servo_angle)

    await server.stop()

    print(f'\n{"="*60}')
    print(f'{len(PASS)} passed, {len(FAIL)} failed')
    if FAIL:
        print('FAILED:', ', '.join(FAIL))
    return 0 if not FAIL else 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
