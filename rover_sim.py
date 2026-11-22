#!/usr/bin/env python3
"""
rover_sim.py - full rover mobility simulation, no hardware: real joystick
input -> VroomVroom mixing -> 4x (steering EKF+PID / drive PID) -> 4x
simulated motor plants -> simulated CAN readback -> swerve forward
kinematics -> XY trajectory with a rover graphic, plus the same per-wheel
diagnostic plots as joy_can_sim.py (shown for one reference wheel).

Controller/plant/kinematics classes are DUPLICATED from
mobility_control/controllers/ and joy_can_sim.py for standalone use - see
those files' docstrings for the same caveat: keep in sync manually.

NEW ASSUMPTIONS beyond joy_can_sim.py (none of these exist in your real
code - all invented for this demo, flagged so they're not mistaken for
calibrated values):
  - WHEEL_RADIUS_M, TICKS_PER_REV: convert simulated tick-rate into a
    linear wheel speed (m/s). Arbitrary. The whole XY trajectory scale is
    illustrative only.
  - WHEEL_POS: physical (x, y) wheel positions in the chassis frame,
    assigned by what each label means (FR = +x/+y etc.) - this is a
    SEPARATE decision from WHEEL_ORDER's index-to-VroomVroom-output
    mapping (which trusts VroomVroom's docstring, per prior discussion).
    They don't have to agree with each other and, given the unresolved
    FR/BR/FL/BL conflict in mobility_node.py, may not.

WORLD-FRAME CONVENTION FIX (new): VroomVroom's angle output turned out to
need a +90 degree offset before it corresponds to this file's x=right,
y=forward world frame - confirmed by checking that "drive forward" should
produce +vy, not +vx, under idealized wheel tracking. This offset is
applied ONLY in the forward-kinematics/graphics code below (trajectory,
wheel-direction ticks) - it does NOT touch target_count, the PID, or the
EKF, which all work directly in VroomVroom's own angle convention and
never needed a "world frame" interpretation. This was purely a simulation
visualization bug, not a control-loop bug.

Requires: pygame, matplotlib, numpy
    pip install pygame matplotlib numpy --break-system-packages

Controls (same mapping as drive_controller.py / mobility_node.py):
    Left stick X    -> rotate (push left = turn left, verified via
                       kinematics, not just assumed)
    L2/R2 triggers  -> throttle (R2 forward, L2 reverse)
    Button 9 (L3)   -> hold for crab mode
"""
import argparse
import math
import sys
import time
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation

try:
    import pygame
except ImportError:
    print("This script needs pygame: pip install pygame --break-system-packages")
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────
# Controller classes - DUPLICATED from mobility_control/controllers/.
# Keep in sync manually.
# ─────────────────────────────────────────────────────────────────────────

COUNTS_PER_REV = 256
H = np.array([[1, 0], [1, 0], [0, 1]], dtype=float)
RAD_TO_COUNT2 = (COUNTS_PER_REV / (2 * np.pi)) ** 2


def deg_to_count(deg):
    return (deg % 360.0) * COUNTS_PER_REV / 360.0


def count_to_deg(count):
    return (count % COUNTS_PER_REV) * 360.0 / COUNTS_PER_REV


def count_to_signed_deg(count):
    d = count_to_deg(count)
    if d > 180:
        d -= 360
    return d


def wrap_count(c, period=COUNTS_PER_REV):
    return c % period


def wrap_count_diff(a, b, period=COUNTS_PER_REV):
    d = (a - b) % period
    if d > period / 2:
        d -= period
    return d


def signed_tick_delta(new, old, modulus):
    d = (new - old) % modulus
    if d > modulus / 2:
        d -= modulus
    return d


class SteerPID:
    def __init__(self, kp, ki, kd, period=COUNTS_PER_REV):
        self.kp, self.ki, self.kd, self.period = kp, ki, kd, period
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, target, current, dt):
        error = wrap_count_diff(target, current, self.period)
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


