// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from can_interfaces:msg/CANQueue.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/can_queue.h"


#ifndef CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__STRUCT_H_
#define CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/CANQueue in the package can_interfaces.
typedef struct can_interfaces__msg__CANQueue
{
  int32_t arb_id;
  rosidl_runtime_c__int32__Sequence data;
} can_interfaces__msg__CANQueue;

// Struct for a sequence of can_interfaces__msg__CANQueue.
typedef struct can_interfaces__msg__CANQueue__Sequence
{
  can_interfaces__msg__CANQueue * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} can_interfaces__msg__CANQueue__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__STRUCT_H_
