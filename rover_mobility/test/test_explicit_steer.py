"""
Stress tests for controllers/explicit_steer.py (per-wheel EKF + PID steering controller).

Pure math, no ROS - runs directly under plain pytest. See
rover_mobility_review/rover_mobility_review.md for the write-up these tests
provide evidence for, in particular the EKF unit-mismatch bug
(mobility_node.py feeds degree-space sensor readings into a count-space
filter) reproduced in isolation here.
"""
import math

import numpy as np
import pytest

from rover_mobility.controllers.explicit_steer import (
    count_to_deg,
    COUNTS_PER_REV,
    deg_to_count,
    ExplicitController,
    SteerPID,
    wrap_count,
    wrap_count_diff,
)


class TestCountConversions:

    @pytest.mark.parametrize('deg', [-181, -45, 0, 45, 90, 180, 270, 359, 400])
    def test_round_trip_modulo_360(self, deg):
        assert count_to_deg(deg_to_count(deg)) == pytest.approx(deg % 360.0, abs=1e-9)

    def test_wrap_count_various(self):
        assert wrap_count(300) == pytest.approx(44.0)
        assert wrap_count(-10) == pytest.approx(246.0)
        assert wrap_count(256) == pytest.approx(0.0)
        assert wrap_count(512.5) == pytest.approx(0.5)


class TestWrapCountDiff:

    def test_normal_case_is_antisymmetric(self):
        assert wrap_count_diff(10, 0) == pytest.approx(10.0)
        assert wrap_count_diff(0, 10) == pytest.approx(-10.0)

    def test_exact_half_period_tie_break_is_always_positive(self):
        """
        At exactly period/2 the `d > period/2` comparison is a strict inequality, so.

        BOTH directions resolve to +128, not the expected antisymmetric +-128 - a real,
        deterministic edge case worth knowing about rather than assuming symmetry holds
        everywhere.
        """
        assert wrap_count_diff(128, 0) == pytest.approx(128.0)
        assert wrap_count_diff(0, 128) == pytest.approx(128.0)


class TestExplicitControllerConstruction:

    def test_t_motor_zero_raises_at_construction(self):
        with pytest.raises(ZeroDivisionError):
            ExplicitController(dt=0.01, t_motor=0.0)


class TestExplicitControllerStep:

    def test_dt_zero_produces_silent_nan_that_gets_clamped_to_full_power(self):
        """
        Empirically verified - NOT the ZeroDivisionError one might expect by analogy.

        with DrivePID (drive_pid.py operates on plain Python floats/ints, so its dt=0
        case genuinely raises - see test_drive_pid.py). Here, self.x is a numpy array,
        so `error` (from wrap_count_diff on x[0]) is numpy.float64: dividing it by
        dt=0.0 silently returns numpy inf/nan with a RuntimeWarning instead of raising.
        With the default kd=0.0, `0.0 * inf` is nan, so the raw PID output is NaN - but
        then `max(-1.0, min(1.0, pwm))` silently clamps that NaN to exactly +1.0,
        because Python's builtin min/max keep their first argument whenever a NaN
        comparison returns False. Net effect: dt=0 does not crash and does not even
        surface as NaN in the output - it silently commands full positive steering
        power.
        """
        ctl = ExplicitController(dt=0.0)
        with pytest.warns(RuntimeWarning):
            pwm, _ = ctl.step(target_count=10)
        assert not math.isnan(pwm), 'pwm is silently clamped away from NaN, not left as NaN'
        assert pwm == pytest.approx(1.0)

    def test_pwm_output_is_clamped_to_unit_range(self):
        ctl_pos = ExplicitController(dt=0.01, pid_kp=1000.0)
        pwm_pos, _ = ctl_pos.step(target_count=128, z=None)
        assert pwm_pos == pytest.approx(1.0)

        ctl_neg = ExplicitController(dt=0.01, pid_kp=1000.0)
        pwm_neg, _ = ctl_neg.step(target_count=129, z=None)
        assert pwm_neg == pytest.approx(-1.0)

    def test_multiple_instances_do_not_share_state(self):
        ctl_a = ExplicitController(dt=0.01)
        ctl_b = ExplicitController(dt=0.01)
        ctl_a.step(target_count=10, z=[10.0, 10.0, 0.0])
        assert ctl_b.x[0] == pytest.approx(0.0)
        assert not np.array_equal(ctl_a.x, ctl_b.x)

    def test_identical_measurement_rows_with_zero_variance_are_singular(self):
        """
        H's mag/quad rows are both [1, 0] (structurally indistinguishable to the model).

        If their measurement variances are both driven to 0, S becomes singular and the
        Kalman gain computation blows up.
        """
        ctl = ExplicitController(dt=0.01, r_diag=(0.0, 0.0, 0.01))
        with pytest.raises(np.linalg.LinAlgError):
            ctl.step(target_count=0, z=[10.0, 10.0, 0.0])


