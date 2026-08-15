// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice
#include "can_interfaces/msg/detail/drive_command__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "can_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "can_interfaces/msg/detail/drive_command__struct.h"
#include "can_interfaces/msg/detail/drive_command__functions.h"
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

#include "rosidl_runtime_c/primitives_sequence.h"  // drive_direction, drive_pwm, explicit_direction, explicit_pwm
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // drive_direction, drive_pwm, explicit_direction, explicit_pwm

// forward declare type support functions


using _DriveCommand__ros_msg_type = can_interfaces__msg__DriveCommand;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_serialize_can_interfaces__msg__DriveCommand(
  const can_interfaces__msg__DriveCommand * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: drive_direction
  {
    size_t size = ros_message->drive_direction.size;
    auto array_ptr = ros_message->drive_direction.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  // Field name: drive_pwm
  {
    size_t size = ros_message->drive_pwm.size;
    auto array_ptr = ros_message->drive_pwm.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  // Field name: explicit_direction
  {
    size_t size = ros_message->explicit_direction.size;
    auto array_ptr = ros_message->explicit_direction.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  // Field name: explicit_pwm
  {
    size_t size = ros_message->explicit_pwm.size;
    auto array_ptr = ros_message->explicit_pwm.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_deserialize_can_interfaces__msg__DriveCommand(
  eprosima::fastcdr::Cdr & cdr,
  can_interfaces__msg__DriveCommand * ros_message)
{
  // Field name: drive_direction
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->drive_direction.data) {
      rosidl_runtime_c__boolean__Sequence__fini(&ros_message->drive_direction);
    }
    if (!rosidl_runtime_c__boolean__Sequence__init(&ros_message->drive_direction, size)) {
      fprintf(stderr, "failed to create array for field 'drive_direction'");
      return false;
    }
    auto array_ptr = ros_message->drive_direction.data;
    for (size_t i = 0; i < size; ++i) {
      uint8_t tmp;
      cdr >> tmp;
      array_ptr[i] = tmp ? true : false;
    }
  }

  // Field name: drive_pwm
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->drive_pwm.data) {
      rosidl_runtime_c__int32__Sequence__fini(&ros_message->drive_pwm);
    }
    if (!rosidl_runtime_c__int32__Sequence__init(&ros_message->drive_pwm, size)) {
      fprintf(stderr, "failed to create array for field 'drive_pwm'");
      return false;
    }
    auto array_ptr = ros_message->drive_pwm.data;
    cdr.deserialize_array(array_ptr, size);
  }

  // Field name: explicit_direction
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->explicit_direction.data) {
      rosidl_runtime_c__boolean__Sequence__fini(&ros_message->explicit_direction);
    }
    if (!rosidl_runtime_c__boolean__Sequence__init(&ros_message->explicit_direction, size)) {
      fprintf(stderr, "failed to create array for field 'explicit_direction'");
      return false;
    }
    auto array_ptr = ros_message->explicit_direction.data;
    for (size_t i = 0; i < size; ++i) {
      uint8_t tmp;
      cdr >> tmp;
      array_ptr[i] = tmp ? true : false;
    }
  }

  // Field name: explicit_pwm
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->explicit_pwm.data) {
      rosidl_runtime_c__int32__Sequence__fini(&ros_message->explicit_pwm);
    }
    if (!rosidl_runtime_c__int32__Sequence__init(&ros_message->explicit_pwm, size)) {
      fprintf(stderr, "failed to create array for field 'explicit_pwm'");
      return false;
    }
    auto array_ptr = ros_message->explicit_pwm.data;
    cdr.deserialize_array(array_ptr, size);
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t get_serialized_size_can_interfaces__msg__DriveCommand(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _DriveCommand__ros_msg_type * ros_message = static_cast<const _DriveCommand__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: drive_direction
  {
    size_t array_size = ros_message->drive_direction.size;
    auto array_ptr = ros_message->drive_direction.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_pwm
  {
    size_t array_size = ros_message->drive_pwm.size;
    auto array_ptr = ros_message->drive_pwm.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_direction
  {
    size_t array_size = ros_message->explicit_direction.size;
    auto array_ptr = ros_message->explicit_direction.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_pwm
  {
    size_t array_size = ros_message->explicit_pwm.size;
    auto array_ptr = ros_message->explicit_pwm.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t max_serialized_size_can_interfaces__msg__DriveCommand(
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

  // Field name: drive_direction
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: drive_pwm
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_direction
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: explicit_pwm
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = can_interfaces__msg__DriveCommand;
    is_plain =
      (
      offsetof(DataType, explicit_pwm) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_serialize_key_can_interfaces__msg__DriveCommand(
  const can_interfaces__msg__DriveCommand * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: drive_direction
  {
    size_t size = ros_message->drive_direction.size;
    auto array_ptr = ros_message->drive_direction.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  // Field name: drive_pwm
  {
    size_t size = ros_message->drive_pwm.size;
    auto array_ptr = ros_message->drive_pwm.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  // Field name: explicit_direction
  {
    size_t size = ros_message->explicit_direction.size;
    auto array_ptr = ros_message->explicit_direction.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  // Field name: explicit_pwm
  {
    size_t size = ros_message->explicit_pwm.size;
    auto array_ptr = ros_message->explicit_pwm.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serialize_array(array_ptr, size);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t get_serialized_size_key_can_interfaces__msg__DriveCommand(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _DriveCommand__ros_msg_type * ros_message = static_cast<const _DriveCommand__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: drive_direction
  {
    size_t array_size = ros_message->drive_direction.size;
    auto array_ptr = ros_message->drive_direction.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: drive_pwm
  {
    size_t array_size = ros_message->drive_pwm.size;
    auto array_ptr = ros_message->drive_pwm.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_direction
  {
    size_t array_size = ros_message->explicit_direction.size;
    auto array_ptr = ros_message->explicit_direction.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: explicit_pwm
  {
    size_t array_size = ros_message->explicit_pwm.size;
    auto array_ptr = ros_message->explicit_pwm.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t max_serialized_size_key_can_interfaces__msg__DriveCommand(
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
  // Field name: drive_direction
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: drive_pwm
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: explicit_direction
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: explicit_pwm
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = can_interfaces__msg__DriveCommand;
    is_plain =
      (
      offsetof(DataType, explicit_pwm) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _DriveCommand__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const can_interfaces__msg__DriveCommand * ros_message = static_cast<const can_interfaces__msg__DriveCommand *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_can_interfaces__msg__DriveCommand(ros_message, cdr);
}

static bool _DriveCommand__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  can_interfaces__msg__DriveCommand * ros_message = static_cast<can_interfaces__msg__DriveCommand *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_can_interfaces__msg__DriveCommand(cdr, ros_message);
}

static uint32_t _DriveCommand__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_can_interfaces__msg__DriveCommand(
      untyped_ros_message, 0));
}

static size_t _DriveCommand__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_can_interfaces__msg__DriveCommand(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_DriveCommand = {
  "can_interfaces::msg",
  "DriveCommand",
  _DriveCommand__cdr_serialize,
  _DriveCommand__cdr_deserialize,
  _DriveCommand__get_serialized_size,
  _DriveCommand__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _DriveCommand__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_DriveCommand,
  get_message_typesupport_handle_function,
  &can_interfaces__msg__DriveCommand__get_type_hash,
  &can_interfaces__msg__DriveCommand__get_type_description,
  &can_interfaces__msg__DriveCommand__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, can_interfaces, msg, DriveCommand)() {
  return &_DriveCommand__type_support;
}

#if defined(__cplusplus)
}
#endif
