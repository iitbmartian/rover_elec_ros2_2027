// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/drive_command.h"


#ifndef CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__STRUCT_H_
#define CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'drive_direction'
// Member 'drive_pwm'
// Member 'explicit_direction'
// Member 'explicit_pwm'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/DriveCommand in the package can_interfaces.
typedef struct can_interfaces__msg__DriveCommand
{
  rosidl_runtime_c__boolean__Sequence drive_direction;
  rosidl_runtime_c__int32__Sequence drive_pwm;
  rosidl_runtime_c__boolean__Sequence explicit_direction;
  rosidl_runtime_c__int32__Sequence explicit_pwm;
} can_interfaces__msg__DriveCommand;

// Struct for a sequence of can_interfaces__msg__DriveCommand.
typedef struct can_interfaces__msg__DriveCommand__Sequence
{
  can_interfaces__msg__DriveCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} can_interfaces__msg__DriveCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__STRUCT_H_
