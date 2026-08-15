// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from can_interfaces:msg/CANQueue.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "can_interfaces/msg/detail/can_queue__rosidl_typesupport_introspection_c.h"
#include "can_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "can_interfaces/msg/detail/can_queue__functions.h"
#include "can_interfaces/msg/detail/can_queue__struct.h"


// Include directives for member types
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  can_interfaces__msg__CANQueue__init(message_memory);
}

void can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_fini_function(void * message_memory)
{
  can_interfaces__msg__CANQueue__fini(message_memory);
}

size_t can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__size_function__CANQueue__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__get_const_function__CANQueue__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__get_function__CANQueue__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__fetch_function__CANQueue__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__get_const_function__CANQueue__data(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__assign_function__CANQueue__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__get_function__CANQueue__data(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__resize_function__CANQueue__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_member_array[2] = {
  {
    "arb_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(can_interfaces__msg__CANQueue, arb_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(can_interfaces__msg__CANQueue, data),  // bytes offset in struct
    NULL,  // default value
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__size_function__CANQueue__data,  // size() function pointer
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__get_const_function__CANQueue__data,  // get_const(index) function pointer
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__get_function__CANQueue__data,  // get(index) function pointer
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__fetch_function__CANQueue__data,  // fetch(index, &value) function pointer
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__assign_function__CANQueue__data,  // assign(index, value) function pointer
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__resize_function__CANQueue__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_members = {
  "can_interfaces__msg",  // message namespace
  "CANQueue",  // message name
  2,  // number of fields
  sizeof(can_interfaces__msg__CANQueue),
  false,  // has_any_key_member_
  can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_member_array,  // message members
  can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_init_function,  // function to initialize message memory (memory has to be allocated)
  can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_type_support_handle = {
  0,
  &can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_members,
  get_message_typesupport_handle_function,
  &can_interfaces__msg__CANQueue__get_type_hash,
  &can_interfaces__msg__CANQueue__get_type_description,
  &can_interfaces__msg__CANQueue__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_can_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, can_interfaces, msg, CANQueue)() {
  if (!can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_type_support_handle.typesupport_identifier) {
    can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &can_interfaces__msg__CANQueue__rosidl_typesupport_introspection_c__CANQueue_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
