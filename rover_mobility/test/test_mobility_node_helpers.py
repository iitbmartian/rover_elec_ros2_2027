"""
Stress tests for the pure-Python helpers on rover_mobility.mobility_node.

NOT a live-node/rclpy integration test (see rover_mobility_review/runtime/
for that). Import of the module itself only succeeds because of the
conftest.py shim patching can_interfaces.msg.DriveCommand in memory - that
shim's existence is itself evidence of bug #1 (see
rover_mobility_review/rover_mobility_review.md).
"""
import time
from types import SimpleNamespace

from can_interfaces.msg import EncoderDataFL, MobilityData
import numpy as np
import pytest

from rover_mobility.controllers.vroomvroom import VroomVroom
from rover_mobility.mobility_node import MobilityNode, MSG_TYPES, WHEEL_ORDER


class TestWheelOrderAndMsgTypes:

    def test_wheel_order_is_fr_br_fl_bl(self):
        assert WHEEL_ORDER == ['FR', 'BR', 'FL', 'BL']

    def test_wheel_order_matches_actual_vroomvroom_geometry(self):
        """
        Cross-checks WHEEL_ORDER against VroomVroom.from_R_vec's fixed w1..w4 geometric.

        pattern directly (a=half_width=right, b=half_length=forward), rather than
        trusting the inline comment - see
        TestFromRVec.test_wheel_at_icr_has_zero_required_velocity in test_vroomvroom.py
        for the underlying technique.
        """
        vroom = VroomVroom(half_width=0.35, half_length=0.45)
        a, b = vroom.a, vroom.b
        expected_name_for_corner = {
            (a, b): 'FR',
            (a, -b): 'BR',
            (-a, b): 'FL',
            (-a, -b): 'BL',
        }
        corners_in_index_order = [(a, b), (a, -b), (-a, b), (-a, -b)]
        for i, corner in enumerate(corners_in_index_order):
            assert WHEEL_ORDER[i] == expected_name_for_corner[corner]

    def test_all_four_per_wheel_msg_types_now_import_successfully(self):
        """
        EncoderDataFL/FR/BL/BR now exist in can_interfaces.msg (added alongside.

        MobilityData.msg, one message type per wheel per the mobility_node.py
        module docstring), so the CAN subscription loop now actually
        subscribes for all 4 wheels - this used to be all-None (see
        rover_mobility_review/rover_mobility_review.md bug #3) when the
        per-wheel types didn't exist yet. Confirmed here offline, without
        needing a live node.
        """
        from can_interfaces.msg import EncoderDataFL, EncoderDataFR, EncoderDataBL, EncoderDataBR
        assert MSG_TYPES == {
            'FL': EncoderDataFL, 'FR': EncoderDataFR,
            'BL': EncoderDataBL, 'BR': EncoderDataBR,
        }


class TestFormatMagneticAngle:

    @pytest.mark.parametrize('raw_angle,offset,expected', [
        (190.0, 10.0, 180.0),
        (200.0, 10.0, -170.0),
        (-190.0, 10.0, 160.0),
        (0.0, 0.0, 0.0),
    ])
    def test_wraps_into_plus_minus_180(self, raw_angle, offset, expected):
        fake_self = SimpleNamespace(mag_offsets=[offset, 0.0, 0.0, 0.0])
        result = MobilityNode.format_magnetic_angle(fake_self, raw_angle, 0)
        assert result == pytest.approx(expected)

    def test_linear_wrap_loop_stalls_on_a_glitched_reading(self):
        """
        Wrap loop is linear, not O(1) - a glitched reading stalls it.

        format_magnetic_angle wraps with `while real_angle > 180:
        real_angle -= 360` instead of modulo arithmetic (contrast with
        explicit_steer.py's wrap_count()/wrap_count_diff(), which use `%`
        and are O(1) regardless of magnitude). explicit_mag_* is a plain
        int32 field (MobilityData.msg), so a single corrupted/glitched CAN
        byte can produce a huge value - this reproduces that offline and
        proves the O(n) cost live-confirmed to stall the real control loop
        for several seconds in rover_mobility_review/runtime/runtime_log.md.
        """
        fake_self = SimpleNamespace(mag_offsets=[0.0, 0.0, 0.0, 0.0])
        start = time.perf_counter()
        result = MobilityNode.format_magnetic_angle(fake_self, 2_000_000_000.0, 0)
        elapsed = time.perf_counter() - start
        assert -180.0 <= result <= 180.0
        assert elapsed > 0.05, (
            'expected the linear wrap loop to take a real, measurable amount of time '
            'for a glitch-sized input - if this now runs fast, the wrap was likely '
            'switched to O(1) modulo arithmetic and this test should be updated/removed'
        )


