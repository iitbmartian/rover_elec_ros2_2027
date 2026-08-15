// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "can_interfaces/msg/detail/drive_command__rosidl_typesupport_introspection_c.h"
#include "can_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "can_interfaces/msg/detail/drive_command__functions.h"
#include "can_interfaces/msg/detail/drive_command__struct.h"


// Include directives for member types
// Member `drive_direction`
// Member `drive_pwm`
// Member `explicit_direction`
// Member `explicit_pwm`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  can_interfaces__msg__DriveCommand__init(message_memory);
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_fini_function(void * message_memory)
{
  can_interfaces__msg__DriveCommand__fini(message_memory);
}

size_t can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__drive_direction(
  const void * untyped_member)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return member->size;
}

const void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__drive_direction(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__drive_direction(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__drive_direction(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const bool * item =
    ((const bool *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__drive_direction(untyped_member, index));
  bool * value =
    (bool *)(untyped_value);
  *value = *item;
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__drive_direction(
  void * untyped_member, size_t index, const void * untyped_value)
{
  bool * item =
    ((bool *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__drive_direction(untyped_member, index));
  const bool * value =
    (const bool *)(untyped_value);
  *item = *value;
}

bool can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__drive_direction(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  rosidl_runtime_c__boolean__Sequence__fini(member);
  return rosidl_runtime_c__boolean__Sequence__init(member, size);
}

size_t can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__drive_pwm(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__drive_pwm(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__drive_pwm(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__drive_pwm(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__drive_pwm(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__drive_pwm(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__drive_pwm(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__drive_pwm(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

size_t can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__explicit_direction(
  const void * untyped_member)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return member->size;
}

const void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__explicit_direction(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__explicit_direction(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__explicit_direction(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const bool * item =
    ((const bool *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__explicit_direction(untyped_member, index));
  bool * value =
    (bool *)(untyped_value);
  *value = *item;
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__explicit_direction(
  void * untyped_member, size_t index, const void * untyped_value)
{
  bool * item =
    ((bool *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__explicit_direction(untyped_member, index));
  const bool * value =
    (const bool *)(untyped_value);
  *item = *value;
}

bool can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__explicit_direction(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  rosidl_runtime_c__boolean__Sequence__fini(member);
  return rosidl_runtime_c__boolean__Sequence__init(member, size);
}

size_t can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__explicit_pwm(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__explicit_pwm(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__explicit_pwm(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__explicit_pwm(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__explicit_pwm(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__explicit_pwm(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__explicit_pwm(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__explicit_pwm(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_member_array[4] = {
  {
    "drive_direction",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(can_interfaces__msg__DriveCommand, drive_direction),  // bytes offset in struct
    NULL,  // default value
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__drive_direction,  // size() function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__drive_direction,  // get_const(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__drive_direction,  // get(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__drive_direction,  // fetch(index, &value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__drive_direction,  // assign(index, value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__drive_direction  // resize(index) function pointer
  },
  {
    "drive_pwm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(can_interfaces__msg__DriveCommand, drive_pwm),  // bytes offset in struct
    NULL,  // default value
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__drive_pwm,  // size() function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__drive_pwm,  // get_const(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__drive_pwm,  // get(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__drive_pwm,  // fetch(index, &value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__drive_pwm,  // assign(index, value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__drive_pwm  // resize(index) function pointer
  },
  {
    "explicit_direction",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(can_interfaces__msg__DriveCommand, explicit_direction),  // bytes offset in struct
    NULL,  // default value
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__explicit_direction,  // size() function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__explicit_direction,  // get_const(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__explicit_direction,  // get(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__explicit_direction,  // fetch(index, &value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__explicit_direction,  // assign(index, value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__explicit_direction  // resize(index) function pointer
  },
  {
    "explicit_pwm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(can_interfaces__msg__DriveCommand, explicit_pwm),  // bytes offset in struct
    NULL,  // default value
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__size_function__DriveCommand__explicit_pwm,  // size() function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_const_function__DriveCommand__explicit_pwm,  // get_const(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__get_function__DriveCommand__explicit_pwm,  // get(index) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__fetch_function__DriveCommand__explicit_pwm,  // fetch(index, &value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__assign_function__DriveCommand__explicit_pwm,  // assign(index, value) function pointer
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__resize_function__DriveCommand__explicit_pwm  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_members = {
  "can_interfaces__msg",  // message namespace
  "DriveCommand",  // message name
  4,  // number of fields
  sizeof(can_interfaces__msg__DriveCommand),
  false,  // has_any_key_member_
  can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_member_array,  // message members
  can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_init_function,  // function to initialize message memory (memory has to be allocated)
  can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_type_support_handle = {
  0,
  &can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_members,
  get_message_typesupport_handle_function,
  &can_interfaces__msg__DriveCommand__get_type_hash,
  &can_interfaces__msg__DriveCommand__get_type_description,
  &can_interfaces__msg__DriveCommand__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_can_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, can_interfaces, msg, DriveCommand)() {
  if (!can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_type_support_handle.typesupport_identifier) {
    can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &can_interfaces__msg__DriveCommand__rosidl_typesupport_introspection_c__DriveCommand_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
