"""
pid_tuning_core.py

The PID auto-tuning algorithm (RLS system-ID + pole-placement gain
computation + threshold-gated auto-apply + step/chirp/PRBS experiment
injection), extracted out of tune_pid.py so it has ZERO ROS dependency.

Why this file exists: tune_pid.py's PidTunerNode (a rclpy.Node subclass)
used to define these classes inline, which meant anything that wanted to
reuse the exact tuning algorithm - e.g. a standalone, no-ROS joystick
simulation - had to either duplicate this code (drifts out of sync, see
rover_sim.py/joy_can_sim.py's own docstrings for exactly that complaint
about the controller classes) or drag in rclpy + a built all_interfaces
package just to do math. Splitting the algorithm out here means
tune_pid.py's PidTunerNode and any other consumer both import the SAME
code - there is only one implementation of this algorithm, not two kept
in sync by hand.

Classes, in the order data flows through them:
    RLSEstimator        - online 2nd-order ARX system identification
    PolePlacementPID     - plant params -> PID gains via pole placement
    GainChangeMonitor    - gates large gain jumps for manual review
    ExperimentManager    - step/chirp/PRBS test-signal injection + batch RLS
    WheelTuner           - bundles one of each PER LOOP (pos, vel) for one
                            wheel, with the exact per-wheel orchestration
                            tune_pid.py's PidTunerNode used to run inline
                            in its ROS callbacks (_telemetry_cb,
                            _run_experiment_cb, _set_gains_cb, _set_rls_cb)
                            - unchanged logic, just callable directly.
"""
import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# RLS Estimator (unchanged from the original tune_pid.py)
# ─────────────────────────────────────────────────────────────────────────────

class RLSEstimator:
    """
    Recursive Least Squares estimator for a 2nd-order ARX model:
        y(k) = a1*y(k-1) + a2*y(k-2) + b1*u(k-1) + b2*u(k-2)
    """

    def __init__(self, lam: float = 0.97, P_init: float = 1000.0):
        self.lam = lam
        self.n = 4
        self.theta = np.array([0.9, 0.0, 0.1, 0.0], dtype=float)
        self.P = np.eye(self.n) * P_init
        self.y_buf = [0.0, 0.0]
        self.u_buf = [0.0, 0.0]
        self.last_innovation = 0.0
        self.last_phi = np.zeros(self.n)

    def update(self, y_new: float, u_new: float) -> np.ndarray:
        phi = np.array([self.y_buf[1], self.y_buf[0], self.u_buf[1], self.u_buf[0]])
        self.last_phi = phi

        y_pred = phi @ self.theta
        e = y_new - y_pred
        self.last_innovation = e

        P_phi = self.P @ phi
        denom = self.lam + phi @ P_phi
        if abs(denom) < 1e-10:
            denom = 1e-10
        L = P_phi / denom

        self.theta = self.theta + L * e

        I_Lphi = np.eye(self.n) - np.outer(L, phi)
        self.P = (1.0 / self.lam) * (I_Lphi @ self.P @ I_Lphi.T + 1e-6 * np.eye(self.n))

        self.y_buf[0] = self.y_buf[1]
        self.y_buf[1] = y_new
        self.u_buf[0] = self.u_buf[1]
        self.u_buf[1] = u_new

        return self.theta.copy()

    def get_plant_params(self) -> dict:
        a1, a2, b1, b2 = self.theta
        denom = 1.0 - a1 - a2
        if abs(denom) < 1e-6:
            denom = 1e-6
        K = (b1 + b2) / denom
        roots = np.roots([1.0, -a1, -a2])
        dominant_pole = roots[np.argmax(np.abs(roots))]
        pole_mag = np.abs(dominant_pole)
        return {'K': float(K), 'pole_mag': float(pole_mag),
                'dominant_pole': dominant_pole, 'theta': self.theta.copy()}

    def reset_covariance(self, P_init: float = 1000.0):
        self.P = np.eye(self.n) * P_init

    def set_lambda(self, lam: float):
        self.lam = max(0.8, min(1.0, lam))


# ─────────────────────────────────────────────────────────────────────────────
# Pole Placement PID Computation (unchanged from the original tune_pid.py)
# ─────────────────────────────────────────────────────────────────────────────

