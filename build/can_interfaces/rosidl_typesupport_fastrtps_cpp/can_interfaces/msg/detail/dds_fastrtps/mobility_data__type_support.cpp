// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from can_interfaces:msg/MobilityData.idl
// generated code does not contain a copyright notice
#include "can_interfaces/msg/detail/mobility_data__rosidl_typesupport_fastrtps_cpp.hpp"
#include "can_interfaces/msg/detail/mobility_data__functions.h"
#include "can_interfaces/msg/detail/mobility_data__struct.hpp"

#include <cstddef>
#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace can_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{


bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_can_interfaces
cdr_serialize(
  const can_interfaces::msg::MobilityData & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: explicit_mag_fl
  cdr << ros_message.explicit_mag_fl;

  // Member: explicit_quad_fl
  cdr << ros_message.explicit_quad_fl;

  // Member: explicit_imu_fl
  cdr << ros_message.explicit_imu_fl;

  // Member: drive_quad_fl
  cdr << ros_message.drive_quad_fl;

  // Member: explicit_mag_fr
  cdr << ros_message.explicit_mag_fr;

  // Member: explicit_quad_fr
  cdr << ros_message.explicit_quad_fr;

  // Member: explicit_imu_fr
  cdr << ros_message.explicit_imu_fr;

  // Member: drive_quad_fr
  cdr << ros_message.drive_quad_fr;

  // Member: explicit_mag_bl
  cdr << ros_message.explicit_mag_bl;

  // Member: explicit_quad_bl
  cdr << ros_message.explicit_quad_bl;

  // Member: explicit_imu_bl
  cdr << ros_message.explicit_imu_bl;

  // Member: drive_quad_bl
  cdr << ros_message.drive_quad_bl;

  // Member: explicit_mag_br
  cdr << ros_message.explicit_mag_br;

  // Member: explicit_quad_br
  cdr << ros_message.explicit_quad_br;

  // Member: explicit_imu_br
  cdr << ros_message.explicit_imu_br;

  // Member: drive_quad_br
  cdr << ros_message.drive_quad_br;

  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_can_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  can_interfaces::msg::MobilityData & ros_message)
{
  // Member: explicit_mag_fl
  cdr >> ros_message.explicit_mag_fl;

  // Member: explicit_quad_fl
  cdr >> ros_message.explicit_quad_fl;

  // Member: explicit_imu_fl
  cdr >> ros_message.explicit_imu_fl;

  // Member: drive_quad_fl
  cdr >> ros_message.drive_quad_fl;

  // Member: explicit_mag_fr
  cdr >> ros_message.explicit_mag_fr;

  // Member: explicit_quad_fr
  cdr >> ros_message.explicit_quad_fr;

  // Member: explicit_imu_fr
  cdr >> ros_message.explicit_imu_fr;

  // Member: drive_quad_fr
  cdr >> ros_message.drive_quad_fr;

  // Member: explicit_mag_bl
  cdr >> ros_message.explicit_mag_bl;

  // Member: explicit_quad_bl
  cdr >> ros_message.explicit_quad_bl;

  // Member: explicit_imu_bl
  cdr >> ros_message.explicit_imu_bl;

  // Member: drive_quad_bl
  cdr >> ros_message.drive_quad_bl;

  // Member: explicit_mag_br
  cdr >> ros_message.explicit_mag_br;

  // Member: explicit_quad_br
  cdr >> ros_message.explicit_quad_br;

  // Member: explicit_imu_br
  cdr >> ros_message.explicit_imu_br;

  // Member: drive_quad_br
  cdr >> ros_message.drive_quad_br;

  return true;
}  // NOLINT(readability/fn_size)


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_can_interfaces
get_serialized_size(
  const can_interfaces::msg::MobilityData & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: explicit_mag_fl
  {
    size_t item_size = sizeof(ros_message.explicit_mag_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_fl
  {
    size_t item_size = sizeof(ros_message.explicit_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_fl
  {
    size_t item_size = sizeof(ros_message.explicit_imu_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_fl
  {
    size_t item_size = sizeof(ros_message.drive_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_mag_fr
  {
    size_t item_size = sizeof(ros_message.explicit_mag_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_fr
  {
    size_t item_size = sizeof(ros_message.explicit_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_fr
  {
    size_t item_size = sizeof(ros_message.explicit_imu_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_fr
  {
    size_t item_size = sizeof(ros_message.drive_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_mag_bl
  {
    size_t item_size = sizeof(ros_message.explicit_mag_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_bl
  {
    size_t item_size = sizeof(ros_message.explicit_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_bl
  {
    size_t item_size = sizeof(ros_message.explicit_imu_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_bl
  {
    size_t item_size = sizeof(ros_message.drive_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_mag_br
  {
    size_t item_size = sizeof(ros_message.explicit_mag_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_br
  {
    size_t item_size = sizeof(ros_message.explicit_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_br
  {
    size_t item_size = sizeof(ros_message.explicit_imu_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_br
  {
    size_t item_size = sizeof(ros_message.drive_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_can_interfaces
max_serialized_size_MobilityData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Member: explicit_mag_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_imu_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: drive_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_mag_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_imu_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: drive_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_mag_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_imu_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: drive_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_mag_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_quad_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: explicit_imu_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // Member: drive_quad_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = can_interfaces::msg::MobilityData;
    is_plain =
      (
      offsetof(DataType, drive_quad_br) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_can_interfaces
cdr_serialize_key(
  const can_interfaces::msg::MobilityData & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: explicit_mag_fl
  cdr << ros_message.explicit_mag_fl;

  // Member: explicit_quad_fl
  cdr << ros_message.explicit_quad_fl;

  // Member: explicit_imu_fl
  cdr << ros_message.explicit_imu_fl;

  // Member: drive_quad_fl
  cdr << ros_message.drive_quad_fl;

  // Member: explicit_mag_fr
  cdr << ros_message.explicit_mag_fr;

  // Member: explicit_quad_fr
  cdr << ros_message.explicit_quad_fr;

  // Member: explicit_imu_fr
  cdr << ros_message.explicit_imu_fr;

  // Member: drive_quad_fr
  cdr << ros_message.drive_quad_fr;

  // Member: explicit_mag_bl
  cdr << ros_message.explicit_mag_bl;

  // Member: explicit_quad_bl
  cdr << ros_message.explicit_quad_bl;

  // Member: explicit_imu_bl
  cdr << ros_message.explicit_imu_bl;

  // Member: drive_quad_bl
  cdr << ros_message.drive_quad_bl;

  // Member: explicit_mag_br
  cdr << ros_message.explicit_mag_br;

  // Member: explicit_quad_br
  cdr << ros_message.explicit_quad_br;

  // Member: explicit_imu_br
  cdr << ros_message.explicit_imu_br;

  // Member: drive_quad_br
  cdr << ros_message.drive_quad_br;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_can_interfaces
get_serialized_size_key(
  const can_interfaces::msg::MobilityData & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: explicit_mag_fl
  {
    size_t item_size = sizeof(ros_message.explicit_mag_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_fl
  {
    size_t item_size = sizeof(ros_message.explicit_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_fl
  {
    size_t item_size = sizeof(ros_message.explicit_imu_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_fl
  {
    size_t item_size = sizeof(ros_message.drive_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_mag_fr
  {
    size_t item_size = sizeof(ros_message.explicit_mag_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_fr
  {
    size_t item_size = sizeof(ros_message.explicit_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_fr
  {
    size_t item_size = sizeof(ros_message.explicit_imu_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_fr
  {
    size_t item_size = sizeof(ros_message.drive_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_mag_bl
  {
    size_t item_size = sizeof(ros_message.explicit_mag_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_bl
  {
    size_t item_size = sizeof(ros_message.explicit_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_bl
  {
    size_t item_size = sizeof(ros_message.explicit_imu_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_bl
  {
    size_t item_size = sizeof(ros_message.drive_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_mag_br
  {
    size_t item_size = sizeof(ros_message.explicit_mag_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_quad_br
  {
    size_t item_size = sizeof(ros_message.explicit_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: explicit_imu_br
  {
    size_t item_size = sizeof(ros_message.explicit_imu_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: drive_quad_br
  {
    size_t item_size = sizeof(ros_message.drive_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_can_interfaces
max_serialized_size_key_MobilityData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Member: explicit_mag_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_imu_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: drive_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_mag_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_imu_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: drive_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_mag_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_imu_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: drive_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_mag_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_quad_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: explicit_imu_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: drive_quad_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = can_interfaces::msg::MobilityData;
    is_plain =
      (
      offsetof(DataType, drive_quad_br) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}


static bool _MobilityData__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const can_interfaces::msg::MobilityData *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _MobilityData__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<can_interfaces::msg::MobilityData *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _MobilityData__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const can_interfaces::msg::MobilityData *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _MobilityData__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_MobilityData(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _MobilityData__callbacks = {
  "can_interfaces::msg",
  "MobilityData",
  _MobilityData__cdr_serialize,
  _MobilityData__cdr_deserialize,
  _MobilityData__get_serialized_size,
  _MobilityData__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _MobilityData__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_MobilityData__callbacks,
  get_message_typesupport_handle_function,
  &can_interfaces__msg__MobilityData__get_type_hash,
  &can_interfaces__msg__MobilityData__get_type_description,
  &can_interfaces__msg__MobilityData__get_type_description_sources,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace can_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_can_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<can_interfaces::msg::MobilityData>()
{
  return &can_interfaces::msg::typesupport_fastrtps_cpp::_MobilityData__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, can_interfaces, msg, MobilityData)() {
  return &can_interfaces::msg::typesupport_fastrtps_cpp::_MobilityData__handle;
}

#ifdef __cplusplus
}
#endif