class TestGetField:

    def test_matches_real_suffixed_field_name(self):
        msg = MobilityData()
        msg.explicit_mag_fl = 123
        assert MobilityNode._get_field(msg, 'explicit_mag', 'fl') == 123

    def test_returns_none_when_field_absent(self):
        msg = MobilityData()
        assert MobilityNode._get_field(msg, 'totally_made_up_field', 'fl') is None

    def test_field_matching_would_work_for_every_wheel_and_signal(self):
        """
        Proves _get_field's candidate-spelling logic is NOT the reason telemetry never.

        arrives (bug #3 - the missing subscription - is the sole blocker): every real
        field name on the actual built MobilityData message matches on the first
        candidate spelling.
        """
        msg = MobilityData()
        for suf in ('fl', 'fr', 'bl', 'br'):
            for base in ('explicit_mag', 'explicit_quad', 'explicit_imu', 'drive_quad'):
                field_name = f'{base}_{suf}'
                setattr(msg, field_name, 7)
                assert MobilityNode._get_field(msg, base, suf) == 7
                setattr(msg, field_name, 0)


class TestToPwmBytes:

    @pytest.mark.parametrize('pwm,expected', [
        (1.0, [1, 127]),
        (-1.0, [0, 127]),
        (0.0, [0, 0]),
        (2.0, [1, 127]),   # out-of-range input still clamps cleanly
        (-2.0, [0, 127]),
    ])
    def test_clamps_and_splits_sign_magnitude(self, pwm, expected):
        assert MobilityNode._to_pwm_bytes(pwm) == expected


class TestDriveCommandSchemaMismatch:

    def test_all_interfaces_drive_command_is_not_actually_built(self):
        """
        all_interfaces/CMakeLists.txt's rosidl_generate_interfaces() call only lists.

        TelemetryData.msg / PidCommands.msg / PidGains.msg - DriveCommand.msg is never
        passed to codegen at all, despite the .msg file existing on disk. So even
        correcting mobility_node.py's import to read `from all_interfaces.msg import
        DriveCommand` would still fail with ImportError - this is a second, independent
        root cause from the wrong-package import (bug #1).
        """
        with pytest.raises(ImportError):
            from all_interfaces.msg import DriveCommand  # noqa: F401

    def test_mobility_node_field_names_do_not_match_real_drive_command_schema(self):
        """
        mobility_node.py's loop() (lines 453-456) does.

        `drive_command_msg.drive_direction.append(...)`, `.drive_pwm.append(...)`,
        `.explicit_direction.append(...)`, `.explicit_pwm.append(...)`. Reconstructed
        here from all_interfaces/msg/DriveCommand.msg's DECLARED source (since it is
        never actually rosidl-built - see test above): the real schema is just `pwm:
        int64[]` and `direction: int64[]`. None of the four names the node writes exist
        on it.
        """

        class RealShapedDriveCommand:

            def __init__(self):
                self.pwm = []
                self.direction = []

        dc = RealShapedDriveCommand()
        with pytest.raises(AttributeError):
            dc.drive_direction.append(True)


class _FakeLogger:

    def warn(self, msg):
        pass

    def info(self, msg):
        pass


class _FakeSteerCtl:

    def __init__(self):
        self.x = np.array([42.0, 3.0])
        self.P = np.eye(2) * 99.0


def _make_fake_node():
    node = SimpleNamespace()
    node.mag_offsets = [0.0, 0.0, 0.0, 0.0]
    node.quad_offsets = [0.0, 0.0, 0.0, 0.0]
    node.steer_input_flip = [False, False, False, False]
    node._latest_raw_mag = [None, None, None, None]
    node._latest_raw_quad = [None, None, None, None]
    node._latest_steer_z = [None, None, None, None]
    node._new_steer_data = [False, False, False, False]
    node._latest_drive_quad = [None, None, None, None]
    node._latest_sensor_check = [[1, 1] for _ in range(4)]
    node._latest_limit_switch = [[0, 0] for _ in range(4)]
    node._logged_msg_fields = set()
    node._tick = 0
    node.steer_ctls = [_FakeSteerCtl() for _ in range(4)]
    node.get_logger = lambda: _FakeLogger()
    node._pending_zero = set()
    node.limit_switch_calls = []
    node._on_limit_switch = lambda i: node.limit_switch_calls.append(i)
    # can_receive() calls self.format_magnetic_angle()/self._get_field() -
    # bind the REAL implementations so a full can_receive() call can be
    # exercised against this fake node, not just the methods tested
    # elsewhere in isolation.
    node.format_magnetic_angle = (
        lambda angle, i: MobilityNode.format_magnetic_angle(node, angle, i)
    )
    node._get_field = MobilityNode._get_field
    return node