class PolePlacementPID:
    def __init__(self, Ts: float, T_settle: float, zeta: float = 0.7):
        self.Ts = Ts
        self.T_settle = T_settle
        self.zeta = zeta
        wn = 4.0 / (zeta * T_settle)
        self.p_d = np.exp(-zeta * wn * Ts)

    def compute_gains(self, K: float, pole_mag: float) -> dict:
        p = np.clip(pole_mag, 0.01, 0.9999)
        pd = self.p_d
        if abs(K) < 1e-6:
            K = 1e-6
        Kp = (pd - p) / (K * (1.0 - p))
        Ki = Kp * (1.0 - pd) / self.Ts
        Kd = Kp * self.Ts / (1.0 + pd)
        Kp = float(np.clip(Kp, 0.1, 100.0))
        Ki = float(np.clip(Ki, 0.0, 50.0))
        Kd = float(np.clip(Kd, 0.0, 10.0))
        return {'Kp': Kp, 'Ki': Ki, 'Kd': Kd, 'p_d': float(pd)}

    def update_settle_time(self, T_settle: float):
        self.T_settle = T_settle
        wn = 4.0 / (self.zeta * T_settle)
        self.p_d = np.exp(-self.zeta * wn * self.Ts)


# ─────────────────────────────────────────────────────────────────────────────
# Threshold Logic (unchanged from the original tune_pid.py)
# ─────────────────────────────────────────────────────────────────────────────

class GainChangeMonitor:
    def __init__(self, Kp_thresh=3.0, Ki_thresh=1.0, Kd_thresh=1.0,
                 min_updates_before_change=20):
        self.thresholds = {'Kp': Kp_thresh, 'Ki': Ki_thresh, 'Kd': Kd_thresh}
        self.min_updates = min_updates_before_change
        self.update_count = 0

    def check(self, current: dict, proposed: dict) -> dict:
        self.update_count += 1
        if self.update_count < self.min_updates:
            return {'apply': False, 'needs_manual': False, 'deltas': {},
                    'reason': f'warming up ({self.update_count}/{self.min_updates})'}
        deltas = {k: abs(proposed[k] - current[k]) for k in ('Kp', 'Ki', 'Kd')}
        breaches = [k for k, v in deltas.items() if v > self.thresholds[k]]
        if breaches:
            return {'apply': False, 'needs_manual': True, 'deltas': deltas,
                    'reason': f'threshold exceeded for {breaches}'}
        return {'apply': True, 'needs_manual': False, 'deltas': deltas,
                'reason': 'within thresholds'}

    def reset(self):
        self.update_count = 0


# ─────────────────────────────────────────────────────────────────────────────
# Experiment Manager (unchanged from the original tune_pid.py)
# ─────────────────────────────────────────────────────────────────────────────

class ExperimentManager:
    STEP = 'step'
    CHIRP = 'chirp'
    PRBS = 'prbs'

    def __init__(self, Ts: float, amplitude: float = 50.0):
        self.Ts = Ts
        self.amplitude = amplitude
        self._step = 0
        self._active = False
        self._signal_type = None
        self._signal_buffer = []
        self._results = []

    def start(self, signal_type: str, duration_s: float):
        n_samples = int(duration_s / self.Ts)
        self._signal_buffer = self._generate(signal_type, n_samples)
        self._step = 0
        self._active = True
        self._signal_type = signal_type
        self._results = []
        return len(self._signal_buffer)

    def _generate(self, signal_type: str, n: int):
        A = self.amplitude
        if signal_type == self.STEP:
            sig = np.zeros(n)
            sig[int(0.2 * n):int(0.7 * n)] = A
            return sig.tolist()
        elif signal_type == self.CHIRP:
            t = np.arange(n) * self.Ts
            f0, f1 = 0.1, 5.0
            phase = 2 * np.pi * (f0 * t + 0.5 * (f1 - f0) / t[-1] * t ** 2)
            return (A * np.sin(phase)).tolist()
        elif signal_type == self.PRBS:
            register = [1] * 7
            seq = []
            for _ in range(n):
                bit = register[-1] ^ register[-3]
                seq.append(A if register[-1] else -A)
                register = [bit] + register[:-1]
            return seq
        else:
            raise ValueError(f'Unknown signal type: {signal_type}')

    def tick(self, y_current: float):
        if not self._active or self._step >= len(self._signal_buffer):
            self._active = False
            return 0.0, True
        u = self._signal_buffer[self._step]
        self._results.append((float(y_current), float(u)))
        self._step += 1
        done = self._step >= len(self._signal_buffer)
        if done:
            self._active = False
        return u, done

    @property
    def is_active(self):
        return self._active

    @property
    def progress(self):
        """0.0-1.0, how far through the current/last signal buffer we are -
        not in the original tune_pid.py (nothing there needed a progress
        readout), added purely as a read-only convenience for a live
        progress bar. Does not change tuning behavior."""
        if not self._signal_buffer:
            return 0.0
        return min(1.0, self._step / len(self._signal_buffer))

    def get_results(self):
        return list(self._results)

    def run_batch_rls(self, rls: RLSEstimator):
        rls.reset_covariance(P_init=5000.0)
        for y, u in self._results:
            rls.update(y, u)
        return rls.theta.copy()


