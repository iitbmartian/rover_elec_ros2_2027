"""
Stress tests for controllers/drive_pid.py (per-wheel drive-velocity controller).

Rollover-safe tick-delta feedback -> plain PID. Pure math, no ROS - runs
directly under plain pytest. See
rover_mobility_review/rover_mobility_review.md for the write-up these tests
provide evidence for.
"""
import pytest

from rover_mobility.controllers.drive_pid import DriveController, DrivePID, signed_tick_delta


class TestSignedTickDelta:

    def test_normal_small_delta(self):
        assert signed_tick_delta(110, 100, 65536) == pytest.approx(10.0)
        assert signed_tick_delta(100, 110, 65536) == pytest.approx(-10.0)

    def test_rollover_forward_across_boundary(self):
        # 8-bit counter wraps 250 -> 5 (advanced by 11 ticks)
        assert signed_tick_delta(5, 250, 256) == pytest.approx(11.0)

    def test_rollover_backward_across_boundary(self):
        # 8-bit counter "wraps" 5 -> 250 interpreted as -11 ticks
        assert signed_tick_delta(250, 5, 256) == pytest.approx(-11.0)

    def test_exact_half_modulus_tie_break_is_always_positive(self):
        """
        Same asymmetric tie-break as wrap_count_diff in explicit_steer.py (strict `>`.

        comparison): both directions resolve to +modulus/2.
        """
        assert signed_tick_delta(128, 0, 256) == pytest.approx(128.0)
        assert signed_tick_delta(0, 128, 256) == pytest.approx(128.0)


class TestDrivePIDDirectly:

    def test_zero_dt_raises(self):
        pid = DrivePID(kp=1.0, ki=0.0, kd=0.0)
        with pytest.raises(ZeroDivisionError):
            pid.update(target=10, current=0, dt=0.0)

    def test_no_anti_windup_integral_grows_unbounded(self):
        """
        Ki has no integral clamp/back-calculation.

        Dormant today since params.yaml ships ki=0.0, but real if changed.
        """
        pid = DrivePID(kp=0.0, ki=1.0, kd=0.0)
        for _ in range(1000):
            pid.update(target=50.0, current=0.0, dt=1.0)
        assert pid.integral > 10000


class TestDriveControllerStep:

    def test_first_call_returns_none(self):
        """
        Deliberate design: no prior tick reading yet, so it declines to fabricate a pwm.

        off an undefined delta.
        """
        ctl = DriveController(dt=0.01)
        assert ctl.step(1.0, 0.5, quad=100) is None

    def test_second_call_returns_a_pwm_value(self):
        ctl = DriveController(dt=0.01)
        ctl.step(1.0, 0.5, quad=100)
        pwm = ctl.step(1.0, 0.5, quad=110)
        assert pwm is not None
        assert -1.0 <= pwm <= 1.0

    def test_pwm_output_is_clamped_to_unit_range(self):
        ctl = DriveController(dt=0.01, max_ticks_per_dt=1.0, pid_kp=1000.0)
        ctl.step(1.0, 1.0, quad=0)
        # zero measured delta vs. a large target -> large error -> huge pid_out
        pwm = ctl.step(1.0, 1.0, quad=0)
        assert pwm == pytest.approx(1.0)

    def test_multiple_instances_do_not_share_state(self):
        ctl_a = DriveController(dt=0.01)
        ctl_b = DriveController(dt=0.01)
        ctl_a.step(1.0, 0.5, quad=100)
        ctl_a.step(1.0, 0.5, quad=110)
        assert ctl_b._prev_quad is None

    @pytest.mark.parametrize('bits,expected_modulus', [(8, 256), (16, 65536), (32, 4294967296)])
    def test_tick_counter_bits_sets_modulus(self, bits, expected_modulus):
        ctl = DriveController(dt=0.01, tick_counter_bits=bits)
        assert ctl.tick_counter_mod == expected_modulus

    def test_tick_counter_bits_zero_is_degenerate_but_does_not_crash(self):
        """
        1 << 0 == 1, so every delta collapses mod 1 to exactly 0 - velocity feedback.

        becomes permanently zero rather than raising, a silent-degradation edge case
        worth knowing about.
        """
        ctl = DriveController(dt=0.01, tick_counter_bits=0)
        assert ctl.tick_counter_mod == 1
        ctl.step(1.0, 0.5, quad=5)
        pwm = ctl.step(1.0, 0.5, quad=999)
        assert ctl.measured_ticks_per_dt == pytest.approx(0.0)
        assert pwm is not None

    def test_negative_tick_counter_bits_raises_value_error(self):
        with pytest.raises(ValueError):
            DriveController(dt=0.01, tick_counter_bits=-1)

    def test_max_ticks_per_dt_zero_raises_zero_division(self):
        ctl = DriveController(dt=0.01, max_ticks_per_dt=0.0)
        ctl.step(1.0, 0.5, quad=0)
        with pytest.raises(ZeroDivisionError):
            ctl.step(1.0, 0.5, quad=5)

    def test_dt_zero_raises_zero_division(self):
        ctl = DriveController(dt=0.0)
        ctl.step(1.0, 0.5, quad=0)
        with pytest.raises(ZeroDivisionError):
            ctl.step(1.0, 0.5, quad=5)