class ExplicitController:
    def __init__(self, dt, t_motor=0.15, k_motor=0.8,
                 q_diag=(0.001, 0.01), r_diag=(0.05, 0.02, 0.01),
                 pid_kp=1.0, pid_ki=0.0, pid_kd=0.0):
        self.dt = dt
        self.t_motor = t_motor
        self.k_motor = k_motor
        self.Q = np.diag(q_diag) * RAD_TO_COUNT2
        self.R = np.diag(r_diag) * RAD_TO_COUNT2
        self.F = np.array([[1, dt], [0, 1 - dt / t_motor]], dtype=float)
        self.x = np.zeros(2)
        self.P = np.eye(2) * 1.0
        self.pid = SteerPID(pid_kp, pid_ki, pid_kd)

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        self.x[0] = wrap_count(self.x[0])

    def update(self, z):
        pred = H @ self.x
        y = np.array([
            wrap_count_diff(z[0], pred[0]),
            wrap_count_diff(z[1], pred[1]),
            z[2] - pred[2],
        ])
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.x[0] = wrap_count(self.x[0])
        self.P = (np.eye(2) - K @ H) @ self.P

    def step(self, target_count, z=None):
        self.predict()
        if z is not None:
            self.update(z)
        pwm = self.pid.update(target_count, self.x[0], self.dt)
        return max(-1.0, min(1.0, pwm)), self.x.copy()


class DrivePID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


class DriveController:
    def __init__(self, dt, max_ticks_per_dt=50.0, tick_counter_bits=16,
                 pid_kp=1.0, pid_ki=0.0, pid_kd=0.0):
        self.dt = dt
        self.max_ticks_per_dt = max_ticks_per_dt
        self.tick_counter_mod = 1 << int(tick_counter_bits)
        self.pid = DrivePID(pid_kp, pid_ki, pid_kd)
        self._prev_quad = None
        self.measured_ticks_per_dt = 0.0

    def step(self, target_direction, target_pwm, quad):
        if self._prev_quad is None:
            self._prev_quad = quad
            return None
        d = signed_tick_delta(quad, self._prev_quad, self.tick_counter_mod)
        self._prev_quad = quad
        self.measured_ticks_per_dt = d
        target_ticks_per_dt = target_direction * target_pwm * self.max_ticks_per_dt
        pid_out = self.pid.update(target_ticks_per_dt, d, self.dt)
        return max(-1.0, min(1.0, pid_out / self.max_ticks_per_dt))


class VroomVroom:
    def __init__(self, half_width=0.35, half_length=0.45, speed_scalar=250, r_scalar=1, deadzone=0.0):
        self.a, self.b = half_width, half_length
        self.speed_scalar, self.r_scalar, self.deadzone = speed_scalar, r_scalar, deadzone

    def magnitude(self, v):
        return (v[0] ** 2 + v[1] ** 2) ** 0.5

    def angle(self, v):
        return math.atan2(v[1], v[0])

    def smooooth_operatorrrr(self, throttle, rotate, crab):
        if abs(throttle) <= self.deadzone: throttle = 0
        if abs(rotate) <= self.deadzone: rotate = 0
        if abs(crab) <= self.deadzone: crab = 0
        flipper = False
        rinv = math.tan(rotate * (math.pi / 2 - 0.01))
        R = 10 ** 5 if rinv == 0 else self.r_scalar / rinv
        if R < 0:
            flipper = not flipper
        theta = -crab * math.pi / 2
        if theta > 0:
            flipper = not flipper
            theta -= math.pi
        R_vec = [R * math.cos(theta), R * math.sin(theta)]
        angles, vels = self.from_R_vec(R_vec, flipper)
        max_vel = max(vels)
        if max_vel > 0:
            for i in range(len(vels)):
                vels[i] *= self.speed_scalar * throttle / max_vel
        return [angles, vels]

    def from_R_vec(self, R_vec, flipper):
        angles = [0.0] * 4
        vels = [0.0] * 4
        w1 = [self.a - R_vec[0], self.b - R_vec[1]]
        w2 = [self.a - R_vec[0], -self.b - R_vec[1]]
        w3 = [-self.a - R_vec[0], self.b - R_vec[1]]
        w4 = [-self.a - R_vec[0], -self.b - R_vec[1]]
        for i, w in enumerate([w1, w2, w3, w4]):
            angles[i] = self.angle(w) - math.pi
            vels[i] = self.magnitude(w)
        if flipper:
            for i in range(4):
                angles[i] += math.pi
        for i in range(4):
            angles[i] *= 180 / math.pi
            # NOTE: reverted to (-180, 180] to match mobility_control's
            # canonical vroomvroom.py - the (0, 360) wrap tried here
            # earlier was numerically harmless (deg_to_count() takes mod
            # 360 regardless of representation) but an unnecessary
            # divergence from the file this is duplicated from.
            while angles[i] > 180: angles[i] -= 360
            while angles[i] < -180: angles[i] += 360
        return [angles, vels]


