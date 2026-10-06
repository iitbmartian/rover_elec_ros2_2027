# rover_mobility code review + stress test

**Package:** `/home/aaravb/rover_ws/src/rover_mobility` (ROS2 Humble,
`ament_python`, single node `mobility_node` - a 4-wheel independent
steer+drive swerve-drive rover controller).

**Scope of the original pass (2026-09-23):** report only. Nothing under
`rover_mobility/`, `config/`, `package.xml`, `setup.py`, or `launch/` was
modified - confirmed by re-checksumming every existing file against
`baseline_checksums.txt` (taken before any work started) at the end of
that review. New files added: `rover_mobility/test/{conftest,test_vroomvroom,
test_explicit_steer,test_drive_pid,test_mobility_node_helpers}.py` (offline
pytest suite) and `rover_mobility_review/runtime/{harness_node,fake_joy_publisher,
fake_can_publisher}.py` (live ROS2 stress-test harness - see
`runtime/runtime_log.md`).

**2026-10-04 update:** the user explicitly requested a real source change
this time (with sign-off on the plan beforehand) - finding #4 below is now
**fixed**, not just documented, and two new capabilities (#17, #18) were
added alongside it. See `track.md`'s 2026-10-04 entry for the full
before/during/after narrative, including a repeat of the exact
stale-install trap from the first review and a real test bug this session
caught in its own new tests. Offline suite is now 109 tests, all passing.

**Method:** full static read of every source file in dependency order,
cross-referenced against the sibling `can_interfaces`/`all_interfaces`
packages' actual built `.msg` output (not just their `.msg` source text);
an 81-test offline pytest suite exercising the pure-Python control math
with adversarial/edge-case inputs; a real `colcon build` +
`ros2 run rover_mobility mobility_node` attempt; and a live ~36-second
ROS2 session running a faithful reconstruction of the control loop
(`harness_node.py`) against scripted synthetic `/joy` and CAN telemetry.

---

## Findings, most severe first

### 1. The node crashes immediately on startup - wrong import package (CONFIRMED, live)
`mobility_node.py:29`: `from can_interfaces.msg import DriveCommand`.
`can_interfaces` only defines `MobilityData` (`can_interfaces/msg/MobilityData.msg`).
Live-reproduced: `ros2 run rover_mobility mobility_node` raises
`ImportError: cannot import name 'DriveCommand' from 'can_interfaces.msg'`
before the node object is even constructed (`runtime_log.md`, step 1).

### 2. Even the "correct" package doesn't build DriveCommand at all (CONFIRMED, live) - a second, independent root cause
`all_interfaces/CMakeLists.txt`'s `rosidl_generate_interfaces()` call only
lists `TelemetryData.msg`, `PidCommands.msg`, `PidGains.msg` (+3 `.srv`
files) - `DriveCommand.msg` is never passed to codegen, despite the file
existing on disk at `all_interfaces/msg/DriveCommand.msg`. Live-confirmed:
`python3 -c "from all_interfaces.msg import DriveCommand"` also raises
`ImportError` (`runtime_log.md`, step 2; offline-reproduced too, in
`test_mobility_node_helpers.py::test_all_interfaces_drive_command_is_not_actually_built`).
**Simply correcting the import's package name in bug #1 would not fix the
node** - `DriveCommand` needs to actually be added to `all_interfaces`'s
`rosidl_generate_interfaces()` list and rebuilt first.

### 3. Even if both imports were fixed, the field names don't match (CONFIRMED, offline)
`all_interfaces/msg/DriveCommand.msg`'s real (declared) schema is just
`int64[] pwm` and `int64[] direction`. But `mobility_node.py:453-456`
writes `drive_command_msg.drive_direction.append(...)`, `.drive_pwm.append(...)`,
`.explicit_direction.append(...)`, `.explicit_pwm.append(...)` - none of
those four names exist on the real message. This would raise
`AttributeError` on the very first tick, once/if bugs #1-#2 are fixed.
Offline-reproduced in `test_mobility_node_helpers.py::test_mobility_node_field_names_do_not_match_real_drive_command_schema`.

### 4. No wheel ever receives CAN telemetry - all 4 wheels run open-loop, permanently (FIXED 2026-10-04, was CONFIRMED offline + live)
**Status: fixed.** Originally: `mobility_node.py` tried to import four
per-wheel message types (`MobilityDataFL/FR/BL/BR`) via `_try_import_msg`,
but `can_interfaces` only defined a single unified `MobilityData` message
with suffixed fields (`explicit_mag_fl`, `explicit_mag_fr`, ...). All four
imports returned `None` (`MSG_TYPES == {'FL': None, 'FR': None, 'BL': None, 'BR': None}`),
so `create_subscription` was never called for any wheel's CAN topic - the
node ran silently on stale/zero feedback forever. Note: `_get_field`'s
candidate-spelling logic was *not* the problem - it matched every real
`MobilityData` field correctly on the first try.

**The fix** (requested directly by the user, with explicit sign-off before
implementation - see `track.md`'s 2026-10-04 entry): added real
`EncoderDataFL/FR/BL/BR` message types to `can_interfaces` (one per wheel,
plus two new fields - see findings #17/#18 below) and pointed `MSG_TYPES`
at them. `MSG_TYPES` is no longer all-`None` - confirmed live, the CAN
subscription loop now actually subscribes all 4 wheels for the first time
in this package's history. Default per-wheel topics renamed
`/can/mobility_data_<suf>` -> `/can/encoder_data_<suf>` to match.
Regression test flipped from `test_all_four_per_wheel_msg_types_fail_to_import`
to `test_all_four_per_wheel_msg_types_now_import_successfully`.

### 5. The EKF mixes degrees and counts - a silent, independent unit-consistency bug (NEW, CONFIRMED offline)
`can_receive()` (`mobility_node.py:295-303`) stores
`format_magnetic_angle()`'s output - **degrees**, range [-180, 180] - directly
as `z[0]` (`mag_count`) into `ExplicitController.update()`. But the EKF's
entire state space (`explicit_steer.py`) is **count-space**, [0, 256).
`deg_to_count()` is only ever applied to the outgoing *target* angle
(`mobility_node.py:409`), never to the incoming sensor reading. Reproduced
in isolation: `test_explicit_steer.py::test_degrees_fed_as_counts_reproduces_real_unit_mismatch_bug`
feeds a real 90&deg; physical angle through the exact data path
`can_receive()` uses and shows the EKF converges to ~126.6&deg;, not 90&deg;.
This is independent of bug #4 - even after fixing the CAN wiring, this
would still bias every steering angle estimate.

### 6. A single corrupted/glitched sensor reading stalls the entire control loop for multiple real seconds (NEW, CONFIRMED live)
`format_magnetic_angle()` (`mobility_node.py:244-250`) wraps the incoming
angle with a **linear** `while real_angle > 180: real_angle -= 360` loop
instead of modulo arithmetic (contrast with `explicit_steer.py`'s
`wrap_count()`/`wrap_count_diff()`, which correctly use `%` and are O(1)
regardless of magnitude). `explicit_mag_*` is a plain `int32` field
(`MobilityData.msg`), so a single bit-flip/glitch on the CAN bus can easily
produce a value in the billions.

Live-reproduced **twice**, independently, in `harness_node.py` sessions
(see `runtime/runtime_log.md` for full timestamps): publishing one
`MobilityData` frame with `explicit_mag_fl = 2_000_000_000` stalled the
100 Hz (`dt=0.01`) control loop's tick cadence for **2.7-3.0 real
seconds**. Isolated and precisely timed outside any ROS context:

| input magnitude | elapsed |
|---|---|
| 1e6 | 0.0002s |
| 1e7 | 0.0016s |
| 2e9 | 0.3887s |

(~5.5 million loop iterations for the 2e9 case; the live multi-wheel stall
is roughly 4x this since the harness applies the same glitched value to
all 4 wheels per frame, plus rclpy/DDS overhead.) Because
`main()` uses a plain `rclpy.spin(node)` with the default
`SingleThreadedExecutor`, this stall blocks *every* other callback too -
including `/joy` - so a single bad CAN reading on one wheel freezes
steering and drive commands for the whole rover for several seconds, not
just that wheel's telemetry. Offline regression test added:
`test_mobility_node_helpers.py::test_linear_wrap_loop_stalls_on_a_glitched_reading`.

### 7. `ExplicitController` at `dt=0` doesn't crash - it silently commands full power (NEW, CONFIRMED offline, discovered empirically)
Unlike `DriveController`/`DrivePID` (plain Python floats/ints - `dt=0`
correctly raises `ZeroDivisionError`, confirmed in `test_drive_pid.py`),
`ExplicitController`'s state (`self.x`) is a numpy array, so `SteerPID`'s
derivative term divides a `numpy.float64` by `dt=0.0`: numpy silently
returns `inf`/`nan` with a `RuntimeWarning` instead of raising. With the
default `kd=0.0`, `0.0 * inf == nan`, so the raw PID output is `NaN` - but
`pwm = max(-1.0, min(1.0, pwm))` then silently clamps that `NaN` to exactly
**+1.0**, because Python's built-in `min`/`max` keep their first argument
whenever a NaN comparison returns `False`. Net effect: `dt=0` produces
neither a crash nor a visible `NaN` in the output - it silently commands
full positive steering power. Confirmed empirically (this was not
predicted in advance - the original hypothesis was a `ZeroDivisionError`
by analogy with the drive controller) in
`test_explicit_steer.py::test_dt_zero_produces_silent_nan_that_gets_clamped_to_full_power`.
`dt` is currently a fixed ROS parameter (default `0.01`), so this needs a
misconfigured launch/params file to trigger - but there is no validation
anywhere guarding against it.

### 8. `package.xml` has a dead dependency and several missing ones (CONFIRMED)
`<depend>custom_interfaces</depend>` refers to a package that does not
exist anywhere in the workspace (`src/` or `install/`) - dead declaration.
Missing `<depend>`s: `sensor_msgs` (used for `Joy`), `can_interfaces`
(imported directly), and `numpy` (used in `controllers/explicit_steer.py`,
declared in neither `package.xml` nor `setup.py`'s `install_requires`).

### 9. Wheel-order docstring in `vroomvroom.py` contradicts the actual geometry - now proven wrong, not just re-asserted (CONFIRMED)
`vroomvroom.py:26`'s docstring claims wheel order "FR, BL, FL, BR".
`mobility_node.py:47-63` carries a long comment explaining this was a
previously-fixed real control bug and asserting the correct order is
`['FR', 'BR', 'FL', 'BL']` - but that fix lives only in a comment, with no
test. This review adds one:
`test_mobility_node_helpers.py::test_wheel_order_matches_actual_vroomvroom_geometry`
independently re-derives the FR/BR/FL/BL mapping directly from
`VroomVroom.from_R_vec`'s `w1..w4` formula (not by trusting either
docstring) and confirms `WHEEL_ORDER` matches the real geometry.
`vroomvroom.py`'s own docstring is the stale one and should be corrected
to match.

**Also independently discovered while writing this test**: the *installed*
copy of `mobility_node.py` was stale relative to `src/` and still had the
OLD, pre-fix `WHEEL_ORDER = ['FR', 'BL', 'FL', 'BR']` - the exact bug the
long comment says was already fixed. Running `ros2 run`/`ros2 launch`
without an intervening `colcon build` silently re-introduces a real,
previously-fixed control bug (see track.md for the rebuild that resolved
this for the rest of this review).

### 10. EKF: identical measurement rows can make the Kalman gain singular (NEW, CONFIRMED offline)
`H`'s mag and quad rows are both `[1, 0]` (structurally indistinguishable
to the model - differentiated only via `R`). If `r_diag[0] == r_diag[1] == 0`,
`S = H @ P @ H.T + R` becomes singular and `np.linalg.inv(S)` raises
`LinAlgError`. Confirmed in
`test_explicit_steer.py::test_identical_measurement_rows_with_zero_variance_are_singular`.
Not triggered by current `params.yaml` defaults (`steer_r_diag: [0.05, 0.02, 0.01]`),
but unguarded against a future misconfiguration.

### 11. EKF has no control-input term - "holding position" with no CAN data is really just decay-to-stall (NEW, CONFIRMED offline)
`predict()` (`explicit_steer.py:82-85`) is `x = F @ x` only - no `B*u`
term feeding back the commanded pwm. Combined with bug #4 (z is
permanently `None`), the filter isn't tracking or holding anything
physically meaningful: `omega_count` exponentially decays toward 0 every
tick (via `F[1,1] = 1 - dt/t_motor`) regardless of what the real wheel is
doing, and `theta_count` drifts only by whatever residual `omega`
integrates before it dies out, then stalls. Confirmed in
`test_explicit_steer.py::test_predict_only_no_feedback_just_decays_towards_frozen_position`.

### 12. No anti-windup on either PID (CONFIRMED offline, dormant today)
Neither `SteerPID` nor `DrivePID` clamps or back-calculates the integral
term. Dormant with current defaults (`*_pid_ki: 0.0` in `params.yaml`),
but unguarded if either gain is ever set nonzero - confirmed both integral
terms grow unbounded under sustained error
(`test_explicit_steer.py`/`test_drive_pid.py::test_no_anti_windup_integral_grows_unbounded`).

### 13. Unguarded zero-division / negative-shift parameters (CONFIRMED offline)
None of the following are validated anywhere, despite the node validating
five other array-length parameters (`mobility_node.py:155-161`):
- `dt=0` -> `ZeroDivisionError` in `DrivePID`/`SteerPID`'s derivative term when using plain floats (`DriveController`); silently produces NaN-then-clamped-to-full-power in `ExplicitController` (see finding #7).
- `steer_t_motor=0.0` -> `ZeroDivisionError` at `ExplicitController.__init__` (building `F`).
- `drive_max_ticks_per_dt=0.0` -> `ZeroDivisionError` at the end of `DriveController.step()`.
- `drive_tick_counter_bits` negative -> `ValueError: negative shift count` (`1 << int(bits)`).
- `drive_tick_counter_bits == 0` -> does *not* crash, but silently zeroes all drive velocity feedback (`1 << 0 == 1`, every tick delta collapses mod 1 to 0) - a silent-degradation edge case.

All confirmed in `test_explicit_steer.py`/`test_drive_pid.py`.

### 14. A bare `print()` bypasses the ROS logger (CONFIRMED)
`mobility_node.py:481` uses `print("\r" + ...)` for a per-tick debug status
line with carriage-return overwriting. This interleaves badly with
`ros2 launch`/multi-process output and can't be filtered or leveled like
the rest of the node's logging (which otherwise consistently uses
`self.get_logger()`).

