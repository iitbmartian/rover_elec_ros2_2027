# Runtime / integration test log

Workspace was built with `colcon build --packages-select can_interfaces
all_interfaces rover_mobility` before any of this (see track.md for the
two stale-build-artifact directories that had to be removed first). The
installed `mobility_node.py` was verified byte-identical to `src/`.

## Step 1: `ros2 run rover_mobility mobility_node` - real, live crash

Command: `ros2 run rover_mobility mobility_node`. Confirms bug #1 with a
live traceback, not just a static read of the import line.

```
Traceback (most recent call last):
  File "/home/aaravb/rover_ws/install/rover_mobility/lib/rover_mobility/mobility_node", line 33, in <module>
    sys.exit(load_entry_point('rover_mobility==0.0.0', 'console_scripts', 'mobility_node')())
  File "/home/aaravb/rover_ws/install/rover_mobility/lib/rover_mobility/mobility_node", line 25, in importlib_load_entry_point
    return next(matches).load()
  File "/usr/lib/python3.10/importlib/metadata/__init__.py", line 171, in load
    module = import_module(match.group('module'))
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/aaravb/rover_ws/install/rover_mobility/lib/python3.10/site-packages/rover_mobility/mobility_node.py", line 29, in <module>
    from can_interfaces.msg import DriveCommand
ImportError: cannot import name 'DriveCommand' from 'can_interfaces.msg' (/home/aaravb/rover_ws/install/can_interfaces/local/lib/python3.10/dist-packages/can_interfaces/msg/__init__.py)
[ros2run]: Process exited with failure 1
exit code: 1
```

## Step 2: even the "corrected" import target fails too

Command: `python3 -c "from all_interfaces.msg import DriveCommand"`.
Confirms finding #2: `DriveCommand` is not rosidl-built in `all_interfaces`
either, so simply fixing the import's package name would not unblock the
node.

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: cannot import name 'DriveCommand' from 'all_interfaces.msg' (/home/aaravb/rover_ws/install/all_interfaces/local/lib/python3.10/dist-packages/all_interfaces/msg/__init__.py)
```

## Step 3-4: fallback harness live session

Since the real executable cannot proceed past step 1 without editing
`rover_mobility`'s own source (out of scope - report only), `runtime/harness_node.py`
reconstructs the real control loop: it imports the actual, unmodified
`VroomVroom`/`ExplicitController`/`DriveController` classes and
`MobilityNode`'s static helpers, subscribes to `/joy` and a single working
`can_interfaces/msg/MobilityData` topic (`/review/can/mobility_data`
instead of the real node's unbuildable per-wheel scheme), and runs the
identical per-tick math at the real `dt=0.01` (100 Hz) under `rclpy.spin`.
This is a stress-test aid for the math under live ROS timing, not a
validation of the real (currently crashed) executable.

Ran `harness_node.py` for ~3600 ticks (~36s of control-loop time) while
`fake_can_publisher.py` and `fake_joy_publisher.py` fed it scripted
sequences of synthetic CAN telemetry and joystick input (normal deltas,
encoder rollover, stalled values, extreme int32 glitch values; neutral,
full forward/reverse, full rotate L/R, crab toggle, simultaneous
throttle+rotate+crab, rapid reversals, and a malformed short axes array).
**No unhandled exception occurred during the session** - the harness ran
the full script and only stopped when deliberately killed.

### New finding discovered live, not predictable from static reading alone

The session's timer-callback cadence (tick N+50 should log ~0.5s after
tick N, since `dt=0.01`) held to within a few ms for the entire run -
**except for one large, exactly-reproducible stall right after the
`extreme_glitch` CAN frame** (`explicit_mag_fl=2_000_000_000`, simulating
a corrupted/glitched sensor byte - the field is a plain `int32` per
`MobilityData.msg`, so a single bit-flip on the bus can produce a value in
this range):

Run 1: tick 300 logged at `...485.590`, tick 350 (next scheduled 50 ticks
later, expected +0.5s) instead logged at `...488.822` - a **2.73s** stall.

Run 2 (independent re-run, separate log files per process to rule out a
logging artifact): `extreme_glitch` published at `...579.231089272`; tick
300 logged at `...578.754482694` (normal cadence); tick 350 logged at
`...581.724905502` - a **2.97s** stall, landing in exactly the window
right after the glitch frame was received.

**Root cause, isolated and precisely timed**: `MobilityNode.format_magnetic_angle()`
(`mobility_node.py:244-250`) wraps the incoming angle into [-180, 180]
using a linear `while real_angle > 180: real_angle -= 360` loop, instead
of modulo arithmetic (contrast with `explicit_steer.py`'s `wrap_count()`/
`wrap_count_diff()`, which correctly use `%` and are O(1) regardless of
input magnitude). Timed in isolation:

```
input=1e+06   result=-80.0    elapsed=0.0002s
input=1e+07   result=-80.0    elapsed=0.0016s
input=2e+09   result=-160.0   elapsed=0.3887s
```

Cost scales linearly with the input magnitude (~5.5 million loop
iterations for a 2e9 input). In the live harness, the same glitched value
is applied to **all 4 wheels** per CAN frame (the synthetic message sets
an identical value on every wheel's field, matching how `can_receive()`
loops per-wheel), consistent with the observed ~2.5-3s multi-wheel stall
being roughly 4x the ~0.39s single-call cost plus rclpy/DDS overhead.

**Impact**: a control loop specified to run at 100 Hz (`dt=0.01`) can be
stalled for several real seconds by a single out-of-range sensor reading
on one wheel - during which `rclpy.spin()`'s single-threaded executor
blocks entirely (confirmed elsewhere in this review that the node uses
the default `SingleThreadedExecutor`), so no other callback (including
`/joy`) runs either. On real hardware this means a transient CAN glitch
freezes the entire rover's steering/drive command loop for multiple
seconds, not just the one affected wheel's telemetry.