# ─────────────────────────────────────────────────────────────────────────
# Simulated plants - invented for this script, do not exist in real code.
# ─────────────────────────────────────────────────────────────────────────

class SteerPlant:
    def __init__(self, dt, tau=0.18, max_omega_cps=150.0,
                 mag_noise=1.0, quad_noise=1.5, imu_noise=2.0):
        self.dt = dt
        self.tau = tau
        self.max_omega_cps = max_omega_cps
        self.theta = 0.0
        self.omega = 0.0
        self.mag_noise = mag_noise
        self.quad_noise = quad_noise
        self.imu_noise = imu_noise

    def step(self, pwm):
        target_omega = pwm * self.max_omega_cps
        self.omega += self.dt / self.tau * (target_omega - self.omega)
        self.theta = wrap_count(self.theta + self.omega * self.dt)
        return self.theta, self.omega

    def sense(self):
        mag = wrap_count(self.theta + np.random.normal(0, self.mag_noise))
        quad = wrap_count(self.theta + np.random.normal(0, self.quad_noise))
        imu = self.omega * self.dt + np.random.normal(0, self.imu_noise)
        return np.array([mag, quad, imu])


class DrivePlant:
    def __init__(self, dt, tau=0.12, max_ticks_per_dt=45.0, tick_counter_bits=16, tick_noise=0.5):
        self.dt = dt
        self.tau = tau
        self.max_ticks_per_dt = max_ticks_per_dt
        self.tick_counter_mod = 1 << tick_counter_bits
        self.tick_noise = tick_noise
        self.rate = 0.0
        self.ticks = 0.0

    def step(self, pwm):
        target_rate = pwm * self.max_ticks_per_dt
        self.rate += self.dt / self.tau * (target_rate - self.rate)
        self.ticks = (self.ticks + self.rate) % self.tick_counter_mod
        return self.rate

    def sense(self):
        noisy = self.ticks + np.random.normal(0, self.tick_noise)
        return int(noisy) % self.tick_counter_mod


# ─────────────────────────────────────────────────────────────────────────
# Wheel layout. Two SEPARATE decisions, see module docstring.
# ─────────────────────────────────────────────────────────────────────────

# Index-order used to read VroomVroom's smooooth_operatorrrr() output
# arrays. FIXED (see analysis below) - this was previously ['FR','FL',
# 'BR','BL'], which mislabeled two wheels.
#
# ROOT CAUSE of the non-crab "crazy wheels" / front-back-swap-between-
# left-and-right symptom: VroomVroom's w1..w4 have a FIXED geometric
# pattern - w1=(+a,+b), w2=(+a,-b), w3=(-a,+b), w4=(-a,-b), i.e.
# RIGHT+FRONT, RIGHT+BACK, LEFT+FRONT, LEFT+BACK (with a=half_width=x,
# b=half_length=y, standard x=right/y=forward convention). The label
# order must match that fixed pattern: RIGHT+BACK is unambiguously "BR",
# not "FL". Verified directly from the raw w-vectors (not just angle
# output) and by a full-range continuity sweep (zero discontinuities
# with this order, vs the previous order which produced a genuine
# front/back role swap between left and right turns of equal magnitude).
# This also resolves the FR/BR/FL/BL ordering conflict flagged
# repeatedly earlier in this project - VroomVroom's own docstring
# claiming "FR, BL, FL, BR" turns out to be the wrong one; a different,
# now-superseded comment claiming "FR, BR, FL, BL" was actually correct.
WHEEL_ORDER = ['FR', 'BR', 'FL', 'BL']

# Physical (x, y) position of each wheel in the chassis frame (x = right,
# y = forward), assigned by what the label means - independent of the
# index-order decision above, and NOT re-derived from VroomVroom's internal
# w1..w4 formula (that derivation is exactly the part that's ambiguous).
HALF_WIDTH = 0.35
HALF_LENGTH = 0.45
WHEEL_POS = {
    'FR': (HALF_WIDTH, HALF_LENGTH),
    'FL': (-HALF_WIDTH, HALF_LENGTH),
    'BR': (HALF_WIDTH, -HALF_LENGTH),
    'BL': (-HALF_WIDTH, -HALF_LENGTH),
}