### 15. Referenced sibling files don't exist anywhere in the workspace (CONFIRMED)
Comments repeatedly cite `drive_controller.py`, `rover_sim.py`/`SteerPlant`,
and `mobility_can.py` as sources of real calibration values and simulated
tuning data - none exist under `rover_ws/src` (or anywhere else searched).
Either they live in a different branch/repo not checked out here, or that
context is unrecoverable from this workspace. Worth chasing down before
trusting any cited value (e.g. the `16.17/93.95/355.80/260.50` calibration
numbers `params.yaml` explicitly warns not to reuse blindly).

### 16. Checked and found NOT to be a bug: thread-safety / callback reentrancy
`main()` uses a plain `rclpy.spin(node)`, which defaults to
`SingleThreadedExecutor` - callbacks (timer, `/joy`, CAN subscriptions)
cannot run concurrently or reenter each other. Noted here explicitly so
it's not left as an open question for a future review.

### 17. NEW (2026-10-04): per-wheel limit switch telemetry, currently a no-op hook
Each `EncoderData<WHEEL>.msg` carries `int32[2] ls_<suf>` (added alongside
the fix to finding #4). `can_receive()` stores both values into
`_latest_limit_switch[i]` and calls `_on_limit_switch(i)` whenever
`ls_<suf>[0] == 1` (triggered) - but `_on_limit_switch()` is an
intentional, literal no-op today, explicitly requested as a placeholder
"reserved for future calibration use." Index 1 of the 2-integer `ls_<suf>`
field has no defined meaning yet on the firmware side either - stored but
unused. Not a bug; flagging so a future session doesn't mistake the
no-op for an oversight.

### 18. NEW (2026-10-04): sensor-health gating in the steering EKF
Each `EncoderData<WHEEL>.msg` also carries `int32[2] sensor_check_<suf>` =
`[mag_sensor_up, imu_sensor_up]` (1 = up, 0 = down; quadrature has no
health flag and is always trusted). `mobility_node.py`'s `loop()` now
reads the latest per-wheel values and passes a `trust=(mag_ok, 1, imu_ok)`
tuple into `ExplicitController.step()`/`.update()`
(`controllers/explicit_steer.py`) every tick. A down sensor is excluded by
zeroing its row of `H` for that update - deliberately NOT by zeroing its
`R` entry, which would mean "fully trust" in Kalman-filter terms and,
combined with finding #10 (`H`'s mag/quad rows are identical), risks
exactly the `LinAlgError` documented there. Proven safe and effective in
`test_explicit_steer.py::TestExplicitControllerTrust` (an untrusted
channel fed garbage converges identically to a controller that never saw
that garbage at all; excluding a channel under normal, nonzero `r_diag`
does not raise). Default (no `sensor_check` field present, or not yet
received) is "trust both" - this gate only ever reduces trust, it never
raises it above what `r_diag` already encodes.

---

## Existing test coverage (pre-existing files, unchanged by this review)

Only ament boilerplate (`test_flake8.py`, `test_pep257.py`, a `@pytest.mark.skip`'d
`test_copyright.py`) existed before this review - zero functional coverage
of the control-theory-heavy code. The pre-existing package files
themselves do not pass their own lint gates either: 53 flake8 + 27 pep257
findings, entirely in `mobility_node.py`/`controllers/*.py`/`setup.py`/
`launch/mobility.launch.py` (see `offline_test_results.md` for the
file-by-file breakdown) - out of scope for this report-only pass, noted
here for completeness.

## What was added by this review

- `rover_mobility/test/{conftest,test_vroomvroom,test_explicit_steer,test_drive_pid,test_mobility_node_helpers}.py` - 81 offline pytest tests, all passing, 0 flake8/pep257 findings. See `offline_test_results.md`.
- `runtime/{harness_node,fake_joy_publisher,fake_can_publisher}.py` - live ROS2 stress-test harness. See `runtime/runtime_log.md`.
- This report, `track.md` (running step log), `offline_test_results.md`.

## Verification that no existing package file was modified

```
$ cd rover_mobility && find . -path ./test -prune -o -type f -print | sort | xargs md5sum | diff - ../rover_mobility_review/baseline_checksums.txt
```
The only diff lines are generated `__pycache__/*.pyc` bytecode caches
(created by importing the modules while testing) and a `.pytest_cache/`
directory - neither is source, both are standard, gitignore-typical build
byproducts. Every actual source file - `mobility_node.py`, all of
`controllers/*.py`, `config/params.yaml`, `package.xml`, `setup.py`,
`setup.cfg`, `launch/mobility.launch.py`, and `resource/rover_mobility` -
is byte-identical (same md5sum) to its state at the start of this review.
