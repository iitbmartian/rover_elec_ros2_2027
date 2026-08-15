# generated from rosidl_generator_py/resource/_idl.py.em
# with input from can_interfaces:msg/DriveCommand.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

# Member 'drive_pwm'
# Member 'explicit_pwm'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_DriveCommand(type):
    """Metaclass of message 'DriveCommand'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('can_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'can_interfaces.msg.DriveCommand')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__drive_command
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__drive_command
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__drive_command
            cls._TYPE_SUPPORT = module.type_support_msg__msg__drive_command
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__drive_command

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class DriveCommand(metaclass=Metaclass_DriveCommand):
    """Message class 'DriveCommand'."""

    __slots__ = [
        '_drive_direction',
        '_drive_pwm',
        '_explicit_direction',
        '_explicit_pwm',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'drive_direction': 'sequence<boolean>',
        'drive_pwm': 'sequence<int32>',
        'explicit_direction': 'sequence<boolean>',
        'explicit_pwm': 'sequence<int32>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('boolean')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('int32')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('boolean')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('int32')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.drive_direction = kwargs.get('drive_direction', [])
        self.drive_pwm = array.array('i', kwargs.get('drive_pwm', []))
        self.explicit_direction = kwargs.get('explicit_direction', [])
        self.explicit_pwm = array.array('i', kwargs.get('explicit_pwm', []))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.drive_direction != other.drive_direction:
            return False
        if self.drive_pwm != other.drive_pwm:
            return False
        if self.explicit_direction != other.explicit_direction:
            return False
        if self.explicit_pwm != other.explicit_pwm:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def drive_direction(self):
        """Message field 'drive_direction'."""
        return self._drive_direction

    @drive_direction.setter
    def drive_direction(self, value):
        if self._check_fields:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, bool) for v in value) and
                 True), \
                "The 'drive_direction' field must be a set or sequence and each value of type 'bool'"
        self._drive_direction = value

    @builtins.property
    def drive_pwm(self):
        """Message field 'drive_pwm'."""
        return self._drive_pwm

    @drive_pwm.setter
    def drive_pwm(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'i', \
                    "The 'drive_pwm' array.array() must have the type code of 'i'"
                self._drive_pwm = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= -2147483648 and val < 2147483648 for val in value)), \
                "The 'drive_pwm' field must be a set or sequence and each value of type 'int' and each integer in [-2147483648, 2147483647]"
        self._drive_pwm = array.array('i', value)

    @builtins.property
    def explicit_direction(self):
        """Message field 'explicit_direction'."""
        return self._explicit_direction

    @explicit_direction.setter
    def explicit_direction(self, value):
        if self._check_fields:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, bool) for v in value) and
                 True), \
                "The 'explicit_direction' field must be a set or sequence and each value of type 'bool'"
        self._explicit_direction = value

    @builtins.property
    def explicit_pwm(self):
        """Message field 'explicit_pwm'."""
        return self._explicit_pwm

    @explicit_pwm.setter
    def explicit_pwm(self, value):
        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'i', \
                    "The 'explicit_pwm' array.array() must have the type code of 'i'"
                self._explicit_pwm = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= -2147483648 and val < 2147483648 for val in value)), \
                "The 'explicit_pwm' field must be a set or sequence and each value of type 'int' and each integer in [-2147483648, 2147483647]"
        self._explicit_pwm = array.array('i', value)
