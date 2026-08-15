// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from can_interfaces:msg/MobilitySensorData.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/mobility_sensor_data.h"


#ifndef CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__STRUCT_H_
#define CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/MobilitySensorData in the package can_interfaces.
typedef struct can_interfaces__msg__MobilitySensorData
{
  int32_t explicit_mag_fl;
  int32_t explicit_quad_fl;
  int32_t explicit_imu_fl;
  int32_t drive_quad_fl;
  int32_t explicit_mag_fr;
  int32_t explicit_quad_fr;
  int32_t explicit_imu_fr;
  int32_t drive_quad_fr;
  int32_t explicit_mag_bl;
  int32_t explicit_quad_bl;
  int32_t explicit_imu_bl;
  int32_t drive_quad_bl;
  int32_t explicit_mag_br;
  int32_t explicit_quad_br;
  int32_t explicit_imu_br;
  int32_t drive_quad_br;
} can_interfaces__msg__MobilitySensorData;

// Struct for a sequence of can_interfaces__msg__MobilitySensorData.
typedef struct can_interfaces__msg__MobilitySensorData__Sequence
{
  can_interfaces__msg__MobilitySensorData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} can_interfaces__msg__MobilitySensorData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__STRUCT_H_