# ─────────────────────────────────────────────────────────────────────────────
# Per-wheel orchestration - exact port of PidTunerNode's former inline
# per-wheel loop bodies (_telemetry_cb / _run_experiment_cb / _set_gains_cb
# / _set_rls_cb), just addressed by method call instead of ROS message.
# ─────────────────────────────────────────────────────────────────────────────

class WheelTuner:
    """
    One wheel's worth of RLS + pole-placement + threshold-monitor +
    experiment-manager state, for BOTH loops (pos = steering angle,
    vel = drive rate). tune_pid.py's PidTunerNode holds one of these per
    wheel instead of the parallel per-wheel arrays it used to maintain by
    hand - same algorithm, same defaults, same thresholds.
    """

    def __init__(self, Ts, name='W0', mag_offset=0.0, pos_flip=False, vel_flip=False,
                 lambda_pos=0.97, lambda_vel=0.97, T_settle_pos=0.5, T_settle_vel=0.3,
                 Kp_thresh=3.0, Ki_thresh=1.0, Kd_thresh=1.0, min_rls_warmup=20,
                 init_pos_gains=(15.0, 1.0, 1.0), init_vel_gains=(5.0, 0.0, 0.0)):
        self.Ts = Ts
        self.name = name
        self.mag_offset = mag_offset
        self.pos_flip = pos_flip
        self.vel_flip = vel_flip

        self.rls_pos = RLSEstimator(lam=lambda_pos)
        self.rls_vel = RLSEstimator(lam=lambda_vel)
        self.pp_pos = PolePlacementPID(Ts=Ts, T_settle=T_settle_pos)
        self.pp_vel = PolePlacementPID(Ts=Ts, T_settle=T_settle_vel)
        self.mon_pos = GainChangeMonitor(Kp_thresh, Ki_thresh, Kd_thresh, min_rls_warmup)
        self.mon_vel = GainChangeMonitor(Kp_thresh, Ki_thresh, Kd_thresh, min_rls_warmup)
        self.exp_pos = ExperimentManager(Ts)
        self.exp_vel = ExperimentManager(Ts)

        pk, pi_, pd_ = init_pos_gains
        vk, vi, vd = init_vel_gains
        self.current_pos_gains = {'Kp': pk, 'Ki': pi_, 'Kd': pd_}
        self.current_vel_gains = {'Kp': vk, 'Ki': vi, 'Kd': vd}

        self.last_pos_cmd = 0.0
        self.last_vel_cmd = 0.0
        self.manual_override_pos = False
        self.manual_override_vel = False
        self.last_needs_manual = False

    def set_commands(self, pos_cmd, vel_cmd):
        """Mirrors _commands_cb's per-wheel assignment."""
        self.last_pos_cmd = float(pos_cmd)
        self.last_vel_cmd = float(vel_cmd)

    def on_telemetry(self, raw_angle, speed, auto_tune=True):
        """
        Mirrors _telemetry_cb's per-wheel loop body exactly.

        auto_tune=False skips the continuous-RLS-update step (current
        gains are left untouched) while STILL servicing any active
        experiment and batch-RLS-recomputing when it completes - this is
        the hook a caller uses to implement a "continuous auto-tune
        on/off" toggle without it fighting a manually-triggered
        experiment. Returns (pos_gains, vel_gains, needs_manual, log_lines).
        """
        pos_y = raw_angle - self.mag_offset
        while pos_y > 180:
            pos_y -= 360
        while pos_y < -180:
            pos_y += 360
        if self.pos_flip:
            pos_y = -pos_y

        vel_y = float(speed)
        if self.vel_flip:
            vel_y = -vel_y

        pos_u = self.last_pos_cmd
        vel_u = self.last_vel_cmd
        log = []

        if self.exp_pos.is_active:
            exp_u, done = self.exp_pos.tick(pos_y)
            pos_u = exp_u
            if done:
                self.exp_pos.run_batch_rls(self.rls_pos)
                self._recompute_pos()
                log.append(f'[{self.name}] POS experiment complete - gains recomputed')

        if self.exp_vel.is_active:
            exp_u, done = self.exp_vel.tick(vel_y)
            vel_u = exp_u
            if done:
                self.exp_vel.run_batch_rls(self.rls_vel)
                self._recompute_vel()
                log.append(f'[{self.name}] VEL experiment complete - gains recomputed')

        is_manual = False

        if auto_tune and not self.manual_override_pos:
            self.rls_pos.update(pos_y, pos_u)
            params_pos = self.rls_pos.get_plant_params()
            proposed_pos = self.pp_pos.compute_gains(params_pos['K'], params_pos['pole_mag'])
            result_pos = self.mon_pos.check(self.current_pos_gains, proposed_pos)
            if result_pos['apply']:
                self.current_pos_gains = proposed_pos
            elif result_pos['needs_manual']:
                is_manual = True
                log.append(f'[{self.name}] POS gains need manual review: {result_pos["reason"]}')

        if auto_tune and not self.manual_override_vel:
            self.rls_vel.update(vel_y, vel_u)
            params_vel = self.rls_vel.get_plant_params()
            proposed_vel = self.pp_vel.compute_gains(params_vel['K'], params_vel['pole_mag'])
            result_vel = self.mon_vel.check(self.current_vel_gains, proposed_vel)
            if result_vel['apply']:
                self.current_vel_gains = proposed_vel
            elif result_vel['needs_manual']:
                is_manual = True
                log.append(f'[{self.name}] VEL gains need manual review: {result_vel["reason"]}')

        self.last_needs_manual = is_manual
        return self.current_pos_gains, self.current_vel_gains, is_manual, log

    def start_experiment(self, loop, signal_type, duration_s, amplitude=50.0):
        """Mirrors _run_experiment_cb's per-wheel body. loop is 'pos' or
        'vel'. Returns the number of samples the experiment will run for."""
        if loop == 'pos':
            self.exp_pos.amplitude = amplitude
            n = self.exp_pos.start(signal_type, duration_s)
            self.manual_override_pos = True
            return n
        elif loop == 'vel':
            self.exp_vel.amplitude = amplitude
            n = self.exp_vel.start(signal_type, duration_s)
            self.manual_override_vel = True
            return n
        raise ValueError(f'Unknown loop "{loop}" - use "pos" or "vel"')

    def set_manual_gains(self, loop, kp, ki, kd):
        """Mirrors _set_gains_cb."""
        gains = {'Kp': kp, 'Ki': ki, 'Kd': kd}
        if loop == 'pos':
            self.current_pos_gains = gains
            self.manual_override_pos = True
            self.mon_pos.reset()
        elif loop == 'vel':
            self.current_vel_gains = gains
            self.manual_override_vel = True
            self.mon_vel.reset()
        else:
            raise ValueError(f'Unknown loop "{loop}" - use "pos" or "vel"')

    def resume_auto_tune(self, loop='both'):
        """Mirrors _set_rls_cb's resume_rls path. loop is 'pos', 'vel', or
        'both'."""
        if loop in ('pos', 'both'):
            self.manual_override_pos = False
            self.mon_pos.reset()
        if loop in ('vel', 'both'):
            self.manual_override_vel = False
            self.mon_vel.reset()

    def set_lambda(self, loop, lam):
        """Mirrors _set_rls_cb's lambda-update path."""
        if loop in ('pos', 'both'):
            self.rls_pos.set_lambda(lam)
        if loop in ('vel', 'both'):
            self.rls_vel.set_lambda(lam)

    def reset_covariance(self, loop='both'):
        """Mirrors _set_rls_cb's reset_cov path."""
        if loop in ('pos', 'both'):
            self.rls_pos.reset_covariance()
        if loop in ('vel', 'both'):
            self.rls_vel.reset_covariance()

    def _recompute_pos(self):
        params = self.rls_pos.get_plant_params()
        self.current_pos_gains = self.pp_pos.compute_gains(params['K'], params['pole_mag'])
        self.manual_override_pos = False
        self.mon_pos.reset()

    def _recompute_vel(self):
        params = self.rls_vel.get_plant_params()
        self.current_vel_gains = self.pp_vel.compute_gains(params['K'], params['pole_mag'])
        self.manual_override_vel = False
        self.mon_vel.reset()