# Invented conversion from simulated tick-rate to real linear speed - not
# calibrated to anything, purely to make the trajectory plot move at a
# visually reasonable rate.
WHEEL_RADIUS_M = 0.075
TICKS_PER_REV = 64.0

# Mirrors mobility_node.py's drive_alignment_max_error_deg - drive power
# scales down while a wheel is still turning toward its target angle,
# instead of driving at full commanded speed while badly misaligned.
DRIVE_ALIGNMENT_MAX_ERROR_DEG = 30.0

# Offset applied ONLY when converting VroomVroom's angle into this file's
# world frame (trajectory kinematics, wheel-direction graphic) - see
# module docstring. Confirmed empirically: without it, "drive forward"
# produces sideways motion in the trajectory math.
WORLD_FRAME_ANGLE_OFFSET_DEG = 90.0


def solve_body_velocity(wheel_vel_vectors, positions):
    """Least-squares swerve forward kinematics: wheel velocity vectors (in
    chassis frame) + wheel positions -> body (vx, vy, omega). Verified
    against hand-derived pure-translation / pure-spin / combined cases."""
    rows, rhs = [], []
    for (vx_i, vy_i), (x_i, y_i) in zip(wheel_vel_vectors, positions):
        rows.append([1, 0, -y_i])
        rhs.append(vx_i)
        rows.append([0, 1, x_i])
        rhs.append(vy_i)
    sol, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
    return sol  # vx_body, vy_body, omega


# ─────────────────────────────────────────────────────────────────────────
# Joystick, same mapping as drive_controller.py / mobility_node.py
# ─────────────────────────────────────────────────────────────────────────

class JoystickReader:
    def __init__(self, index=0):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("No joystick detected. Plug one in and retry.")
        self.js = pygame.joystick.Joystick(index)
        self.js.init()
        self.crabby = False
        self.joy_x = 0.0
        self.joy_y = 0.0
        self.joy_x_acc = 0.5
        self.joy_y_acc = 2.0
        self.joy_t = time.perf_counter()
        print(f"Joystick connected: {self.js.get_name()}")

    def read(self):
        pygame.event.pump()
        try:
            L3 = self.js.get_button(9)
        except pygame.error:
            L3 = 0
        # hold-to-crab (not toggle) - kept as-is per report that this
        # works well, unlike mobility_node.py's toggle-based crab
        self.crabby = (L3 == 1)

        def axis(i, default=0.0):
            try:
                return self.js.get_axis(i)
            except pygame.error:
                return default

        # rotate sign verified via kinematics (see module docstring):
        # axis(0) directly, no negation - push left (axis=-1) -> negative
        # rotate -> confirmed LEFT turn.
        turning = axis(0)
        # LT/RT trigger axes. Standard SDL/XInput convention: rests at -1,
        # full press at +1 -> (axis+1)/2 gives 0 at rest, 1 fully pressed.
        # VERIFY empirically (print axes[2]/axes[5] while pressing) - this
        # varies by OS/driver.
        lt_val = (axis(2) + 1) / 2
        rt_val = (axis(5) + 1) / 2
        throttle = rt_val - lt_val

        now = time.perf_counter()
        max_dx = self.joy_x_acc * (now - self.joy_t)
        max_dy = self.joy_y_acc * (now - self.joy_t)
        dx = max(-max_dx, min(max_dx, turning - self.joy_x))
        dy = max(-max_dy, min(max_dy, throttle - self.joy_y))
        self.joy_x += dx
        self.joy_y += dy
        self.joy_t = now
        return self.joy_x, self.joy_y, self.crabby


# ─────────────────────────────────────────────────────────────────────────
# Main sim loop + live plot
# ─────────────────────────────────────────────────────────────────────────

