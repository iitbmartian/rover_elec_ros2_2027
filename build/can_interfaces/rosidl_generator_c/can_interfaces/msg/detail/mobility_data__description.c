// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from can_interfaces:msg/MobilityData.idl
// generated code does not contain a copyright notice

#include "can_interfaces/msg/detail/mobility_data__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_can_interfaces
const rosidl_type_hash_t *
can_interfaces__msg__MobilityData__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xdb, 0x07, 0xdc, 0xeb, 0x1d, 0x16, 0x78, 0x14,
      0xf6, 0xef, 0x3a, 0x6d, 0xaa, 0x8d, 0xfc, 0xcf,
      0x4b, 0xc7, 0x56, 0xfe, 0x7f, 0x60, 0x7f, 0x90,
      0x89, 0x07, 0xa9, 0x22, 0x87, 0xc1, 0xfb, 0x3a,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char can_interfaces__msg__MobilityData__TYPE_NAME[] = "can_interfaces/msg/MobilityData";

// Define type names, field names, and default values
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_fl[] = "explicit_mag_fl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_fl[] = "explicit_quad_fl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_fl[] = "explicit_imu_fl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_fl[] = "drive_quad_fl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_fr[] = "explicit_mag_fr";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_fr[] = "explicit_quad_fr";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_fr[] = "explicit_imu_fr";
static char can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_fr[] = "drive_quad_fr";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_bl[] = "explicit_mag_bl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_bl[] = "explicit_quad_bl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_bl[] = "explicit_imu_bl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_bl[] = "drive_quad_bl";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_br[] = "explicit_mag_br";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_br[] = "explicit_quad_br";
static char can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_br[] = "explicit_imu_br";
static char can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_br[] = "drive_quad_br";

static rosidl_runtime_c__type_description__Field can_interfaces__msg__MobilityData__FIELDS[] = {
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_fl, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_fl, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_fl, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_fl, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_fr, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_fr, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_fr, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_fr, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_bl, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_bl, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_bl, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_bl, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_mag_br, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_quad_br, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__explicit_imu_br, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {can_interfaces__msg__MobilityData__FIELD_NAME__drive_quad_br, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
can_interfaces__msg__MobilityData__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {can_interfaces__msg__MobilityData__TYPE_NAME, 31, 31},
      {can_interfaces__msg__MobilityData__FIELDS, 16, 16},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "int32 explicit_mag_fl\n"
  "int32 explicit_quad_fl\n"
  "int32 explicit_imu_fl\n"
  "int32 drive_quad_fl\n"
  "int32 explicit_mag_fr\n"
  "int32 explicit_quad_fr\n"
  "int32 explicit_imu_fr\n"
  "int32 drive_quad_fr\n"
  "int32 explicit_mag_bl\n"
  "int32 explicit_quad_bl\n"
  "int32 explicit_imu_bl\n"
  "int32 drive_quad_bl\n"
  "int32 explicit_mag_br\n"
  "int32 explicit_quad_br\n"
  "int32 explicit_imu_br\n"
  "int32 drive_quad_br";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
can_interfaces__msg__MobilityData__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {can_interfaces__msg__MobilityData__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 348, 348},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
can_interfaces__msg__MobilityData__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *can_interfaces__msg__MobilityData__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
