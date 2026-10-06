"""
Stress tests for the withPidTuner variant of rover_mobility.mobility_node.

Specifically the two things this package adds on top of the base
rover_mobility package: the /pid_gains live-apply callback, and (ported,
same as the base package) the zero-reference calibration feature.

NOT a live-node/rclpy integration test. Import of the module itself only
succeeds because of conftest.py's shim patching can_interfaces.msg.DriveCommand
in memory - see that file's docstring.
"""
from types import SimpleNamespace

from all_interfaces.msg import PidGains
import numpy as np
import pytest

from rover_mobility.mobility_node import MobilityNode, WHEEL_ORDER


class _FakeLogger:

    def warn(self, msg):
        pass

    def info(self, msg):
        pass


class _FakePid:

    def __init__(self):
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.0


class _FakeCtl:

    def __init__(self):
        self.pid = _FakePid()
        self.x = np.array([42.0, 3.0])
        self.P = np.eye(2) * 99.0


def _make_fake_node():
    node = SimpleNamespace()
    node.mag_offsets = [0.0, 0.0, 0.0, 0.0]
    node.quad_offsets = [0.0, 0.0, 0.0, 0.0]
    node._latest_raw_mag = [None, None, None, None]
    node._latest_raw_quad = [None, None, None, None]
    node.steer_ctls = [_FakeCtl() for _ in range(4)]
    node.drive_ctls = [_FakeCtl() for _ in range(4)]
    node.get_logger = lambda: _FakeLogger()
    node._pending_zero = set()
    return node


def _make_pid_gains(pos_kp, pos_ki, pos_kd, vel_kp, vel_ki, vel_kd, needs_manual):
    msg = PidGains()
    msg.wheel_names = WHEEL_ORDER
    msg.pos_kp = pos_kp
    msg.pos_ki = pos_ki
    msg.pos_kd = pos_kd
    msg.vel_kp = vel_kp
    msg.vel_ki = vel_ki
    msg.vel_kd = vel_kd
    msg.needs_manual = needs_manual
    return msg


class TestPidGainsCallback:

    def test_applies_gains_to_all_four_wheels(self):
        node = _make_fake_node()
        msg = _make_pid_gains(
            pos_kp=[1.0, 2.0, 3.0, 4.0], pos_ki=[0.1, 0.2, 0.3, 0.4], pos_kd=[0.0] * 4,
            vel_kp=[5.0, 6.0, 7.0, 8.0], vel_ki=[0.0] * 4, vel_kd=[0.0] * 4,
            needs_manual=[False, False, False, False],
        )
        MobilityNode._pid_gains_cb(node, msg)
        for i in range(4):
            assert node.steer_ctls[i].pid.kp == pytest.approx(msg.pos_kp[i])
            assert node.steer_ctls[i].pid.ki == pytest.approx(msg.pos_ki[i])
            assert node.drive_ctls[i].pid.kp == pytest.approx(msg.vel_kp[i])

    def test_needs_manual_wheel_is_skipped(self):
        node = _make_fake_node()
        original_kp = node.steer_ctls[2].pid.kp
        msg = _make_pid_gains(
            pos_kp=[9.0, 9.0, 9.0, 9.0], pos_ki=[0.0] * 4, pos_kd=[0.0] * 4,
            vel_kp=[9.0, 9.0, 9.0, 9.0], vel_ki=[0.0] * 4, vel_kd=[0.0] * 4,
            needs_manual=[False, False, True, False],   # FL (index 2) flagged
        )
        MobilityNode._pid_gains_cb(node, msg)
        assert node.steer_ctls[0].pid.kp == pytest.approx(9.0)
        assert node.steer_ctls[2].pid.kp == pytest.approx(original_kp)  # untouched
        assert node.steer_ctls[3].pid.kp == pytest.approx(9.0)

    def test_fewer_than_four_wheels_does_not_crash(self):
        """
        A message with fewer than 4 wheels' worth of gains must not crash.

        tune_pid.py's n_wheels is configurable - a message from a
        differently-configured tuner (or mid-startup, before it's read
        n_wheels=4 from params) could carry fewer than 4 entries. Only the
        wheels actually present should be touched, no IndexError.
        """
        node = _make_fake_node()
        msg = _make_pid_gains(
            pos_kp=[1.0], pos_ki=[0.0], pos_kd=[0.0],
            vel_kp=[1.0], vel_ki=[0.0], vel_kd=[0.0],
            needs_manual=[False],
        )
        MobilityNode._pid_gains_cb(node, msg)
        assert node.steer_ctls[0].pid.kp == pytest.approx(1.0)
        assert node.steer_ctls[1].pid.kp == pytest.approx(1.0)  # default, untouched

    def test_empty_needs_manual_does_not_crash(self):
        """
        A PidGains with an empty/short needs_manual must not IndexError.

        Gains still apply in that case since there's no flag telling us
        not to.
        """
        node = _make_fake_node()
        msg = _make_pid_gains(
            pos_kp=[2.0, 2.0, 2.0, 2.0], pos_ki=[0.0] * 4, pos_kd=[0.0] * 4,
            vel_kp=[2.0, 2.0, 2.0, 2.0], vel_ki=[0.0] * 4, vel_kd=[0.0] * 4,
            needs_manual=[],
        )
        MobilityNode._pid_gains_cb(node, msg)
        for i in range(4):
            assert node.steer_ctls[i].pid.kp == pytest.approx(2.0)


class TestApplyZero:
    """
    Ported from the base rover_mobility package's test suite.

    Same feature, same expected behavior, re-verified here since this
    package carries its own copy of mobility_node.py.
    """

    def test_no_telemetry_yet_warns_and_does_not_change_state(self):
        node = _make_fake_node()
        MobilityNode._apply_zero(node, 0)
        assert node.mag_offsets[0] == 0.0
        assert node.quad_offsets[0] == 0.0

    def test_zeroes_offsets_and_resets_ekf_state(self):
        node = _make_fake_node()
        node._latest_raw_mag[1] = 57.3
        node._latest_raw_quad[1] = 128.0
        MobilityNode._apply_zero(node, 1)
        assert node.mag_offsets[1] == pytest.approx(57.3)
        assert node.quad_offsets[1] == pytest.approx(128.0)
        assert np.array_equal(node.steer_ctls[1].x, np.zeros(2))
        assert np.array_equal(node.steer_ctls[1].P, np.eye(2))


class TestOnSetParameters:

    @staticmethod
    def _param(name, value):
        return SimpleNamespace(name=name, value=value)

    def test_valid_wheel_index_queues_that_wheel(self):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('zero_wheel_index', 2)])
        assert result.successful
        assert node._pending_zero == {2}

    def test_out_of_range_index_is_rejected(self):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('zero_wheel_index', 9)])
        assert not result.successful

    def test_zero_all_wheels_queues_every_wheel(self):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('zero_all_wheels', True)])
        assert result.successful
        assert node._pending_zero == {0, 1, 2, 3}


class TestWheelOrder:

    def test_wheel_order_is_fr_br_fl_bl(self):
        assert WHEEL_ORDER == ['FR', 'BR', 'FL', 'BL']
