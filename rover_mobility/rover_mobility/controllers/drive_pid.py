"""
Drive-wheel velocity controller: tick-delta feedback -> PID -> pwm fraction.
No Kalman filter - drive only needs rate, not an absolute angle estimate.

Plain class, no ROS awareness - mobility_node.py owns the ROS plumbing and
calls .step() on one instance of this per wheel, each tick.
"""


def signed_tick_delta(new, old, modulus):
    """Rollover-safe (new - old) for a free-running unsigned tick counter."""
    d = (new - old) % modulus
    if d > modulus / 2:
        d -= modulus
    return d


class DrivePID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


class DriveController:
    """Wraps quad-tick-delta velocity feedback + PID."""

    def __init__(self, dt, max_ticks_per_dt=50.0, tick_counter_bits=16,
                 pid_kp=1.0, pid_ki=0.0, pid_kd=0.0):
        self.dt = dt
        self.max_ticks_per_dt = max_ticks_per_dt  # ticks/dt at pwm=1.0 -- MEASURE ON HARDWARE
        self.tick_counter_mod = 1 << int(tick_counter_bits)

        self.pid = DrivePID(pid_kp, pid_ki, pid_kd)
        self._prev_quad = None
        self.measured_ticks_per_dt = 0.0

    def step(self, target_direction, target_pwm, quad):
        """
        target_direction: +1.0 / -1.0
        target_pwm: 0.0-1.0 (throttle magnitude)
        quad: latest raw quad tick count from CAN
        Returns pwm in [-1, 1], or None on the first call (no delta yet -
        deliberately not commanding motion off a fabricated zero delta).
        """
        if self._prev_quad is None:
            self._prev_quad = quad
            return None

        measured_ticks_per_dt = signed_tick_delta(quad, self._prev_quad, self.tick_counter_mod)
        self._prev_quad = quad
        self.measured_ticks_per_dt = measured_ticks_per_dt

        target_ticks_per_dt = target_direction * target_pwm * self.max_ticks_per_dt
        pid_out = self.pid.update(target_ticks_per_dt, measured_ticks_per_dt, self.dt)
        pwm = pid_out / self.max_ticks_per_dt
        return max(-1.0, min(1.0, pwm))
