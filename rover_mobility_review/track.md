# Track: rover_mobility Review + Stress Test

Running log of every step taken during this review. Updated live as work progresses.

## 2026-09-23

- Plan approved: full runtime test + offline unit tests, report-only (no fixes to existing package source).
- Created deliverables directory `rover_mobility_review/` (plain dir, no package.xml, colcon ignores it) with `runtime/` subdir.
- Created this `track.md`.
- Static review pass complete: read package.xml, setup.py, params.yaml, vroomvroom.py, explicit_steer.py, drive_pid.py, mobility_node.py, launch/mobility.launch.py, can_interfaces/msg/MobilityData.msg, all_interfaces/msg/DriveCommand.msg, both CMakeLists.txt files, and the built install/ trees. All 8 known bugs + all 6 new findings from the Plan agent's grounded read-through were confirmed directly against source (see rover_mobility_review.md once written).
- Confirmed via `find`/`ls` against `install/`: `all_interfaces` never builds `DriveCommand` (CMakeLists only lists TelemetryData/PidCommands/PidGains) — independent root cause from the wrong-package import bug. `can_interfaces` only builds `MobilityData` (no per-wheel FL/FR/BL/BR types). `drive_controller.py`/`rover_sim.py`/`mobility_can.py` confirmed absent anywhere under rover_ws/src.
- Snapshot: recorded md5sums of every existing rover_mobility package file (excluding test/) to `rover_mobility_review/baseline_checksums.txt`, for the end-of-task no-source-touched verification.
- Wrote offline pytest suite under `rover_mobility/test/`: `conftest.py` (in-memory shim for the broken top-level import), `test_vroomvroom.py`, `test_explicit_steer.py`, `test_drive_pid.py`, `test_mobility_node_helpers.py`. Existing 3 boilerplate test files untouched.
- First pytest run (before rebuilding, using the then-current `install/`) surfaced a genuine and unexpected finding: `WHEEL_ORDER` from the installed copy of `mobility_node.py` was `['FR','BL','FL','BR']` (the OLD, pre-fix ordering), while `src/` has `['FR','BR','FL','BL']` (fixed). The installed package was stale relative to src.
- Rebuilt the workspace: `colcon build --packages-select can_interfaces all_interfaces rover_mobility`. Had to first `rm -rf` two stale generated `ament_cmake_python` symlink-conflict directories under `build/can_interfaces/...` and `build/all_interfaces/...` (pure generated build output — compiled `.so`, generated C/py stubs — safe to delete and regenerate; no source files touched). Confirmed post-build that `install/.../mobility_node.py` is now byte-identical to `src/.../mobility_node.py`, and that `all_interfaces` still does not build `DriveCommand` (finding #2 reconfirmed post-rebuild).
- Fixed 3 genuinely-wrong test expectations found by actually running the suite (not test bugs I'd have caught by re-reading alone): (1) `format_magnetic_angle(-190, offset=10)` arithmetic — correct expected value is 160.0, not 170.0; (2) wheel-order test failure was caused by the stale install, not a test bug — passes after rebuild; (3) `ExplicitController` at `dt=0` does NOT raise `ZeroDivisionError` like `DriveController` does — it silently produces NaN via numpy which then gets clamped to a hard +1.0 pwm by Python's NaN-insensitive `min`/`max`. This is a new, more severe finding than originally hypothesized — added to the report list.
- All 80 offline tests pass. Ran the ament boilerplate `test_flake8.py`/`test_pep257.py`/`test_copyright.py` too: after several rounds of mechanical docstring/import-order/blank-line fixes (scripted, then hand-corrected where the auto-wrap produced awkward mid-phrase breaks), the 5 new test files are fully flake8- and pep257-clean. Confirmed via file-scoped flake8/pep257 runs that all remaining lint findings (53 flake8 + 27 pep257) are exclusively in the pre-existing package files (`mobility_node.py`, `controllers/*.py`, `setup.py`, `launch/mobility.launch.py`) that are out of scope (report-only, not modified) — not in anything we wrote.
- Wrote `offline_test_results.md` summarizing results and highlighting which tests provide evidence for which bugs, plus the stale-install finding.
- Ran `ros2 run rover_mobility mobility_node` — confirmed the live `ImportError: cannot import name 'DriveCommand' from 'can_interfaces.msg'` crash (bug #1), captured in `runtime/runtime_log.md`. Also confirmed `from all_interfaces.msg import DriveCommand` independently fails too (bug #2, second root cause).
- Built `runtime/harness_node.py` (standalone rclpy node reconstructing the real control loop from the unmodified VroomVroom/ExplicitController/DriveController classes + MobilityNode's static helpers, via the same in-memory import shim as conftest.py) plus `runtime/fake_joy_publisher.py` and `runtime/fake_can_publisher.py` (scripted synthetic input sequences covering normal/edge-case/adversarial inputs on both topics).
- First harness attempt crashed too (same top-level ImportError, since mobility_node.py is imported directly) — fixed by adding the same DriveCommand shim inside harness_node.py before its imports.
- Ran the full live session twice (once combined-log, once with separate per-process log files to rule out a logging artifact): ~1350–3600 ticks each, no unhandled exception in either run, harness only stopped when deliberately killed.
- **Live discovery, not predicted in advance**: both runs showed one large (~2.7–3.0s), exactly-reproducible stall in the otherwise-steady 100Hz tick cadence, landing right after the `extreme_glitch` synthetic CAN frame (`explicit_mag_fl=2_000_000_000`). Root-caused and precisely timed in isolation: `format_magnetic_angle()`'s linear `while` wrap loop takes ~0.39s for a single 2e9 input (vs. O(1) modulo used elsewhere in the codebase) — with `SingleThreadedExecutor`, this blocks every other callback too. Added as finding #6 in the main report, plus an offline regression test (`test_mobility_node_helpers.py::test_linear_wrap_loop_stalls_on_a_glitched_reading`) so it's caught without needing a live session. Suite is now 81 tests, still all passing, still 0 flake8/pep257 findings on the new files.
- Wrote `runtime/runtime_log.md` (verbatim crash tracebacks + the stall investigation) and the main `rover_mobility_review.md` report tying together all 16 findings (8 originally known, 6 new from deeper static/live analysis, 1 stale-install discovery, 1 explicitly-checked-and-cleared item).
- Final safety check: `find . -path ./test -prune -o -type f -print | xargs md5sum | diff - baseline_checksums.txt` — only diffs are generated `__pycache__`/`.pytest_cache` artifacts (not source). Every actual package source file is byte-identical to its state at the start of this review. Confirmed report-only scope was honored.

## Review complete

All deliverables are in place: this file, `rover_mobility_review.md` (main
report), `offline_test_results.md`, `runtime/runtime_log.md`, the 5 new
test files under `rover_mobility/test/`, and the 3 new runtime harness
files under `runtime/`. 16 findings documented with concrete evidence
(file:line + repro command/test name + captured real output for each).
No existing package file was modified.

---

## 2026-10-04 — fixing bug #3/#4 for real: per-wheel CAN messages now exist

Unlike the two prior sessions on this package (review-only, then the
zero-reference/PID-tuner session), this one explicitly modifies
`mobility_node.py`'s own source - requested directly by the user, who
also asked to be walked through the plan and asked before any change was
made.

### What triggered this

The user pointed at an inline comment someone had inserted directly above
`can_receive()` in `mobility_node.py`:
```
# CHANGE THE CAN_RECEIVE TO 4 DIFFERENT MESSAGES FOR EACH WHEEL HUB (encoder_data_FL, encoder_data_FR, ...BL, ...BR)
# for each wheel: extract explicit_mag_fl, explicit_quad_fl, explicit_imu_fl, drive_quad_fl
# also receive limit switch data for eg.: ls_fl
# also receive if sensors are up for eg.: sensor_check_fl (order is mag, imu)
```
Checked `can_interfaces` fresh: still unchanged since the first review -
only `MobilityData.msg` existed, no per-wheel message types, no
`ls_*`/`sensor_check_*` fields anywhere. This is literally bug #3/#4 from
the original review, finally getting its real fix (previously: report
only, no source changes authorized).

### Clarified before writing any code

Per the user's explicit "ask me before changes" instruction, confirmed
via `AskUserQuestion` before touching anything:
1. Should `can_interfaces` actually gain the new message types, or should
   `mobility_node.py` just be prepared to use them gracefully once someone
   else adds them? **User: create `can_interfaces` message types too, I'll
   specify the details.**
2. `sensor_check_fl`'s exact shape ("order is mag, imu"). **User: a ROS
   integer array, one integer (0 or 1) per sensor - not boolean.**
3. `ls_fl`'s exact shape. **User: one physical limit switch per wheel, but
   the `ls` message carries two integers as well** (symmetric with
   sensor_check's 2-integer shape).
4. What to do with the new data once received. **User: if a sensor_check
   entry shows a sensor is down, exclude it from the Kalman filter so it
   isn't accounted for in the PWM computation; when the limit switch
   reads 1, call a dummy no-op function for now (reserved for future
   calibration use).**

One more confirmation was needed before implementing: the user's literal
phrasing ("put trust ... as 0") would, if taken as "set that sensor's
`R` value to 0," be backwards and dangerous in Kalman-filter terms - R=0
means "fully trust," and since `H`'s mag/quad rows are already identical
(a pre-existing finding from the first review), a literal R=0 risks
exactly the `LinAlgError` documented there. Proposed instead: zero that
sensor's row in `H` for the tick (mathematically proven safe - `S`'s
affected diagonal entry reduces to just `R[i,i]`, which stays positive,
and the corresponding Kalman gain column becomes exactly zero regardless
of the untrusted measurement's value). **User confirmed this translation
is correct** before any code was written.

### Implementation

- **`can_interfaces`**: added `msg/EncoderDataFL.msg`, `EncoderDataFR.msg`,
  `EncoderDataBL.msg`, `EncoderDataBR.msg` (one per wheel, per the
  comment's "4 DIFFERENT MESSAGES" instruction - ROS2 topics can only
  carry one message type each, same constraint the original module
  docstring already documented). Each carries the existing 4 fields
  (`explicit_mag/quad/imu_<suf>`, `drive_quad_<suf>`) plus
  `int32[2] ls_<suf>` and `int32[2] sensor_check_<suf>`. Field names keep
  the wheel suffix even though each message is now wheel-dedicated,
  deliberately matching the user's literal field list AND keeping
  `_get_field()`'s existing `<base>_<suffix>` candidate-matching logic
  working completely unchanged. Kept `MobilityData.msg` as-is (not
  deleted) since the existing test suite and conftest shim depend on it
  and nothing asked for its removal. Added all 4 new files to
  `CMakeLists.txt`'s `rosidl_generate_interfaces()` call.
- **`controllers/explicit_steer.py`**: added a `trust=(1, 1, 1)` parameter
  to `ExplicitController.update()`/`.step()` (mag, quad, imu). Excludes a
  channel by zeroing its row of `H` for that call - not by touching `R` -
  per the confirmed translation above.
- **`mobility_node.py`**:
  - `MSG_TYPES` now imports `EncoderDataFL/FR/BL/BR` (previously guessed,
    nonexistent `MobilityDataFL/FR/BL/BR` names) - **this is the actual
    fix**: these types now really exist, so `MSG_TYPES` is no longer
    all-`None` and the CAN subscription loop now actually subscribes all
    4 wheels (confirmed live, see below).
  - Default per-wheel topic names changed from `/can/mobility_data_<suf>`
    to `/can/encoder_data_<suf>` (`params.yaml` updated to match).
  - `can_receive()` now also extracts `ls_<suf>` and `sensor_check_<suf>`
    via the existing `_get_field()` (needed no changes itself - its
    generic `<base>_<suffix>` candidate logic already handles the new
    field names for free). Stores both into new per-wheel state
    (`_latest_limit_switch`, `_latest_sensor_check`, default `[1, 1]` for
    sensor_check so an old/not-yet-updated CAN bridge doesn't
    permanently distrust everything by omission).
  - New `_on_limit_switch(self, i)`: intentional no-op, called whenever
    `ls_<suf>[0] == 1`, reserved for future calibration use exactly as
    the user described.
  - `loop()` now computes `trust = (mag_ok, 1, imu_ok)` per wheel from
    `_latest_sensor_check[i]` and passes it into
    `self.steer_ctls[i].step(...)` every tick - quad has no health flag
    (not covered by "order is mag, imu") and is always trusted.
  - Replaced the raw instructional comment block with proper docstrings
    once implemented, including an expanded module-docstring section
    describing the new message shape and both new behaviors.

### Verification

- `colcon build --packages-select can_interfaces rover_mobility` -
  confirmed the 4 new message types really compile and are importable
  with the right field shapes (`int32`, `int32[2]`).
- Live-confirmed the actual fix: `MSG_TYPES` resolved to real
  `EncoderDataFL/FR/BL/BR` classes (not `None`) for the first time ever
  in this package's history.
- Hit the exact same **stale-install trap as the first review** again,
  mid-session: edited `can_receive()`/`loop()` further after an earlier
  `colcon build`, then couldn't figure out why a direct-repro script
  showed the new fields weren't being read - `diff`ing `install/` against
  `src/` confirmed the install was stale again. Rebuilt, confirmed
  byte-identical, moved on. (This is now the second time in this
  package's history that editing without rebuilding has caused confusing,
  misleading test/repro results - worth remembering for next time.)
- Caught a **real test bug of my own** while writing the new
  `can_receive()` tests: `WHEEL_ORDER = ['FR', 'BR', 'FL', 'BL']`, so
  index 0 is `'FR'`, not `'FL'` - my first draft of the new tests called
  `can_receive(node, 0, msg)` with an `EncoderDataFL`-shaped message,
  which made `can_receive()` look for `_fr`-suffixed fields that don't
  exist on it. Every assertion silently failed by reading stale defaults
  instead of raising an obvious error. Fixed by using
  `FL_INDEX = WHEEL_ORDER.index('FL')` (= 2) throughout instead of a
  hardcoded `0` - documented the whole false trail directly in the test
  class's docstring so it doesn't get rediscovered the hard way again.
- Added 7 new tests to `test_mobility_node_helpers.py`
  (`TestCanReceiveLimitSwitchAndSensorCheck`: limit-switch trigger/no-op
  behavior, sensor_check storage for all combinations, confirms only the
  targeted wheel's state changes, and a regression check that normal
  mag/quad/imu/drive_quad extraction still works against the new message
  type) and flipped the old `test_all_four_per_wheel_msg_types_fail_to_import`
  into `test_all_four_per_wheel_msg_types_now_import_successfully`
  (asserts the real classes now, not all-`None`).
- Added 5 new tests to `test_explicit_steer.py`
  (`TestExplicitControllerTrust`): default `trust` matches the old
  (pre-change) fully-trusted behavior exactly (regression safety); an
  untrusted channel fed garbage converges identically to a controller
  that never saw that garbage at all (proves exactly-zero influence, not
  just reduced influence); excluding a channel under normal (nonzero)
  `r_diag` does NOT raise `LinAlgError` (the specific failure mode a
  literal `R=0` would have caused); tracking still works from a single
  remaining trusted channel (quad alone).
- Full suite: **109/109 passing** (81 pre-existing + 12 zero-reference +
  7 new CAN-message tests + 5 new trust tests, fewer than 7+5=12 net new
  because 1 old test was transformed rather than added). New/touched test
  files (`test_mobility_node_helpers.py`, `test_explicit_steer.py`) are
  fully flake8- and pep257-clean (fixed a handful of mechanical
  docstring-convention and line-length issues along the way, including
  some pre-existing ones from the prior session that hadn't been
  re-checked since). Also fixed two trivial pre-existing lint nits
  (`W293` trailing whitespace, `W292` missing final newline) directly
  adjacent to today's edits in `mobility_node.py` while already there;
  left the larger pre-existing import-order/quote-style debt in that file
  untouched (same out-of-scope precedent as the first review).
- Did **not** re-attempt the full live harness session from the first
  review (`runtime/harness_node.py` etc.) - the `DriveCommand` bug
  (#1/#2) that blocked that harness partway through is still present and
  still out of scope today; today's verification was offline
  unit/construction-level, not a new live multi-tick session.