class TestExplicitControllerConvergence:

    def test_correctly_scaled_count_input_converges_to_true_angle(self):
        """
        Baseline correctness proof: when z IS in count-space as the EKF expects, it.

        converges to the true angle.
        """
        ctl = ExplicitController(dt=0.01)
        physical_angle_deg = 90.0
        correct_count = deg_to_count(physical_angle_deg)
        z = [correct_count, correct_count, 0.0]
        for _ in range(500):
            ctl.step(target_count=0, z=z)
        assert count_to_deg(ctl.x[0]) == pytest.approx(physical_angle_deg, abs=2.0)

    def test_degrees_fed_as_counts_reproduces_real_unit_mismatch_bug(self):
        """
        Reproduces mobility_node.py's ACTUAL can_receive() -> update() data path in.

        isolation: format_magnetic_angle() returns DEGREES, and that value is stored
        directly as z[0] (mag_count) without ever passing through deg_to_count(). This
        demonstrates the resulting bias concretely: a real physical angle of 90 degrees
        ends up estimated by the filter as ~126.6 degrees, not 90 - independent of (and
        would still happen even after fixing) the CAN wiring bugs.
        """
        ctl = ExplicitController(dt=0.01)
        physical_angle_deg = 90.0
        z = [physical_angle_deg, physical_angle_deg, 0.0]  # what can_receive() actually sends
        for _ in range(500):
            ctl.step(target_count=0, z=z)
        estimated_deg = count_to_deg(ctl.x[0])
        assert estimated_deg == pytest.approx(count_to_deg(physical_angle_deg), abs=2.0)
        assert estimated_deg != pytest.approx(physical_angle_deg, abs=5.0)

    def test_predict_only_no_feedback_just_decays_towards_frozen_position(self):
        """
        With z permanently None (the real, current effect of bug #3 - no wheel is ever.

        actually subscribed to CAN telemetry), the EKF is not 'holding position' in any
        physically meaningful sense: predict() has no control-input term, so omega_count
        just exponentially decays toward 0 every tick regardless of what the real wheel
        is doing, and theta_count drifts only by whatever residual omega integrates
        before it dies out, then stalls.
        """
        ctl = ExplicitController(dt=0.01, t_motor=0.15)
        ctl.x = np.array([50.0, 20.0])  # pretend theta=50 counts, omega=20 counts/tick-ish
        thetas = []
        for _ in range(2000):
            ctl.predict()
            thetas.append(ctl.x[0])
        assert abs(ctl.x[1]) < 1e-3, 'omega should have decayed to ~0 with no control input'
        assert abs(thetas[-1] - thetas[-100]) < 1e-6, (
            'theta should have stalled once omega died out - it is not tracking real motion'
        )


