#!/usr/bin/env python3
"""
example_ros_client.py

A minimal, plain-asyncio reference client for cachebox_esp32.ino's
protocol - NOT a full rclpy node (no ROS2 installation is available in
this environment to test one against), but the exact connect/parse/send
logic a real ROS2 node would wrap in subscriber/publisher callbacks. Drop
this logic into a Node's __init__/callbacks and it's a working bridge.

Usage against the real board:
    python3 example_ros_client.py ws://cachebox.local/ws
Usage against the mock server for a live demo without hardware:
    python3 example_ros_client.py ws://127.0.0.1:<port>/ws
"""
import asyncio
import json
import sys

import websockets


async def run(uri):
    print(f'connecting to {uri} ...')
    async with websockets.connect(uri) as ws:
        print('connected - sending an initial servo command, then listening for telemetry')

        # ROS -> ESP32: this is exactly what a subscriber callback on
        # e.g. a `/cachebox/servo_cmd` (std_msgs/UInt16) topic would do.
        await ws.send('SERVO:90')

        # ESP32 -> ROS: this is exactly what you'd publish onward as
        # sensor_msgs/Temperature, sensor_msgs/RelativeHumidity,
        # sensor_msgs/FluidPressure, etc. in a real node.
        for _ in range(3):
            raw = await ws.recv()
            data = json.loads(raw)
            temp = data['temp']
            hum = data['hum']
            pres = data['pres']  # float, or the string "N/A" if BMP280 isn't found
            current = data['current']  # raw ADC counts, see cachebox_project_notes.md
            print(f'telemetry: temp={temp}C hum={hum}% pres={pres} current_raw={current}')


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'ws://cachebox.local/ws'
    asyncio.run(run(target))