class TestApplyZero:
    """
    Offline tests for the zero_wheel_index/zero_all_wheels calibration feature.

    See mobility_node.py's module docstring and
    _apply_zero()/_on_set_parameters().
    """

    def test_no_telemetry_yet_warns_and_does_not_change_state(self):
        node = _make_fake_node()
        MobilityNode._apply_zero(node, 0)
        assert node.mag_offsets[0] == 0.0
        assert node.quad_offsets[0] == 0.0
        assert node.steer_ctls[0].x[0] == pytest.approx(42.0)

    def test_zeroes_offsets_and_resets_ekf_state(self):
        node = _make_fake_node()
        node._latest_raw_mag[1] = 57.3
        node._latest_raw_quad[1] = 128.0
        MobilityNode._apply_zero(node, 1)
        assert node.mag_offsets[1] == pytest.approx(57.3)
        assert node.quad_offsets[1] == pytest.approx(128.0)
        assert np.array_equal(node.steer_ctls[1].x, np.zeros(2))
        assert np.array_equal(node.steer_ctls[1].P, np.eye(2))
        # untouched wheels stay untouched
        assert node.mag_offsets[0] == 0.0
        assert node.steer_ctls[0].x[0] == pytest.approx(42.0)

    def test_zero_then_format_magnetic_angle_reads_zero_at_that_position(self):
        """
        End-to-end sanity check of the actual promise the feature makes.

        After zeroing at raw_mag=200.0, format_magnetic_angle(200.0) - the
        same raw reading - now reports 0 degrees.
        """
        node = _make_fake_node()
        node._latest_raw_mag[2] = 200.0
        node._latest_raw_quad[2] = 10.0
        MobilityNode._apply_zero(node, 2)
        assert MobilityNode.format_magnetic_angle(node, 200.0, 2) == pytest.approx(0.0)


class TestOnSetParameters:

    @staticmethod
    def _param(name, value):
        return SimpleNamespace(name=name, value=value)

    @pytest.mark.parametrize('index', [0, 1, 2, 3])
    def test_valid_wheel_index_queues_that_wheel(self, index):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('zero_wheel_index', index)])
        assert result.successful
        assert node._pending_zero == {index}

    def test_neutral_value_queues_nothing(self):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('zero_wheel_index', -1)])
        assert result.successful
        assert node._pending_zero == set()

    @pytest.mark.parametrize('bad_index', [-2, 4, 7, 100])
    def test_out_of_range_index_is_rejected(self, bad_index):
        node = _make_fake_node()
        param = self._param('zero_wheel_index', bad_index)
        result = MobilityNode._on_set_parameters(node, [param])
        assert not result.successful
        assert node._pending_zero == set()

    def test_zero_all_wheels_queues_every_wheel(self):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('zero_all_wheels', True)])
        assert result.successful
        assert node._pending_zero == {0, 1, 2, 3}

    def test_zero_all_wheels_false_queues_nothing(self):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('zero_all_wheels', False)])
        assert result.successful
        assert node._pending_zero == set()

    def test_unrelated_parameter_is_ignored(self):
        node = _make_fake_node()
        result = MobilityNode._on_set_parameters(node, [self._param('dt', 0.02)])
        assert result.successful
        assert node._pending_zero == set()


def _make_encoder_data_fl(
    mag=100, quad=50, imu=5, drive_quad=10, ls=(0, 0), sensor_check=(1, 1),
):
    msg = EncoderDataFL()
    msg.explicit_mag_fl = mag
    msg.explicit_quad_fl = quad
    msg.explicit_imu_fl = imu
    msg.drive_quad_fl = drive_quad
    msg.ls_fl = list(ls)
    msg.sensor_check_fl = list(sensor_check)
    return msg


