"""
Steering controller for one wheel: EKF over [theta_count, omega_count] fused
from (mag, quad, imu), driving a wrap-aware PID to a target angle.

Plain class, no ROS awareness - mobility_node.py owns the ROS plumbing and
calls .step() on one instance of this per wheel, each tick.
"""
import numpy as np

COUNTS_PER_REV = 256  # 8-bit angle: 0-255 counts = 0-360 degrees

# H maps the STATE [theta_count, omega_count] to MEASUREMENTS [mag, quad, imu].
# Fixed by which physical sensor measures what.
H = np.array([
    [1, 0],
    [1, 0],
    [0, 1],
], dtype=float)

RAD_TO_COUNT2 = (COUNTS_PER_REV / (2 * np.pi)) ** 2


def deg_to_count(deg):
    return (deg % 360.0) * COUNTS_PER_REV / 360.0


def count_to_deg(count):
    return (count % COUNTS_PER_REV) * 360.0 / COUNTS_PER_REV


def wrap_count(c, period=COUNTS_PER_REV):
    return c % period


def wrap_count_diff(a, b, period=COUNTS_PER_REV):
    """Shortest signed difference (a - b) on a circular count domain."""
    d = (a - b) % period
    if d > period / 2:
        d -= period
    return d


class SteerPID:
    def __init__(self, kp, ki, kd, period=COUNTS_PER_REV):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.period = period
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, target, current, dt):
        error = wrap_count_diff(target, current, self.period)
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


class ExplicitController:
    """EKF-fused steering angle estimate + PID, in 8-bit count-space throughout."""

    def __init__(self, dt, t_motor=0.15, k_motor=0.8,
                 q_diag=(0.001, 0.01), r_diag=(0.05, 0.02, 0.01),
                 pid_kp=1.0, pid_ki=0.0, pid_kd=0.0):
        self.dt = dt
        self.t_motor = t_motor
        self.k_motor = k_motor  # unused in F, carried over as-is

        self.Q = np.diag(q_diag) * RAD_TO_COUNT2
        self.R = np.diag(r_diag) * RAD_TO_COUNT2
        self.F = np.array([
            [1, dt],
            [0, 1 - dt / t_motor],
        ], dtype=float)

        self.x = np.zeros(2)   # [theta_count, omega_count]
        self.P = np.eye(2) * 1.0

        self.pid = SteerPID(pid_kp, pid_ki, pid_kd)

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        self.x[0] = wrap_count(self.x[0])

    def update(self, z, trust=(1, 1, 1)):
        """z = [mag_count, quad_count, imu]

        trust: per-channel (mag, quad, imu) trust flags, 1 (use this
        measurement) or 0 (sensor reported down - exclude it from this
        update). Excluding a channel is done by zeroing its ROW of H for
        this call, NOT by zeroing its R entry: a zero R means "infinitely
        trust this measurement" (the opposite of what we want) and, since
        H's mag/quad rows are identical, a literal R=0 can make S singular
        and raise LinAlgError. Zeroing H's row instead makes that row of S
        reduce to just R[i,i] (still positive, still invertible) and makes
        the corresponding column of the Kalman gain exactly zero, so the
        untrusted measurement provably has no effect on the state update
        regardless of its value.
        """
        trust_col = np.array(trust, dtype=float).reshape(-1, 1)
        H_eff = H * trust_col

        pred = H_eff @ self.x
        y = np.array([
            wrap_count_diff(z[0], pred[0]),
            wrap_count_diff(z[1], pred[1]),
            z[2] - pred[2],
        ])
        S = H_eff @ self.P @ H_eff.T + self.R
        K = self.P @ H_eff.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.x[0] = wrap_count(self.x[0])
        self.P = (np.eye(2) - K @ H_eff) @ self.P

    def step(self, target_count, z=None, trust=(1, 1, 1)):
        """
        Call once per tick.
        target_count: desired steering angle, 0-255 counts.
        z: latest [mag_count, quad_count, imu] reading, or None if no new
           CAN packet arrived this tick (predict-only).
        trust: per-channel (mag, quad, imu) trust flags - see update().
        Returns (pwm in [-1, 1], current [theta_count, omega_count] estimate).
        """
        self.predict()
        if z is not None:
            self.update(z, trust)

        pwm = self.pid.update(target_count, self.x[0], self.dt)
        pwm = max(-1.0, min(1.0, pwm))
        return pwm, self.x.copy()
