// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from can_interfaces:msg/CANQueue.idl
// generated code does not contain a copyright notice

#include "can_interfaces/msg/detail/can_queue__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_can_interfaces
const rosidl_type_hash_t *
can_interfaces__msg__CANQueue__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x48, 0xaa, 0x2a, 0x4a, 0x20, 0x96, 0xea, 0xed,
      0x01, 0x7e, 0x0c, 0x62, 0x8b, 0x0d, 0xcf, 0x92,
      0x44, 0x67, 0x11, 0x78, 0xa1, 0xd8, 0x72, 0xba,
      0xea, 0xd0, 0x9d, 0x0a, 0x88, 0x42, 0x0c, 0xe7,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char can_interfaces__msg__CANQueue__TYPE_NAME[] = "can_interfaces/msg/CANQueue";

// Define type names, field names, and default values
static char can_interfaces__msg__CANQueue__FIELD_NAME__arb_id[] = "arb_id";
static char can_interfaces__msg__CANQueue__FIELD_NAME__data[] = "data";

static rosidl_runtime_c__type_description__Field can_interfaces__msg__CANQueue__FIELDS[] = {
  {
    {can_interfaces__msg__CANQueue__FIELD_NAME__arb_id, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__CANQueue__FIELD_NAME__data, 4, 4},
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
can_interfaces__msg__CANQueue__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {can_interfaces__msg__CANQueue__TYPE_NAME, 27, 27},
      {can_interfaces__msg__CANQueue__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "int32 arb_id\n"
  "int32[] data";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
can_interfaces__msg__CANQueue__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {can_interfaces__msg__CANQueue__TYPE_NAME, 27, 27},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 25, 25},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
can_interfaces__msg__CANQueue__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *can_interfaces__msg__CANQueue__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
