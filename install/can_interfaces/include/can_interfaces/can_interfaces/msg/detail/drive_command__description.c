// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice

#include "can_interfaces/msg/detail/drive_command__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_can_interfaces
const rosidl_type_hash_t *
can_interfaces__msg__DriveCommand__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x74, 0xb4, 0xbf, 0xd0, 0x41, 0x46, 0x13, 0x9c,
      0xe5, 0xb6, 0xed, 0xbe, 0x77, 0xad, 0xad, 0xf7,
      0xdf, 0xa5, 0x75, 0xe8, 0x5c, 0x66, 0x97, 0x82,
      0x9c, 0xf9, 0x7b, 0x91, 0x67, 0xd9, 0xf8, 0x3d,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char can_interfaces__msg__DriveCommand__TYPE_NAME[] = "can_interfaces/msg/DriveCommand";

// Define type names, field names, and default values
static char can_interfaces__msg__DriveCommand__FIELD_NAME__drive_direction[] = "drive_direction";
static char can_interfaces__msg__DriveCommand__FIELD_NAME__drive_pwm[] = "drive_pwm";
static char can_interfaces__msg__DriveCommand__FIELD_NAME__explicit_direction[] = "explicit_direction";
static char can_interfaces__msg__DriveCommand__FIELD_NAME__explicit_pwm[] = "explicit_pwm";

static rosidl_runtime_c__type_description__Field can_interfaces__msg__DriveCommand__FIELDS[] = {
  {
    {can_interfaces__msg__DriveCommand__FIELD_NAME__drive_direction, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__DriveCommand__FIELD_NAME__drive_pwm, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__DriveCommand__FIELD_NAME__explicit_direction, 18, 18},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__DriveCommand__FIELD_NAME__explicit_pwm, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
can_interfaces__msg__DriveCommand__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {can_interfaces__msg__DriveCommand__TYPE_NAME, 31, 31},
      {can_interfaces__msg__DriveCommand__FIELDS, 4, 4},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "bool[] drive_direction \n"
  "int32[] drive_pwm\n"
  "bool[] explicit_direction\n"
  "int32[] explicit_pwm";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
can_interfaces__msg__DriveCommand__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {can_interfaces__msg__DriveCommand__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 88, 88},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
can_interfaces__msg__DriveCommand__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *can_interfaces__msg__DriveCommand__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
