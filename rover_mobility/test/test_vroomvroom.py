"""
Stress tests for controllers/vroomvroom.py (VroomVroom swerve kinematics).

Pure math, no ROS - runs directly under plain pytest. See
rover_mobility_review/rover_mobility_review.md for the write-up these tests
provide evidence for.
"""
import math

import pytest

from rover_mobility.controllers.vroomvroom import VroomVroom


def _assert_all_finite(values):
    for v in values:
        assert math.isfinite(v), f'non-finite value in {values}'


class TestSmoooothOperatorrrr:

    def test_zero_input_gives_zero_velocity(self):
        vroom = VroomVroom()
        angles, vels = vroom.smooooth_operatorrrr(0, 0, 0)
        _assert_all_finite(angles)
        _assert_all_finite(vels)
        # throttle=0 zeroes every velocity exactly, regardless of angle math
        for v in vels:
            assert v == pytest.approx(0.0, abs=1e-9)

    def test_max_throttle_straight_all_wheels_equal_speed(self):
        vroom = VroomVroom(speed_scalar=250.0)
        angles, vels = vroom.smooooth_operatorrrr(1.0, 0, 0)
        _assert_all_finite(angles)
        _assert_all_finite(vels)
        for v in vels:
            assert v == pytest.approx(250.0, rel=1e-3)
        for a in angles:
            assert a == pytest.approx(0.0, abs=0.1)

    def test_full_reverse_mirrors_full_forward_speed_magnitude(self):
        vroom = VroomVroom(speed_scalar=250.0)
        _, vels_fwd = vroom.smooooth_operatorrrr(1.0, 0, 0)
        _, vels_rev = vroom.smooooth_operatorrrr(-1.0, 0, 0)
        for vf, vr in zip(vels_fwd, vels_rev):
            assert vr == pytest.approx(-vf, rel=1e-3)

    @pytest.mark.parametrize('rotate', [-1.0, -0.999999, -0.5, 0.0, 0.5, 0.999999, 1.0])
    def test_rotate_sweep_never_produces_nan_or_inf(self, rotate):
        """
        rotate=+-1 gets close to the tan(pi/2) singularity but the code's `pi/2 - 0.01`.

        epsilon should keep R finite everywhere in [-1, 1].
        """
        vroom = VroomVroom()
        angles, vels = vroom.smooooth_operatorrrr(1.0, rotate, 0)
        _assert_all_finite(angles)
        _assert_all_finite(vels)

    def test_throttle_zero_with_full_rotate_still_yields_zero_velocity(self):
        """
        Documented UX quirk: releasing throttle (joy_y=0) zeroes all wheel velocities.

        even at full rotate input - "rotate in place" requires throttle to be nonzero,
        it is not a self-sufficient axis.
        """
        vroom = VroomVroom()
        _, vels = vroom.smooooth_operatorrrr(0.0, 1.0, 0.0)
        for v in vels:
            assert v == pytest.approx(0.0, abs=1e-9)

    def test_repeated_calls_are_idempotent(self):
        """Pure function, no hidden state - same input must give same output every time."""
        vroom = VroomVroom()
        out1 = vroom.smooooth_operatorrrr(0.6, -0.3, 0.2)
        out2 = vroom.smooooth_operatorrrr(0.6, -0.3, 0.2)
        assert out1 == out2

    @pytest.mark.parametrize('deadzone,inside,outside', [
        (0.1, 0.1, 0.1000001),
        (0.2, 0.2, 0.2000001),
    ])
    def test_deadzone_boundary_is_inclusive(self, deadzone, inside, outside):
        """
        abs(throttle) <= deadzone zeroes it (boundary inclusive); anything strictly.

        above the deadzone passes through.
        """
        vroom = VroomVroom(deadzone=deadzone, speed_scalar=250.0)
        _, vels_inside = vroom.smooooth_operatorrrr(inside, 0, 0)
        _, vels_outside = vroom.smooooth_operatorrrr(outside, 0, 0)
        for v in vels_inside:
            assert v == pytest.approx(0.0, abs=1e-9)
        assert any(abs(v) > 1e-9 for v in vels_outside)

    def test_crab_plus_minus_one_are_mirror_images(self):
        """
        crab=+1 and crab=-1 (with rotate=0) drive from_R_vec with the SAME R_vec but.

        opposite `flipper`, so velocities must match exactly and angles must differ by
        exactly 180 degrees (mod 360).
        """
        vroom = VroomVroom()
        angles_pos, vels_pos = vroom.smooooth_operatorrrr(1.0, 0, 1.0)
        angles_neg, vels_neg = vroom.smooooth_operatorrrr(1.0, 0, -1.0)
        for vp, vn in zip(vels_pos, vels_neg):
            assert vn == pytest.approx(vp, rel=1e-6)
        for ap, an in zip(angles_pos, angles_neg):
            diff = (an - ap) % 360.0
            assert diff == pytest.approx(180.0, abs=1e-3)

    def test_simultaneous_throttle_rotate_crab_stays_finite(self):
        """
        Every axis pushed hard at once - the combination most likely to expose a hidden.

        singularity.
        """
        vroom = VroomVroom()
        for throttle in (-1.0, 1.0):
            for rotate in (-1.0, 1.0):
                for crab in (-1.0, 1.0):
                    angles, vels = vroom.smooooth_operatorrrr(throttle, rotate, crab)
                    _assert_all_finite(angles)
                    _assert_all_finite(vels)


