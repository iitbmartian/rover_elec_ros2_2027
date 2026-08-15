// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from can_interfaces:msg/MobilitySensorData.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/mobility_sensor_data.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__TRAITS_HPP_
#define CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "can_interfaces/msg/detail/mobility_sensor_data__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace can_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const MobilitySensorData & msg,
  std::ostream & out)
{
  out << "{";
  // member: explicit_mag_fl
  {
    out << "explicit_mag_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_fl, out);
    out << ", ";
  }

  // member: explicit_quad_fl
  {
    out << "explicit_quad_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_fl, out);
    out << ", ";
  }

  // member: explicit_imu_fl
  {
    out << "explicit_imu_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_fl, out);
    out << ", ";
  }

  // member: drive_quad_fl
  {
    out << "drive_quad_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_fl, out);
    out << ", ";
  }

  // member: explicit_mag_fr
  {
    out << "explicit_mag_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_fr, out);
    out << ", ";
  }

  // member: explicit_quad_fr
  {
    out << "explicit_quad_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_fr, out);
    out << ", ";
  }

  // member: explicit_imu_fr
  {
    out << "explicit_imu_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_fr, out);
    out << ", ";
  }

  // member: drive_quad_fr
  {
    out << "drive_quad_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_fr, out);
    out << ", ";
  }

  // member: explicit_mag_bl
  {
    out << "explicit_mag_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_bl, out);
    out << ", ";
  }

  // member: explicit_quad_bl
  {
    out << "explicit_quad_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_bl, out);
    out << ", ";
  }

  // member: explicit_imu_bl
  {
    out << "explicit_imu_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_bl, out);
    out << ", ";
  }

  // member: drive_quad_bl
  {
    out << "drive_quad_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_bl, out);
    out << ", ";
  }

  // member: explicit_mag_br
  {
    out << "explicit_mag_br: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_br, out);
    out << ", ";
  }

  // member: explicit_quad_br
  {
    out << "explicit_quad_br: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_br, out);
    out << ", ";
  }

  // member: explicit_imu_br
  {
    out << "explicit_imu_br: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_br, out);
    out << ", ";
  }

  // member: drive_quad_br
  {
    out << "drive_quad_br: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_br, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MobilitySensorData & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: explicit_mag_fl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_mag_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_fl, out);
    out << "\n";
  }

  // member: explicit_quad_fl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_quad_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_fl, out);
    out << "\n";
  }

  // member: explicit_imu_fl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_imu_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_fl, out);
    out << "\n";
  }

  // member: drive_quad_fl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "drive_quad_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_fl, out);
    out << "\n";
  }

  // member: explicit_mag_fr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_mag_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_fr, out);
    out << "\n";
  }

  // member: explicit_quad_fr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_quad_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_fr, out);
    out << "\n";
  }

  // member: explicit_imu_fr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_imu_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_fr, out);
    out << "\n";
  }

  // member: drive_quad_fr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "drive_quad_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_fr, out);
    out << "\n";
  }

  // member: explicit_mag_bl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_mag_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_bl, out);
    out << "\n";
  }

  // member: explicit_quad_bl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_quad_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_bl, out);
    out << "\n";
  }

  // member: explicit_imu_bl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_imu_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_bl, out);
    out << "\n";
  }

  // member: drive_quad_bl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "drive_quad_bl: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_bl, out);
    out << "\n";
  }

  // member: explicit_mag_br
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_mag_br: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_mag_br, out);
    out << "\n";
  }

  // member: explicit_quad_br
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_quad_br: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_quad_br, out);
    out << "\n";
  }

  // member: explicit_imu_br
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "explicit_imu_br: ";
    rosidl_generator_traits::value_to_yaml(msg.explicit_imu_br, out);
    out << "\n";
  }

  // member: drive_quad_br
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "drive_quad_br: ";
    rosidl_generator_traits::value_to_yaml(msg.drive_quad_br, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MobilitySensorData & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace can_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use can_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const can_interfaces::msg::MobilitySensorData & msg,
  std::ostream & out, size_t indentation = 0)
{
  can_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use can_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const can_interfaces::msg::MobilitySensorData & msg)
{
  return can_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<can_interfaces::msg::MobilitySensorData>()
{
  return "can_interfaces::msg::MobilitySensorData";
}

template<>
inline const char * name<can_interfaces::msg::MobilitySensorData>()
{
  return "can_interfaces/msg/MobilitySensorData";
}

template<>
struct has_fixed_size<can_interfaces::msg::MobilitySensorData>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<can_interfaces::msg::MobilitySensorData>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<can_interfaces::msg::MobilitySensorData>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__TRAITS_HPP_
