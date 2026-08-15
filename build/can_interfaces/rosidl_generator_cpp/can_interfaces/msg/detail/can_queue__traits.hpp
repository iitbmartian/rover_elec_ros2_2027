// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from can_interfaces:msg/CANQueue.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/can_queue.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__TRAITS_HPP_
#define CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "can_interfaces/msg/detail/can_queue__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace can_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CANQueue & msg,
  std::ostream & out)
{
  out << "{";
  // member: arb_id
  {
    out << "arb_id: ";
    rosidl_generator_traits::value_to_yaml(msg.arb_id, out);
    out << ", ";
  }

  // member: data
  {
    if (msg.data.size() == 0) {
      out << "data: []";
    } else {
      out << "data: [";
      size_t pending_items = msg.data.size();
      for (auto item : msg.data) {
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
  const CANQueue & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: arb_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "arb_id: ";
    rosidl_generator_traits::value_to_yaml(msg.arb_id, out);
    out << "\n";
  }

  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.data.size() == 0) {
      out << "data: []\n";
    } else {
      out << "data:\n";
      for (auto item : msg.data) {
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

inline std::string to_yaml(const CANQueue & msg, bool use_flow_style = false)
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
  const can_interfaces::msg::CANQueue & msg,
  std::ostream & out, size_t indentation = 0)
{
  can_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use can_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const can_interfaces::msg::CANQueue & msg)
{
  return can_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<can_interfaces::msg::CANQueue>()
{
  return "can_interfaces::msg::CANQueue";
}

template<>
inline const char * name<can_interfaces::msg::CANQueue>()
{
  return "can_interfaces/msg/CANQueue";
}

template<>
struct has_fixed_size<can_interfaces::msg::CANQueue>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<can_interfaces::msg::CANQueue>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<can_interfaces::msg::CANQueue>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__TRAITS_HPP_