class TestExplicitControllerTrust:
    """
    Tests for the `trust` parameter on update()/step().

    Added so mobility_node.py can exclude a sensor reported down by
    sensor_check_<suf> from this wheel's EKF update without risking a
    singular S the way literally zeroing that sensor's r_diag entry would
    (see test_identical_measurement_rows_with_zero_variance_are_singular
    above - that's the exact failure mode `trust` is designed to avoid).
    """

    def test_default_trust_matches_fully_trusted_explicit_call(self):
        ctl_default = ExplicitController(dt=0.01)
        ctl_explicit = ExplicitController(dt=0.01)
        z = [64.0, 64.0, 0.0]
        for _ in range(50):
            ctl_default.step(target_count=0, z=z)
            ctl_explicit.step(target_count=0, z=z, trust=(1, 1, 1))
        assert np.allclose(ctl_default.x, ctl_explicit.x)
        assert np.allclose(ctl_default.P, ctl_explicit.P)

    def test_untrusted_mag_channel_has_zero_influence(self):
        """
        A wildly wrong mag reading with trust mag=0 must converge identically to a.

        controller that never saw a wrong mag reading at all - proving the
        untrusted channel has exactly zero effect, not just "reduced" effect.
        """
        ctl_bad_mag_untrusted = ExplicitController(dt=0.01)
        ctl_good_mag_trusted = ExplicitController(dt=0.01)
        true_count = 64.0
        bad_z = [999999.0, true_count, 0.0]
        good_z = [true_count, true_count, 0.0]
        for _ in range(500):
            ctl_bad_mag_untrusted.step(target_count=0, z=bad_z, trust=(0, 1, 1))
            ctl_good_mag_trusted.step(target_count=0, z=good_z, trust=(1, 1, 1))
        assert np.allclose(ctl_bad_mag_untrusted.x, ctl_good_mag_trusted.x, atol=1e-6)

    def test_untrusted_imu_channel_has_zero_influence(self):
        ctl_bad_imu_untrusted = ExplicitController(dt=0.01)
        ctl_good_imu_trusted = ExplicitController(dt=0.01)
        true_count = 64.0
        bad_z = [true_count, true_count, 99999.0]
        good_z = [true_count, true_count, 0.0]
        for _ in range(500):
            ctl_bad_imu_untrusted.step(target_count=0, z=bad_z, trust=(1, 1, 0))
            ctl_good_imu_trusted.step(target_count=0, z=good_z, trust=(1, 1, 1))
        assert np.allclose(ctl_bad_imu_untrusted.x, ctl_good_imu_trusted.x, atol=1e-6)

    def test_excluding_a_channel_keeps_s_invertible_with_real_gains(self):
        """
        Regression guard for the exact scenario sensor_check triggers: mag reported.

        down (trust mag=0) under normal (nonzero) r_diag must NOT raise
        LinAlgError, unlike setting r_diag itself to 0.
        """
        ctl = ExplicitController(dt=0.01)  # default r_diag, all nonzero
        try:
            ctl.step(target_count=0, z=[10.0, 10.0, 0.0], trust=(0, 1, 1))
        except np.linalg.LinAlgError:
            pytest.fail('excluding a channel via trust should not make S singular')

    def test_both_mag_and_imu_untrusted_still_tracks_from_quad_alone(self):
        ctl = ExplicitController(dt=0.01)
        true_count = 100.0
        for _ in range(500):
            ctl.step(target_count=0, z=[0.0, true_count, 0.0], trust=(0, 1, 0))
        assert count_to_deg(ctl.x[0]) == pytest.approx(count_to_deg(true_count), abs=2.0)


class TestSteerPIDDirectly:

    def test_zero_dt_raises(self):
        pid = SteerPID(kp=1.0, ki=0.0, kd=0.0)
        with pytest.raises(ZeroDivisionError):
            pid.update(target=10, current=0, dt=0.0)

    def test_no_anti_windup_integral_grows_unbounded(self):
        """
        Documents that ki>0 has no integral clamp/back-calculation - dormant today since.

        params.yaml ships ki=0.0, but real if changed.
        """
        pid = SteerPID(kp=0.0, ki=1.0, kd=0.0, period=COUNTS_PER_REV)
        for _ in range(1000):
            pid.update(target=128, current=0, dt=1.0)
        assert pid.integral > 100000  # unbounded growth, no clamp anywhere
