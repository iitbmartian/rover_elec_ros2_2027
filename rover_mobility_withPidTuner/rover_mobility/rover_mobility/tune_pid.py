#!/usr/bin/env python3
"""
pid_tuner_node.py
Runs one RLS estimator pair (pos + vel) per wheel and publishes updated
PID gains to /pid_gains. Wheel count is a parameter (n_wheels), default 1
for single-wheel bench testing - the algorithm is unchanged from the
4-wheel design, only wheel_names/mag_offsets/flip arrays are now sized
by n_wheels instead of hardcoded to 4.

The actual tuning algorithm (RLSEstimator, PolePlacementPID,
GainChangeMonitor, ExperimentManager, and the per-wheel orchestration that
ties them together) now lives in pid_tuning_core.py, with zero ROS
dependency - this node is a thin ROS wrapper around one WheelTuner per
wheel. Pulled out so a non-ROS consumer (e.g. the standalone joystick
simulation) can run the IDENTICAL algorithm without needing rclpy or a
built all_interfaces package.

Subscribes:
  /telemetry        (all_interfaces/TelemetryData)  - y(k)
  /pid_commands      (all_interfaces/PidCommands)     - u(k)
Publishes:
  /pid_gains         (all_interfaces/PidGains)
Services:
  /set_pid_gains     (all_interfaces/SetPidGains)
  /set_rls_params    (all_interfaces/SetRlsParams)
  /run_experiment     (all_interfaces/RunExperiment)
"""

import rclpy
from rclpy.node import Node

from all_interfaces.msg import TelemetryData, PidGains, PidCommands
from all_interfaces.srv import SetPidGains, SetRlsParams, RunExperiment

from .pid_tuning_core import WheelTuner


