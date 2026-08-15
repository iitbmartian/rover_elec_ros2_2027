// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from can_interfaces:msg/MobilitySensorData.idl
// generated code does not contain a copyright notice
#include "can_interfaces/msg/detail/mobility_sensor_data__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "can_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "can_interfaces/msg/detail/mobility_sensor_data__struct.h"
#include "can_interfaces/msg/detail/mobility_sensor_data__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _MobilitySensorData__ros_msg_type = can_interfaces__msg__MobilitySensorData;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_serialize_can_interfaces__msg__MobilitySensorData(
  const can_interfaces__msg__MobilitySensorData * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: explicit_mag_fl
  {
    cdr << ros_message->explicit_mag_fl;
  }

  // Field name: explicit_quad_fl
  {
    cdr << ros_message->explicit_quad_fl;
  }

  // Field name: explicit_imu_fl
  {
    cdr << ros_message->explicit_imu_fl;
  }

  // Field name: drive_quad_fl
  {
    cdr << ros_message->drive_quad_fl;
  }

  // Field name: explicit_mag_fr
  {
    cdr << ros_message->explicit_mag_fr;
  }

  // Field name: explicit_quad_fr
  {
    cdr << ros_message->explicit_quad_fr;
  }

  // Field name: explicit_imu_fr
  {
    cdr << ros_message->explicit_imu_fr;
  }

  // Field name: drive_quad_fr
  {
    cdr << ros_message->drive_quad_fr;
  }

  // Field name: explicit_mag_bl
  {
    cdr << ros_message->explicit_mag_bl;
  }

  // Field name: explicit_quad_bl
  {
    cdr << ros_message->explicit_quad_bl;
  }

  // Field name: explicit_imu_bl
  {
    cdr << ros_message->explicit_imu_bl;
  }

  // Field name: drive_quad_bl
  {
    cdr << ros_message->drive_quad_bl;
  }

  // Field name: explicit_mag_br
  {
    cdr << ros_message->explicit_mag_br;
  }

  // Field name: explicit_quad_br
  {
    cdr << ros_message->explicit_quad_br;
  }

  // Field name: explicit_imu_br
  {
    cdr << ros_message->explicit_imu_br;
  }

  // Field name: drive_quad_br
  {
    cdr << ros_message->drive_quad_br;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_deserialize_can_interfaces__msg__MobilitySensorData(
  eprosima::fastcdr::Cdr & cdr,
  can_interfaces__msg__MobilitySensorData * ros_message)
{
  // Field name: explicit_mag_fl
  {
    cdr >> ros_message->explicit_mag_fl;
  }

  // Field name: explicit_quad_fl
  {
    cdr >> ros_message->explicit_quad_fl;
  }

  // Field name: explicit_imu_fl
  {
    cdr >> ros_message->explicit_imu_fl;
  }

  // Field name: drive_quad_fl
  {
    cdr >> ros_message->drive_quad_fl;
  }

  // Field name: explicit_mag_fr
  {
    cdr >> ros_message->explicit_mag_fr;
  }

  // Field name: explicit_quad_fr
  {
    cdr >> ros_message->explicit_quad_fr;
  }

  // Field name: explicit_imu_fr
  {
    cdr >> ros_message->explicit_imu_fr;
  }

  // Field name: drive_quad_fr
  {
    cdr >> ros_message->drive_quad_fr;
  }

  // Field name: explicit_mag_bl
  {
    cdr >> ros_message->explicit_mag_bl;
  }

  // Field name: explicit_quad_bl
  {
    cdr >> ros_message->explicit_quad_bl;
  }

  // Field name: explicit_imu_bl
  {
    cdr >> ros_message->explicit_imu_bl;
  }

  // Field name: drive_quad_bl
  {
    cdr >> ros_message->drive_quad_bl;
  }

  // Field name: explicit_mag_br
  {
    cdr >> ros_message->explicit_mag_br;
  }

  // Field name: explicit_quad_br
  {
    cdr >> ros_message->explicit_quad_br;
  }

  // Field name: explicit_imu_br
  {
    cdr >> ros_message->explicit_imu_br;
  }

  // Field name: drive_quad_br
  {
    cdr >> ros_message->drive_quad_br;
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t get_serialized_size_can_interfaces__msg__MobilitySensorData(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _MobilitySensorData__ros_msg_type * ros_message = static_cast<const _MobilitySensorData__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: explicit_mag_fl
  {
    size_t item_size = sizeof(ros_message->explicit_mag_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_fl
  {
    size_t item_size = sizeof(ros_message->explicit_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_fl
  {
    size_t item_size = sizeof(ros_message->explicit_imu_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_fl
  {
    size_t item_size = sizeof(ros_message->drive_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_mag_fr
  {
    size_t item_size = sizeof(ros_message->explicit_mag_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_fr
  {
    size_t item_size = sizeof(ros_message->explicit_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_fr
  {
    size_t item_size = sizeof(ros_message->explicit_imu_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_fr
  {
    size_t item_size = sizeof(ros_message->drive_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_mag_bl
  {
    size_t item_size = sizeof(ros_message->explicit_mag_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_bl
  {
    size_t item_size = sizeof(ros_message->explicit_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_bl
  {
    size_t item_size = sizeof(ros_message->explicit_imu_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_bl
  {
    size_t item_size = sizeof(ros_message->drive_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_mag_br
  {
    size_t item_size = sizeof(ros_message->explicit_mag_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_br
  {
    size_t item_size = sizeof(ros_message->explicit_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_br
  {
    size_t item_size = sizeof(ros_message->explicit_imu_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_br
  {
    size_t item_size = sizeof(ros_message->drive_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t max_serialized_size_can_interfaces__msg__MobilitySensorData(
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

  // Field name: explicit_mag_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_mag_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_mag_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_mag_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_br
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
    using DataType = can_interfaces__msg__MobilitySensorData;
    is_plain =
      (
      offsetof(DataType, drive_quad_br) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_serialize_key_can_interfaces__msg__MobilitySensorData(
  const can_interfaces__msg__MobilitySensorData * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: explicit_mag_fl
  {
    cdr << ros_message->explicit_mag_fl;
  }

  // Field name: explicit_quad_fl
  {
    cdr << ros_message->explicit_quad_fl;
  }

  // Field name: explicit_imu_fl
  {
    cdr << ros_message->explicit_imu_fl;
  }

  // Field name: drive_quad_fl
  {
    cdr << ros_message->drive_quad_fl;
  }

  // Field name: explicit_mag_fr
  {
    cdr << ros_message->explicit_mag_fr;
  }

  // Field name: explicit_quad_fr
  {
    cdr << ros_message->explicit_quad_fr;
  }

  // Field name: explicit_imu_fr
  {
    cdr << ros_message->explicit_imu_fr;
  }

  // Field name: drive_quad_fr
  {
    cdr << ros_message->drive_quad_fr;
  }

  // Field name: explicit_mag_bl
  {
    cdr << ros_message->explicit_mag_bl;
  }

  // Field name: explicit_quad_bl
  {
    cdr << ros_message->explicit_quad_bl;
  }

  // Field name: explicit_imu_bl
  {
    cdr << ros_message->explicit_imu_bl;
  }

  // Field name: drive_quad_bl
  {
    cdr << ros_message->drive_quad_bl;
  }

  // Field name: explicit_mag_br
  {
    cdr << ros_message->explicit_mag_br;
  }

  // Field name: explicit_quad_br
  {
    cdr << ros_message->explicit_quad_br;
  }

  // Field name: explicit_imu_br
  {
    cdr << ros_message->explicit_imu_br;
  }

  // Field name: drive_quad_br
  {
    cdr << ros_message->drive_quad_br;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t get_serialized_size_key_can_interfaces__msg__MobilitySensorData(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _MobilitySensorData__ros_msg_type * ros_message = static_cast<const _MobilitySensorData__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: explicit_mag_fl
  {
    size_t item_size = sizeof(ros_message->explicit_mag_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_fl
  {
    size_t item_size = sizeof(ros_message->explicit_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_fl
  {
    size_t item_size = sizeof(ros_message->explicit_imu_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_fl
  {
    size_t item_size = sizeof(ros_message->drive_quad_fl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_mag_fr
  {
    size_t item_size = sizeof(ros_message->explicit_mag_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_fr
  {
    size_t item_size = sizeof(ros_message->explicit_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_fr
  {
    size_t item_size = sizeof(ros_message->explicit_imu_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_fr
  {
    size_t item_size = sizeof(ros_message->drive_quad_fr);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_mag_bl
  {
    size_t item_size = sizeof(ros_message->explicit_mag_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_bl
  {
    size_t item_size = sizeof(ros_message->explicit_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_bl
  {
    size_t item_size = sizeof(ros_message->explicit_imu_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_bl
  {
    size_t item_size = sizeof(ros_message->drive_quad_bl);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_mag_br
  {
    size_t item_size = sizeof(ros_message->explicit_mag_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_quad_br
  {
    size_t item_size = sizeof(ros_message->explicit_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_imu_br
  {
    size_t item_size = sizeof(ros_message->explicit_imu_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_quad_br
  {
    size_t item_size = sizeof(ros_message->drive_quad_br);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t max_serialized_size_key_can_interfaces__msg__MobilitySensorData(
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
  // Field name: explicit_mag_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_fl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_mag_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_fr
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_mag_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_bl
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_mag_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_quad_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_imu_br
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: drive_quad_br
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
    using DataType = can_interfaces__msg__MobilitySensorData;
    is_plain =
      (
      offsetof(DataType, drive_quad_br) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _MobilitySensorData__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const can_interfaces__msg__MobilitySensorData * ros_message = static_cast<const can_interfaces__msg__MobilitySensorData *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_can_interfaces__msg__MobilitySensorData(ros_message, cdr);
}

static bool _MobilitySensorData__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  can_interfaces__msg__MobilitySensorData * ros_message = static_cast<can_interfaces__msg__MobilitySensorData *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_can_interfaces__msg__MobilitySensorData(cdr, ros_message);
}

static uint32_t _MobilitySensorData__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_can_interfaces__msg__MobilitySensorData(
      untyped_ros_message, 0));
}

static size_t _MobilitySensorData__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_can_interfaces__msg__MobilitySensorData(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_MobilitySensorData = {
  "can_interfaces::msg",
  "MobilitySensorData",
  _MobilitySensorData__cdr_serialize,
  _MobilitySensorData__cdr_deserialize,
  _MobilitySensorData__get_serialized_size,
  _MobilitySensorData__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _MobilitySensorData__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_MobilitySensorData,
  get_message_typesupport_handle_function,
  &can_interfaces__msg__MobilitySensorData__get_type_hash,
  &can_interfaces__msg__MobilitySensorData__get_type_description,
  &can_interfaces__msg__MobilitySensorData__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, can_interfaces, msg, MobilitySensorData)() {
  return &_MobilitySensorData__type_support;
}

#if defined(__cplusplus)
}
#endif
