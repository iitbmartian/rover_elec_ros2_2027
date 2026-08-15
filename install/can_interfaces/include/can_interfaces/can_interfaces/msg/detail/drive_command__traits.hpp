// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/drive_command.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__TRAITS_HPP_
#define CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "can_interfaces/msg/detail/drive_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace can_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const DriveCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: drive_direction
  {
    if (msg.drive_direction.size() == 0) {
      out << "drive_direction: []";
    } else {
      out << "drive_direction: [";
      size_t pending_items = msg.drive_direction.size();
      for (auto item : msg.drive_direction) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: drive_pwm
  {
    if (msg.drive_pwm.size() == 0) {
      out << "drive_pwm: []";
    } else {
      out << "drive_pwm: [";
      size_t pending_items = msg.drive_pwm.size();
      for (auto item : msg.drive_pwm) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: explicit_direction
  {
    if (msg.explicit_direction.size() == 0) {
      out << "explicit_direction: []";
    } else {
      out << "explicit_direction: [";
      size_t pending_items = msg.explicit_direction.size();
      for (auto item : msg.explicit_direction) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: explicit_pwm
  {
    if (msg.explicit_pwm.size() == 0) {
      out << "explicit_pwm: []";
    } else {
      out << "explicit_pwm: [";
      size_t pending_items = msg.explicit_pwm.size();
      for (auto item : msg.explicit_pwm) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DriveCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: drive_direction
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.drive_direction.size() == 0) {
      out << "drive_direction: []\n";
    } else {
      out << "drive_direction:\n";
      for (auto item : msg.drive_direction) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: drive_pwm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.drive_pwm.size() == 0) {
      out << "drive_pwm: []\n";
    } else {
      out << "drive_pwm:\n";
      for (auto item : msg.drive_pwm) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: explicit_direction
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.explicit_direction.size() == 0) {
      out << "explicit_direction: []\n";
    } else {
      out << "explicit_direction:\n";
      for (auto item : msg.explicit_direction) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: explicit_pwm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.explicit_pwm.size() == 0) {
      out << "explicit_pwm: []\n";
    } else {
      out << "explicit_pwm:\n";
      for (auto item : msg.explicit_pwm) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DriveCommand & msg, bool use_flow_style = false)
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
  const can_interfaces::msg::DriveCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  can_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use can_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const can_interfaces::msg::DriveCommand & msg)
{
  return can_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<can_interfaces::msg::DriveCommand>()
{
  return "can_interfaces::msg::DriveCommand";
}

template<>
inline const char * name<can_interfaces::msg::DriveCommand>()
{
  return "can_interfaces/msg/DriveCommand";
}

template<>
struct has_fixed_size<can_interfaces::msg::DriveCommand>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<can_interfaces::msg::DriveCommand>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<can_interfaces::msg::DriveCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__TRAITS_HPP_