class TestFromRVec:

    def test_wheel_at_icr_has_zero_required_velocity(self):
        """
        If the instantaneous center of rotation is placed exactly at one wheel's own.

        body-frame position, that wheel doesn't need to move - directly probes which
        output index corresponds to which physical corner, independent of any
        WHEEL_ORDER labeling assumption.
        """
        vroom = VroomVroom(half_width=0.35, half_length=0.45)
        a, b = vroom.a, vroom.b
        corners = [(a, b), (a, -b), (-a, b), (-a, -b)]  # matches w1..w4 formula
        for i, (cx, cy) in enumerate(corners):
            angles, vels = vroom.from_R_vec([cx, cy], flipper=False)
            _assert_all_finite(angles)
            _assert_all_finite(vels)
            assert vels[i] == pytest.approx(0.0, abs=1e-9), (
                f'wheel index {i} should be motionless when ICR is at its own corner {(cx, cy)}'
            )
            for j in range(4):
                if j != i:
                    assert vels[j] > 1e-6, f'wheel index {j} should be moving'

    def test_flipper_adds_exactly_180_degrees(self):
        vroom = VroomVroom()
        angles_a, vels_a = vroom.from_R_vec([0.1, 0.2], flipper=False)
        angles_b, vels_b = vroom.from_R_vec([0.1, 0.2], flipper=True)
        assert vels_a == vels_b
        for aa, ab in zip(angles_a, angles_b):
            diff = (ab - aa) % 360.0
            assert diff == pytest.approx(180.0, abs=1e-9)

    def test_output_angles_stay_in_wrapped_range(self):
        vroom = VroomVroom()
        for R in (-1000.0, -0.01, 0.01, 1000.0):
            angles, _ = vroom.from_R_vec([R, R * 0.3], flipper=False)
            for a in angles:
                assert -180.0 <= a <= 180.0


class TestWateringWell:
    """
    Alternate/unused-looking kinematics mode - smoke-tested for the explicit zero-guards.

    the code carries (frontz==0 -> 1e-5, yaww==0 -> 1e-10), not for physical correctness
    (no caller in mobility_node.py exercises this method today).
    """

    @pytest.mark.parametrize('frontz,sidez,yaww', [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (-1.0, 0.5, 0.2),
        (1.0, -0.5, -0.2),
        (0.0, 0.0, 1.0),
    ])
    def test_zero_guards_prevent_division_errors(self, frontz, sidez, yaww):
        vroom = VroomVroom()
        angles, vels = vroom.watering_well(frontz, sidez, yaww)
        _assert_all_finite(angles)
        _assert_all_finite(vels)
