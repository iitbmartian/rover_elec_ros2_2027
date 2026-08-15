# generated from rosidl_generator_py/resource/_idl.py.em
# with input from can_interfaces:msg/MobilitySensorData.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MobilitySensorData(type):
    """Metaclass of message 'MobilitySensorData'."""

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
                'can_interfaces.msg.MobilitySensorData')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__mobility_sensor_data
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__mobility_sensor_data
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__mobility_sensor_data
            cls._TYPE_SUPPORT = module.type_support_msg__msg__mobility_sensor_data
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__mobility_sensor_data

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MobilitySensorData(metaclass=Metaclass_MobilitySensorData):
    """Message class 'MobilitySensorData'."""

    __slots__ = [
        '_explicit_mag_fl',
        '_explicit_quad_fl',
        '_explicit_imu_fl',
        '_drive_quad_fl',
        '_explicit_mag_fr',
        '_explicit_quad_fr',
        '_explicit_imu_fr',
        '_drive_quad_fr',
        '_explicit_mag_bl',
        '_explicit_quad_bl',
        '_explicit_imu_bl',
        '_drive_quad_bl',
        '_explicit_mag_br',
        '_explicit_quad_br',
        '_explicit_imu_br',
        '_drive_quad_br',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'explicit_mag_fl': 'int32',
        'explicit_quad_fl': 'int32',
        'explicit_imu_fl': 'int32',
        'drive_quad_fl': 'int32',
        'explicit_mag_fr': 'int32',
        'explicit_quad_fr': 'int32',
        'explicit_imu_fr': 'int32',
        'drive_quad_fr': 'int32',
        'explicit_mag_bl': 'int32',
        'explicit_quad_bl': 'int32',
        'explicit_imu_bl': 'int32',
        'drive_quad_bl': 'int32',
        'explicit_mag_br': 'int32',
        'explicit_quad_br': 'int32',
        'explicit_imu_br': 'int32',
        'drive_quad_br': 'int32',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
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
        self.explicit_mag_fl = kwargs.get('explicit_mag_fl', int())
        self.explicit_quad_fl = kwargs.get('explicit_quad_fl', int())
        self.explicit_imu_fl = kwargs.get('explicit_imu_fl', int())
        self.drive_quad_fl = kwargs.get('drive_quad_fl', int())
        self.explicit_mag_fr = kwargs.get('explicit_mag_fr', int())
        self.explicit_quad_fr = kwargs.get('explicit_quad_fr', int())
        self.explicit_imu_fr = kwargs.get('explicit_imu_fr', int())
        self.drive_quad_fr = kwargs.get('drive_quad_fr', int())
        self.explicit_mag_bl = kwargs.get('explicit_mag_bl', int())
        self.explicit_quad_bl = kwargs.get('explicit_quad_bl', int())
        self.explicit_imu_bl = kwargs.get('explicit_imu_bl', int())
        self.drive_quad_bl = kwargs.get('drive_quad_bl', int())
        self.explicit_mag_br = kwargs.get('explicit_mag_br', int())
        self.explicit_quad_br = kwargs.get('explicit_quad_br', int())
        self.explicit_imu_br = kwargs.get('explicit_imu_br', int())
        self.drive_quad_br = kwargs.get('drive_quad_br', int())

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
        if self.explicit_mag_fl != other.explicit_mag_fl:
            return False
        if self.explicit_quad_fl != other.explicit_quad_fl:
            return False
        if self.explicit_imu_fl != other.explicit_imu_fl:
            return False
        if self.drive_quad_fl != other.drive_quad_fl:
            return False
        if self.explicit_mag_fr != other.explicit_mag_fr:
            return False
        if self.explicit_quad_fr != other.explicit_quad_fr:
            return False
        if self.explicit_imu_fr != other.explicit_imu_fr:
            return False
        if self.drive_quad_fr != other.drive_quad_fr:
            return False
        if self.explicit_mag_bl != other.explicit_mag_bl:
            return False
        if self.explicit_quad_bl != other.explicit_quad_bl:
            return False
        if self.explicit_imu_bl != other.explicit_imu_bl:
            return False
        if self.drive_quad_bl != other.drive_quad_bl:
            return False
        if self.explicit_mag_br != other.explicit_mag_br:
            return False
        if self.explicit_quad_br != other.explicit_quad_br:
            return False
        if self.explicit_imu_br != other.explicit_imu_br:
            return False
        if self.drive_quad_br != other.drive_quad_br:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def explicit_mag_fl(self):
        """Message field 'explicit_mag_fl'."""
        return self._explicit_mag_fl

    @explicit_mag_fl.setter
    def explicit_mag_fl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_mag_fl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_mag_fl' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_mag_fl = value

    @builtins.property
    def explicit_quad_fl(self):
        """Message field 'explicit_quad_fl'."""
        return self._explicit_quad_fl

    @explicit_quad_fl.setter
    def explicit_quad_fl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_quad_fl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_quad_fl' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_quad_fl = value

    @builtins.property
    def explicit_imu_fl(self):
        """Message field 'explicit_imu_fl'."""
        return self._explicit_imu_fl

    @explicit_imu_fl.setter
    def explicit_imu_fl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_imu_fl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_imu_fl' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_imu_fl = value

    @builtins.property
    def drive_quad_fl(self):
        """Message field 'drive_quad_fl'."""
        return self._drive_quad_fl

    @drive_quad_fl.setter
    def drive_quad_fl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'drive_quad_fl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'drive_quad_fl' field must be an integer in [-2147483648, 2147483647]"
        self._drive_quad_fl = value

    @builtins.property
    def explicit_mag_fr(self):
        """Message field 'explicit_mag_fr'."""
        return self._explicit_mag_fr

    @explicit_mag_fr.setter
    def explicit_mag_fr(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_mag_fr' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_mag_fr' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_mag_fr = value

    @builtins.property
    def explicit_quad_fr(self):
        """Message field 'explicit_quad_fr'."""
        return self._explicit_quad_fr

    @explicit_quad_fr.setter
    def explicit_quad_fr(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_quad_fr' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_quad_fr' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_quad_fr = value

    @builtins.property
    def explicit_imu_fr(self):
        """Message field 'explicit_imu_fr'."""
        return self._explicit_imu_fr

    @explicit_imu_fr.setter
    def explicit_imu_fr(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_imu_fr' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_imu_fr' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_imu_fr = value

    @builtins.property
    def drive_quad_fr(self):
        """Message field 'drive_quad_fr'."""
        return self._drive_quad_fr

    @drive_quad_fr.setter
    def drive_quad_fr(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'drive_quad_fr' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'drive_quad_fr' field must be an integer in [-2147483648, 2147483647]"
        self._drive_quad_fr = value

    @builtins.property
    def explicit_mag_bl(self):
        """Message field 'explicit_mag_bl'."""
        return self._explicit_mag_bl

    @explicit_mag_bl.setter
    def explicit_mag_bl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_mag_bl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_mag_bl' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_mag_bl = value

    @builtins.property
    def explicit_quad_bl(self):
        """Message field 'explicit_quad_bl'."""
        return self._explicit_quad_bl

    @explicit_quad_bl.setter
    def explicit_quad_bl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_quad_bl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_quad_bl' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_quad_bl = value

    @builtins.property
    def explicit_imu_bl(self):
        """Message field 'explicit_imu_bl'."""
        return self._explicit_imu_bl

    @explicit_imu_bl.setter
    def explicit_imu_bl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_imu_bl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_imu_bl' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_imu_bl = value

    @builtins.property
    def drive_quad_bl(self):
        """Message field 'drive_quad_bl'."""
        return self._drive_quad_bl

    @drive_quad_bl.setter
    def drive_quad_bl(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'drive_quad_bl' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'drive_quad_bl' field must be an integer in [-2147483648, 2147483647]"
        self._drive_quad_bl = value

    @builtins.property
    def explicit_mag_br(self):
        """Message field 'explicit_mag_br'."""
        return self._explicit_mag_br

    @explicit_mag_br.setter
    def explicit_mag_br(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_mag_br' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_mag_br' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_mag_br = value

    @builtins.property
    def explicit_quad_br(self):
        """Message field 'explicit_quad_br'."""
        return self._explicit_quad_br

    @explicit_quad_br.setter
    def explicit_quad_br(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_quad_br' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_quad_br' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_quad_br = value

    @builtins.property
    def explicit_imu_br(self):
        """Message field 'explicit_imu_br'."""
        return self._explicit_imu_br

    @explicit_imu_br.setter
    def explicit_imu_br(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'explicit_imu_br' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'explicit_imu_br' field must be an integer in [-2147483648, 2147483647]"
        self._explicit_imu_br = value

    @builtins.property
    def drive_quad_br(self):
        """Message field 'drive_quad_br'."""
        return self._drive_quad_br

    @drive_quad_br.setter
    def drive_quad_br(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'drive_quad_br' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'drive_quad_br' field must be an integer in [-2147483648, 2147483647]"
        self._drive_quad_br = value
