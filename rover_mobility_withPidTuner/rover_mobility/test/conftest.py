"""
Test-only shim so rover_mobility.mobility_node can be imported for tests.

The module does an unguarded `from can_interfaces.msg import DriveCommand`
at import time, but `DriveCommand` does not exist in `can_interfaces.msg`
(it's never code-generated there - see the earlier rover_mobility review).
This patches the already-built `can_interfaces.msg` module object in memory
for the duration of the test session, mirroring the shape of the REAL
DriveCommand message (all_interfaces/msg/DriveCommand.msg: `pwm`,
`direction`, both list-typed). It never touches any file on disk and has
no effect on the ament_flake8/ament_pep257/ament_copyright tests, which do
static/AST analysis rather than importing the module under test.
"""
import can_interfaces.msg as _can_msg


class _StubDriveCommand:
    """Mirrors all_interfaces/msg/DriveCommand.msg's real shape."""

    def __init__(self):
        self.pwm = []
        self.direction = []


if not hasattr(_can_msg, 'DriveCommand'):
    _can_msg.DriveCommand = _StubDriveCommand