FL_INDEX = WHEEL_ORDER.index('FL')  # WHEEL_ORDER=['FR','BR','FL','BL'] -> 2, NOT 0


class TestCanReceiveLimitSwitchAndSensorCheck:
    """
    Offline tests for the ls_<suf>/sensor_check_<suf> handling in can_receive().

    See mobility_node.py's module docstring and _on_limit_switch(). Uses
    FL_INDEX (= WHEEL_ORDER.index('FL') = 2), NOT a hardcoded 0, since an
    EncoderDataFL message's fields are suffixed "_fl" and can_receive()
    looks up the suffix from WHEEL_ORDER[i] - calling
    can_receive(node, 0, ...) with an EncoderDataFL message would look for
    "_fr" fields (WHEEL_ORDER[0] is 'FR') that don't exist on it. Caught
    by this test suite itself: the first version of these tests used
    index 0 and every assertion silently failed because can_receive()
    couldn't find any of the expected fields.
    """

    def test_limit_switch_not_triggered_does_not_call_hook(self):
        node = _make_fake_node()
        msg = _make_encoder_data_fl(ls=(0, 0))
        MobilityNode.can_receive(node, FL_INDEX, msg)
        assert node._latest_limit_switch[FL_INDEX] == [0, 0]
        assert node.limit_switch_calls == []

    def test_limit_switch_triggered_calls_hook_with_wheel_index(self):
        node = _make_fake_node()
        msg = _make_encoder_data_fl(ls=(1, 0))
        MobilityNode.can_receive(node, FL_INDEX, msg)
        assert node._latest_limit_switch[FL_INDEX] == [1, 0]
        assert node.limit_switch_calls == [FL_INDEX]

    def test_on_limit_switch_is_a_real_no_op_placeholder(self):
        """
        The real (non-faked) _on_limit_switch() must not raise or change state.

        It's an intentional no-op reserved for future calibration use.
        """
        node = _make_fake_node()
        del node._on_limit_switch  # use the REAL MobilityNode implementation
        result = MobilityNode._on_limit_switch(node, FL_INDEX)
        assert result is None

    def test_sensor_check_both_up_is_stored(self):
        node = _make_fake_node()
        msg = _make_encoder_data_fl(sensor_check=(1, 1))
        MobilityNode.can_receive(node, FL_INDEX, msg)
        assert node._latest_sensor_check[FL_INDEX] == [1, 1]

    def test_sensor_check_mag_down_is_stored(self):
        node = _make_fake_node()
        msg = _make_encoder_data_fl(sensor_check=(0, 1))
        MobilityNode.can_receive(node, FL_INDEX, msg)
        assert node._latest_sensor_check[FL_INDEX] == [0, 1]

    def test_sensor_check_imu_down_is_stored(self):
        node = _make_fake_node()
        msg = _make_encoder_data_fl(sensor_check=(1, 0))
        MobilityNode.can_receive(node, FL_INDEX, msg)
        assert node._latest_sensor_check[FL_INDEX] == [1, 0]

    def test_only_the_targeted_wheel_state_changes(self):
        """can_receive(i=FL_INDEX, ...) must only touch that wheel's state."""
        node = _make_fake_node()
        msg = _make_encoder_data_fl(ls=(1, 1), sensor_check=(0, 0))
        MobilityNode.can_receive(node, FL_INDEX, msg)
        for i in range(4):
            if i == FL_INDEX:
                continue
            assert node._latest_limit_switch[i] == [0, 0]
            assert node._latest_sensor_check[i] == [1, 1]

    def test_normal_telemetry_extraction_still_works_on_new_message_type(self):
        """
        Regression check: the pre-existing mag/quad/imu/drive_quad extraction works.

        Still works now that it's reading from EncoderDataFL instead of
        the old MobilityData.
        """
        node = _make_fake_node()
        msg = _make_encoder_data_fl(mag=12, quad=34, imu=5, drive_quad=99)
        MobilityNode.can_receive(node, FL_INDEX, msg)
        assert node._new_steer_data[FL_INDEX] is True
        assert node._latest_steer_z[FL_INDEX][1] == pytest.approx(34.0)  # quad, offset=0
        assert node._latest_steer_z[FL_INDEX][2] == pytest.approx(5.0)   # imu
        assert node._latest_drive_quad[FL_INDEX] == 99