REF_WHEEL = 'FL'   # which wheel the detail plots (top-left 4 panels) show


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--joystick-index', type=int, default=0)
    parser.add_argument('--dt', type=float, default=0.02)
    parser.add_argument('--window-s', type=float, default=8.0)
    parser.add_argument('--trail-points', type=int, default=3000)
    args = parser.parse_args()

    joy = JoystickReader(args.joystick_index)
    vroom = VroomVroom(half_width=HALF_WIDTH, half_length=HALF_LENGTH)

    # Steering gains retuned: kp=1.0, kd=0.15 gives zero overshoot, zero
    # tail oscillation, settling in ~40 ticks (0.8s) in a sweep of the
    # actual sim plant - was pid_kd=0.0 (no damping), which produced the
    # bang-bang/overshoot-then-correct oscillation.
    steer_ctls = {w: ExplicitController(dt=args.dt, t_motor=0.15, pid_kp=1.0, pid_ki=0.0, pid_kd=0.15)
                  for w in WHEEL_ORDER}
    drive_ctls = {w: DriveController(dt=args.dt, max_ticks_per_dt=50.0, pid_kp=1.0, pid_ki=2.0, pid_kd=0.0)
                  for w in WHEEL_ORDER}
    steer_plants = {w: SteerPlant(dt=args.dt, tau=0.18, max_omega_cps=150.0) for w in WHEEL_ORDER}
    drive_plants = {w: DrivePlant(dt=args.dt, tau=0.12, max_ticks_per_dt=45.0) for w in WHEEL_ORDER}

    positions = [WHEEL_POS[w] for w in WHEEL_ORDER]

    # body pose (world frame): x, y in meters, heading in radians
    body = {'x': 0.0, 'y': 0.0, 'heading': 0.0}

    n = int(args.window_s / args.dt)
    t_hist = deque(maxlen=n)
    steer_target_hist = deque(maxlen=n)
    steer_est_hist = deque(maxlen=n)
    steer_true_hist = deque(maxlen=n)
    steer_pwm_hist = deque(maxlen=n)
    drive_target_hist = deque(maxlen=n)
    drive_meas_hist = deque(maxlen=n)
    drive_pwm_hist = deque(maxlen=n)

    trail_x = deque(maxlen=args.trail_points)
    trail_y = deque(maxlen=args.trail_points)

    t0 = time.perf_counter()

    fig = plt.figure(figsize=(14, 8))
    fig.suptitle('Full rover mobility simulation (no hardware)')
    gs = gridspec.GridSpec(2, 3, width_ratios=[1, 1, 1.3])

    ax_sa = fig.add_subplot(gs[0, 0])
    ax_sp = fig.add_subplot(gs[0, 1])
    ax_dr = fig.add_subplot(gs[1, 0])
    ax_dp = fig.add_subplot(gs[1, 1])
    ax_xy = fig.add_subplot(gs[:, 2])

    (l_target,) = ax_sa.plot([], [], label='target', color='tab:orange')
    (l_est,) = ax_sa.plot([], [], label='EKF estimate', color='tab:blue')
    (l_true,) = ax_sa.plot([], [], label='true (sim plant)', color='tab:green', linestyle='--')
    ax_sa.set_title(f'[{REF_WHEEL}] Steering angle (deg)')
    ax_sa.set_ylim(-190, 190)
    ax_sa.legend(loc='upper right', fontsize=8)

    (l_spwm,) = ax_sp.plot([], [], color='tab:red')
    ax_sp.set_title(f'[{REF_WHEEL}] Steering pwm')
    ax_sp.set_ylim(-1.1, 1.1)

    (l_dtarget,) = ax_dr.plot([], [], label='target', color='tab:orange')
    (l_dmeas,) = ax_dr.plot([], [], label='measured (sim CAN)', color='tab:blue')
    ax_dr.set_title(f'[{REF_WHEEL}] Drive rate (ticks/dt)')
    ax_dr.legend(loc='upper right', fontsize=8)

    (l_dpwm,) = ax_dp.plot([], [], color='tab:red')
    ax_dp.set_title(f'[{REF_WHEEL}] Drive pwm')
    ax_dp.set_ylim(-1.1, 1.1)

    for ax in (ax_sa, ax_sp, ax_dr, ax_dp):
        ax.set_xlabel('t (s)')
        ax.grid(alpha=0.3)

    ax_xy.set_title('Rover trajectory (XY, world frame, meters)')
    ax_xy.set_aspect('equal')
    ax_xy.grid(alpha=0.3)
    (trail_line,) = ax_xy.plot([], [], color='tab:blue', alpha=0.6, linewidth=1)
    chassis_patch = Polygon([[0, 0]] * 4, closed=True, facecolor='0.8', edgecolor='k')
    ax_xy.add_patch(chassis_patch)
    wheel_lines = {w: ax_xy.plot([], [], color='tab:red', linewidth=2)[0] for w in WHEEL_ORDER}
    readout_text = ax_xy.text(
        0.02, 0.98, '', transform=ax_xy.transAxes, va='top', ha='left',
        fontsize=8, family='monospace',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='0.7')
    )

    bounds = {'xmin': -1.0, 'xmax': 1.0, 'ymin': -1.0, 'ymax': 1.0}

    def expand_bounds(x, y, margin=0.5):
        changed = False
        if x - margin < bounds['xmin']:
            bounds['xmin'] = x - margin; changed = True
        if x + margin > bounds['xmax']:
            bounds['xmax'] = x + margin; changed = True
        if y - margin < bounds['ymin']:
            bounds['ymin'] = y - margin; changed = True
        if y + margin > bounds['ymax']:
            bounds['ymax'] = y + margin; changed = True
        if changed:
            ax_xy.set_xlim(bounds['xmin'], bounds['xmax'])
            ax_xy.set_ylim(bounds['ymin'], bounds['ymax'])

    def update(_frame):
        joy_x, joy_y, crabby = joy.read()
        if crabby:
            angles_deg, vels = vroom.smooooth_operatorrrr(joy_y, 0, joy_x)
        else:
            angles_deg, vels = vroom.smooooth_operatorrrr(joy_y, joy_x, 0)

        speed_scalar = vroom.speed_scalar or 1.0
        wheel_vel_vectors = []
        per_wheel_readout = []
        ref_data = {}

        for i, w in enumerate(WHEEL_ORDER):
            angle_deg = angles_deg[i]
            vel = vels[i]
            target_count = deg_to_count(angle_deg)
            drive_frac = max(-1.0, min(1.0, vel / speed_scalar))
            target_direction = 1.0 if drive_frac >= 0 else -1.0
            target_pwm = abs(drive_frac)

            z = steer_plants[w].sense()
            steer_pwm, steer_state = steer_ctls[w].step(target_count, z)
            steer_plants[w].step(steer_pwm)

            align_error_deg = abs(wrap_count_diff(target_count, steer_state[0])) * 360.0 / COUNTS_PER_REV
            align_scale = max(0.0, 1.0 - align_error_deg / DRIVE_ALIGNMENT_MAX_ERROR_DEG)
            target_pwm_gated = target_pwm * align_scale

            quad = drive_plants[w].sense()
            drive_pwm = drive_ctls[w].step(target_direction, target_pwm_gated, quad)
            drive_plants[w].step(drive_pwm if drive_pwm is not None else 0.0)

            # forward kinematics input: this wheel's ACTUAL (simulated true)
            # angle and ACTUAL linear speed, not the commanded target - the
            # body should move according to what the plant really did.
            # +WORLD_FRAME_ANGLE_OFFSET_DEG converts VroomVroom's angle
            # convention into this file's world frame - see module docstring.
            true_angle_rad = math.radians(
                count_to_signed_deg(steer_plants[w].theta) + WORLD_FRAME_ANGLE_OFFSET_DEG
            )
            linear_speed_mps = (drive_plants[w].rate / TICKS_PER_REV) * (2 * math.pi * WHEEL_RADIUS_M) / args.dt
            wheel_vel_vectors.append((linear_speed_mps * math.cos(true_angle_rad),
                                       linear_speed_mps * math.sin(true_angle_rad)))

            per_wheel_readout.append(
                f"{w:2s} tgt={angle_deg:+6.1f} est={count_to_signed_deg(steer_state[0]):+6.1f} "
                f"spwm={steer_pwm:+.2f} drate={drive_ctls[w].measured_ticks_per_dt:+5.1f} "
                f"dpwm={(drive_pwm or 0.0):+.2f}"
            )

            if w == REF_WHEEL:
                ref_data = dict(target_count=target_count, steer_state=steer_state,
                                 steer_true=steer_plants[w].theta, steer_pwm=steer_pwm,
                                 target_direction=target_direction, target_pwm=target_pwm,
                                 drive_ctl=drive_ctls[w], drive_pwm=drive_pwm)

        vx_body, vy_body, omega = solve_body_velocity(wheel_vel_vectors, positions)

        psi = body['heading']
        wx = vx_body * math.cos(psi) - vy_body * math.sin(psi)
        wy = vx_body * math.sin(psi) + vy_body * math.cos(psi)
        body['x'] += wx * args.dt
        body['y'] += wy * args.dt
        body['heading'] = (psi + omega * args.dt) % (2 * math.pi)

        trail_x.append(body['x'])
        trail_y.append(body['y'])
        expand_bounds(body['x'], body['y'])

        # --- reference wheel detail plots ---
        t = time.perf_counter() - t0
        t_hist.append(t)
        steer_target_hist.append(count_to_signed_deg(ref_data['target_count']))
        steer_est_hist.append(count_to_signed_deg(ref_data['steer_state'][0]))
        steer_true_hist.append(count_to_signed_deg(ref_data['steer_true']))
        steer_pwm_hist.append(ref_data['steer_pwm'])
        drive_target_hist.append(ref_data['target_direction'] * ref_data['target_pwm']
                                  * ref_data['drive_ctl'].max_ticks_per_dt)
        drive_meas_hist.append(ref_data['drive_ctl'].measured_ticks_per_dt)
        drive_pwm_hist.append(ref_data['drive_pwm'] if ref_data['drive_pwm'] is not None else 0.0)

        l_target.set_data(t_hist, steer_target_hist)
        l_est.set_data(t_hist, steer_est_hist)
        l_true.set_data(t_hist, steer_true_hist)
        l_spwm.set_data(t_hist, steer_pwm_hist)
        l_dtarget.set_data(t_hist, drive_target_hist)
        l_dmeas.set_data(t_hist, drive_meas_hist)
        l_dpwm.set_data(t_hist, drive_pwm_hist)
        if len(t_hist) > 1:
            for ax in (ax_sa, ax_sp, ax_dr, ax_dp):
                ax.set_xlim(t_hist[0], t_hist[-1])
            ax_dr.relim()
            ax_dr.autoscale_view(scalex=False)

        # --- trajectory + rover graphic ---
        trail_line.set_data(trail_x, trail_y)

        corners_local = np.array([
            [HALF_WIDTH, HALF_LENGTH], [-HALF_WIDTH, HALF_LENGTH],
            [-HALF_WIDTH, -HALF_LENGTH], [HALF_WIDTH, -HALF_LENGTH],
        ])
        c, s = math.cos(body['heading']), math.sin(body['heading'])
        R = np.array([[c, -s], [s, c]])
        corners_world = (R @ corners_local.T).T + np.array([body['x'], body['y']])
        chassis_patch.set_xy(corners_world)

        for w in WHEEL_ORDER:
            wx_local, wy_local = WHEEL_POS[w]
            wheel_world = R @ np.array([wx_local, wy_local]) + np.array([body['x'], body['y']])
            # same world-frame offset as the kinematics above, for visual
            # consistency (wheel ticks should point where the wheel is
            # actually pushing, matching the trajectory direction)
            wheel_angle_world = (body['heading']
                                  + math.radians(count_to_signed_deg(steer_plants[w].theta)
                                                  + WORLD_FRAME_ANGLE_OFFSET_DEG))
            tip = wheel_world + 0.15 * np.array([math.cos(wheel_angle_world), math.sin(wheel_angle_world)])
            wheel_lines[w].set_data([wheel_world[0], tip[0]], [wheel_world[1], tip[1]])

        readout_text.set_text(
            f"x={body['x']:+6.2f}m y={body['y']:+6.2f}m "
            f"heading={math.degrees(body['heading']):+6.1f}deg\n"
            f"vx={vx_body:+5.2f} vy={vy_body:+5.2f} omega={omega:+5.2f} rad/s\n"
            + "\n".join(per_wheel_readout)
        )

        return (l_target, l_est, l_true, l_spwm, l_dtarget, l_dmeas, l_dpwm,
                trail_line, chassis_patch, readout_text, *wheel_lines.values())

    ani = FuncAnimation(fig, update, interval=args.dt * 1000, blit=False)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()