// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from can_interfaces:msg/MobilityData.idl
// generated code does not contain a copyright notice
#ifndef CAN_INTERFACES__MSG__DETAIL__MOBILITY_DATA__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define CAN_INTERFACES__MSG__DETAIL__MOBILITY_DATA__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "can_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "can_interfaces/msg/detail/mobility_data__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_serialize_can_interfaces__msg__MobilityData(
  const can_interfaces__msg__MobilityData * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_deserialize_can_interfaces__msg__MobilityData(
  eprosima::fastcdr::Cdr &,
  can_interfaces__msg__MobilityData * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t get_serialized_size_can_interfaces__msg__MobilityData(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t max_serialized_size_can_interfaces__msg__MobilityData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
bool cdr_serialize_key_can_interfaces__msg__MobilityData(
  const can_interfaces__msg__MobilityData * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t get_serialized_size_key_can_interfaces__msg__MobilityData(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
size_t max_serialized_size_key_can_interfaces__msg__MobilityData(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_can_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, can_interfaces, msg, MobilityData)();

#ifdef __cplusplus
}
#endif

#endif  // CAN_INTERFACES__MSG__DETAIL__MOBILITY_DATA__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