class PidTunerNode(Node):

    def __init__(self):
        super().__init__('pid_tuner')

        # ── Parameters (overridable from params.yaml) ─────────────────────
        self.declare_parameter('Ts', 0.05)
        self.declare_parameter('n_wheels', 1)
        self.declare_parameter('wheel_names', ['W0'])
        # mag_offsets/pos_flip/vel_flip: calibration per wheel, replaces the
        # hardcoded 4-length arrays from the original drive_logic.py-coupled
        # version. Length must match n_wheels.
        self.declare_parameter('mag_offsets', [0.0])
        self.declare_parameter('pos_flip', [False])
        self.declare_parameter('vel_flip', [False])
        self.declare_parameter('lambda_pos', 0.97)
        self.declare_parameter('lambda_vel', 0.97)
        self.declare_parameter('T_settle_pos', 0.5)
        self.declare_parameter('T_settle_vel', 0.3)
        self.declare_parameter('Kp_thresh', 3.0)
        self.declare_parameter('Ki_thresh', 1.0)
        self.declare_parameter('Kd_thresh', 1.0)
        self.declare_parameter('min_rls_warmup', 20)
        # starting gains, mirrors current defaults in explicit.py/drive.py
        self.declare_parameter('init_pos_kp', 15.0)
        self.declare_parameter('init_pos_ki', 1.0)
        self.declare_parameter('init_pos_kd', 1.0)
        self.declare_parameter('init_vel_kp', 5.0)
        self.declare_parameter('init_vel_ki', 0.0)
        self.declare_parameter('init_vel_kd', 0.0)

        Ts = self.get_parameter('Ts').value
        self.Ts = Ts
        self.n_wheels = int(self.get_parameter('n_wheels').value)
        self.wheel_names = list(self.get_parameter('wheel_names').value)
        mag_offsets = list(self.get_parameter('mag_offsets').value)
        pos_flip = list(self.get_parameter('pos_flip').value)
        vel_flip = list(self.get_parameter('vel_flip').value)

        for name, arr in (('wheel_names', self.wheel_names),
                           ('mag_offsets', mag_offsets),
                           ('pos_flip', pos_flip),
                           ('vel_flip', vel_flip)):
            if len(arr) != self.n_wheels:
                raise ValueError(
                    f"param '{name}' has length {len(arr)}, expected n_wheels={self.n_wheels}"
                )

        lam_pos = self.get_parameter('lambda_pos').value
        lam_vel = self.get_parameter('lambda_vel').value
        T_settle_pos = self.get_parameter('T_settle_pos').value
        T_settle_vel = self.get_parameter('T_settle_vel').value
        Kp_thresh = self.get_parameter('Kp_thresh').value
        Ki_thresh = self.get_parameter('Ki_thresh').value
        Kd_thresh = self.get_parameter('Kd_thresh').value
        min_warmup = self.get_parameter('min_rls_warmup').value

        init_pos_gains = (
            self.get_parameter('init_pos_kp').value,
            self.get_parameter('init_pos_ki').value,
            self.get_parameter('init_pos_kd').value,
        )
        init_vel_gains = (
            self.get_parameter('init_vel_kp').value,
            self.get_parameter('init_vel_ki').value,
            self.get_parameter('init_vel_kd').value,
        )

        self.tuners = [
            WheelTuner(
                Ts=Ts, name=self.wheel_names[i], mag_offset=mag_offsets[i],
                pos_flip=pos_flip[i], vel_flip=vel_flip[i],
                lambda_pos=lam_pos, lambda_vel=lam_vel,
                T_settle_pos=T_settle_pos, T_settle_vel=T_settle_vel,
                Kp_thresh=Kp_thresh, Ki_thresh=Ki_thresh, Kd_thresh=Kd_thresh,
                min_rls_warmup=min_warmup,
                init_pos_gains=init_pos_gains, init_vel_gains=init_vel_gains,
            )
            for i in range(self.n_wheels)
        ]

        self.telemetry_sub = self.create_subscription(
            TelemetryData, '/telemetry', self._telemetry_cb, 10)
        self.cmd_sub = self.create_subscription(
            PidCommands, '/pid_commands', self._commands_cb, 10)
        self.gains_pub = self.create_publisher(PidGains, '/pid_gains', 10)

        self.set_gains_srv = self.create_service(
            SetPidGains, '/set_pid_gains', self._set_gains_cb)
        self.set_rls_srv = self.create_service(
            SetRlsParams, '/set_rls_params', self._set_rls_cb)
        self.experiment_srv = self.create_service(
            RunExperiment, '/run_experiment', self._run_experiment_cb)

        self.get_logger().info(
            f'PID tuner started. n_wheels={self.n_wheels} wheel_names={self.wheel_names} '
            f'Ts={Ts}s lambda_pos={lam_pos} lambda_vel={lam_vel}'
        )

    # ─────────────────────────────────────────────────────────────────────
    def _commands_cb(self, msg: PidCommands):
        for i in range(self.n_wheels):
            self.tuners[i].set_commands(msg.pos_cmds[i], msg.vel_cmds[i])

    def _telemetry_cb(self, msg: TelemetryData):
        updated_gains = PidGains()
        updated_gains.wheel_names = self.wheel_names

        pos_kp, pos_ki, pos_kd = [], [], []
        vel_kp, vel_ki, vel_kd = [], [], []
        manual_flags = []

        for i in range(self.n_wheels):
            pos_gains, vel_gains, is_manual, log = self.tuners[i].on_telemetry(
                float(msg.angles[i]), float(msg.speed[i]))
            for line in log:
                self.get_logger().info(line) if 'complete' in line else self.get_logger().warn(line)

            pos_kp.append(pos_gains['Kp'])
            pos_ki.append(pos_gains['Ki'])
            pos_kd.append(pos_gains['Kd'])
            vel_kp.append(vel_gains['Kp'])
            vel_ki.append(vel_gains['Ki'])
            vel_kd.append(vel_gains['Kd'])
            manual_flags.append(is_manual)

        updated_gains.pos_kp = pos_kp
        updated_gains.pos_ki = pos_ki
        updated_gains.pos_kd = pos_kd
        updated_gains.vel_kp = vel_kp
        updated_gains.vel_ki = vel_ki
        updated_gains.vel_kd = vel_kd
        updated_gains.needs_manual = manual_flags

        self.gains_pub.publish(updated_gains)

    # ─────────────────────────────────────────────────────────────────────
    def _set_gains_cb(self, request, response):
        i = request.wheel_index
        loop = request.loop.lower()
        if i < 0 or i >= self.n_wheels:
            response.success = False
            response.message = f'Invalid wheel index {i}. Use 0-{self.n_wheels - 1}.'
            return response
        if loop not in ('pos', 'vel'):
            response.success = False
            response.message = f'Unknown loop "{loop}". Use "pos" or "vel".'
            return response
        self.tuners[i].set_manual_gains(loop, request.kp, request.ki, request.kd)
        self.get_logger().info(
            f'[{self.wheel_names[i]}] Manual {loop} gains set: '
            f'Kp={request.kp:.3f} Ki={request.ki:.3f} Kd={request.kd:.3f}'
        )
        response.success = True
        response.message = f'{self.wheel_names[i]} {loop} gains updated.'
        return response

    def _set_rls_cb(self, request, response):
        idx = request.wheel_index
        loop = request.loop.lower()
        wheels = list(range(self.n_wheels)) if idx == -1 else [idx]
        for i in wheels:
            if request.lam > 0:
                self.tuners[i].set_lambda(loop, request.lam)
            if request.t_settle > 0:
                if loop in ('pos', 'both'):
                    self.tuners[i].pp_pos.update_settle_time(request.t_settle)
                if loop in ('vel', 'both'):
                    self.tuners[i].pp_vel.update_settle_time(request.t_settle)
            if request.reset_cov:
                self.tuners[i].reset_covariance(loop)
            if request.resume_rls:
                self.tuners[i].resume_auto_tune(loop)
        response.success = True
        response.message = f'RLS params updated for wheels {[self.wheel_names[j] for j in wheels]}.'
        return response

    def _run_experiment_cb(self, request, response):
        i = request.wheel_index
        loop = request.loop.lower()
        sig = request.signal_type.lower()
        dur = request.duration_s
        amp = request.amplitude if request.amplitude > 0 else 50.0
        if i < 0 or i >= self.n_wheels:
            response.success = False
            response.message = f'Invalid wheel index {i}.'
            return response
        if loop not in ('pos', 'vel'):
            response.success = False
            response.message = f'Unknown loop "{loop}".'
            return response
        n = self.tuners[i].start_experiment(loop, sig, dur, amp)
        self.get_logger().info(
            f'[{self.wheel_names[i]}] Starting {sig.upper()} experiment on {loop} loop. '
            f'{n} samples at amplitude={amp}.'
        )
        response.success = True
        response.message = (
            f'Experiment started: {self.wheel_names[i]} {loop} {sig.upper()} '
            f'for {dur}s ({n} samples).'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = PidTunerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
