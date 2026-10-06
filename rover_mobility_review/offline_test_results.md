# Offline pytest results - rover_mobility control modules

Pure-Python unit/stress tests against `VroomVroom`, `ExplicitController`,
`DriveController`, and `mobility_node.py`'s static helpers. No ROS runtime
required (rclpy is never spun up) - `conftest.py` only patches
`can_interfaces.msg.DriveCommand` in memory so `mobility_node.py` can be
imported at all (see bug #1 in `rover_mobility_review.md`).

**Command:**
```
source /opt/ros/humble/setup.bash && source install/setup.bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  src/rover_mobility/test/test_vroomvroom.py \
  src/rover_mobility/test/test_explicit_steer.py \
  src/rover_mobility/test/test_drive_pid.py \
  src/rover_mobility/test/test_mobility_node_helpers.py -v
```
(`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` works around an unrelated environment
issue: the `anyio` pytest plugin installed in this environment is
incompatible with the system's pytest 6.2.5 and crashes plugin autoload
before any test runs.)

**Result (2026-10-04): 109 passed, 0 failed** (81 as of the 2026-09-23
review, captured verbatim in `pytest_final_output.txt`; +1 for
`test_linear_wrap_loop_stalls_on_a_glitched_reading` during that same
review; +12 added later that same day in the zero-reference/PID-tuner
session - `_apply_zero`/`_on_set_parameters` tests; +15 added 2026-10-04
when the CAN-message fix landed - `TestCanReceiveLimitSwitchAndSensorCheck`
(7 tests) and `TestExplicitControllerTrust` (5 tests) plus flipping
`test_all_four_per_wheel_msg_types_fail_to_import` into
`..._now_import_successfully` - see `rover_mobility_review.md` findings
#4/#17/#18 and `track.md`'s 2026-10-04 entry for the full story,
including two real bugs (one a stale-install repeat, one a test's own
wheel-index mixup) this session caught in itself before they could hide
anything).

**Lint status of the 5 new files** (`test/conftest.py`,
`test_vroomvroom.py`, `test_explicit_steer.py`, `test_drive_pid.py`,
`test_mobility_node_helpers.py`): 0 flake8 errors, 0 pep257 errors when
checked directly. The package-wide `test/test_flake8.py`/`test_pep257.py`
boilerplate tests still fail, but only because of pre-existing lint debt in
`mobility_node.py`/`controllers/*.py`/`setup.py`/`launch/mobility.launch.py`
(53 flake8 + 27 pep257 findings, all in those untouched files) - confirmed
by re-running flake8/pep257 scoped to just the new files (0 findings) vs.
scoped to the whole package (53/27 findings, same file breakdown as
before any of this review's files existed).

## Notable results and what they prove

| Test | File | Proves |
|---|---|---|
| `test_wheel_order_matches_actual_vroomvroom_geometry` | test_mobility_node_helpers.py | `WHEEL_ORDER = ['FR','BR','FL','BL']` is geometrically correct against `VroomVroom`'s actual `w1..w4` formula (bug #5's docstring claim is the wrong one, confirmed by direct computation, not just re-trusting the comment). |
| `test_all_four_per_wheel_msg_types_fail_to_import` | test_mobility_node_helpers.py | `MSG_TYPES` is `{'FL': None, 'FR': None, 'BL': None, 'BR': None}` - offline, real confirmation of bug #3 (no wheel is ever subscribed to CAN telemetry) without needing a live node. |
| `test_all_interfaces_drive_command_is_not_actually_built` | test_mobility_node_helpers.py | `from all_interfaces.msg import DriveCommand` raises `ImportError` - proves bug #2 is a *second, independent* root cause from bug #1 (wrong package), not fixed by just correcting the import path. |
| `test_field_matching_would_work_for_every_wheel_and_signal` | test_mobility_node_helpers.py | `_get_field`'s candidate-spelling logic matches every real `MobilityData` field on the first try - the missing-subscription bug (#3) is the *sole* blocker on telemetry, not a secondary field-naming bug. |
| `test_degrees_fed_as_counts_reproduces_real_unit_mismatch_bug` | test_explicit_steer.py | Reproduces `can_receive()`'s actual data path in isolation: a real 90&deg; physical angle converges in the EKF to ~126.6&deg;, not 90&deg; - concrete evidence for the new EKF degrees/counts unit-mismatch finding. |
| `test_predict_only_no_feedback_just_decays_towards_frozen_position` | test_explicit_steer.py | With `z` permanently `None` (today's real state per bug #3), `omega_count` decays to 0 and `theta_count` stalls - the EKF is not "holding position," it's just drifting to a stop. |
| `test_dt_zero_produces_silent_nan_that_gets_clamped_to_full_power` | test_explicit_steer.py | **Discovered empirically, not predicted in advance.** `dt=0` in `ExplicitController` does NOT raise `ZeroDivisionError` (unlike `DriveController`/`DrivePID`, which are plain Python floats) - it silently produces `NaN` via numpy, which Python's `max(-1.0, min(1.0, nan))` then silently clamps to a concrete **+1.0** (full positive steering power) because NaN comparisons are always `False`. Worse than a crash: no exception, no NaN in the output, just a wrong hard-power command. New finding, promoted to the main report. |
| `test_identical_measurement_rows_with_zero_variance_are_singular` | test_explicit_steer.py | Confirms `H`'s identical mag/quad rows make the Kalman gain computation singular (`LinAlgError`) if both those measurement variances are ever driven to 0. |
| `test_negative_tick_counter_bits_raises_value_error` / `test_tick_counter_bits_zero_is_degenerate_but_does_not_crash` | test_drive_pid.py | `drive_tick_counter_bits < 0` crashes at construction (`ValueError`); `== 0` silently zeroes all velocity feedback without crashing. |
| `test_max_ticks_per_dt_zero_raises_zero_division` / `test_dt_zero_raises_zero_division` (drive_pid) | test_drive_pid.py | Unlike the steering EKF, `DriveController`'s equivalent zero-division cases *do* raise cleanly, since none of its math touches numpy. |
| `test_no_anti_windup_integral_grows_unbounded` (both PIDs) | test_explicit_steer.py, test_drive_pid.py | Confirms neither PID has an integral clamp - dormant today (`ki=0.0` in params.yaml) but unguarded. |

## Bugs found by writing/running these tests that were NOT in the original recon

While building this suite, running it under `source install/setup.bash`
uncovered that the **installed package was stale** relative to `src/`
(the installed copy still had the pre-fix `WHEEL_ORDER = ['FR','BL','FL','BR']`
- the very ordering bug the current source's long comment says was already
fixed). This is written up as its own finding in `rover_mobility_review.md`
since it means running `ros2 run`/`ros2 launch` without an intervening
`colcon build` silently re-introduces a real, previously-fixed control bug.
The workspace was rebuilt (`colcon build --packages-select can_interfaces
all_interfaces rover_mobility`) before any further testing in this review;
two pre-existing, unrelated stale `ament_cmake_python` build-artifact
directories (in `can_interfaces` and `all_interfaces`) had to be removed
first to let the rebuild proceed at all (generated build output only,
no source files were touched - see track.md).
