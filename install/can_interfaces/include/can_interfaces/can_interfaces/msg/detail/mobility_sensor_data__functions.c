// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from can_interfaces:msg/MobilitySensorData.idl
// generated code does not contain a copyright notice
#include "can_interfaces/msg/detail/mobility_sensor_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
can_interfaces__msg__MobilitySensorData__init(can_interfaces__msg__MobilitySensorData * msg)
{
  if (!msg) {
    return false;
  }
  // explicit_mag_fl
  // explicit_quad_fl
  // explicit_imu_fl
  // drive_quad_fl
  // explicit_mag_fr
  // explicit_quad_fr
  // explicit_imu_fr
  // drive_quad_fr
  // explicit_mag_bl
  // explicit_quad_bl
  // explicit_imu_bl
  // drive_quad_bl
  // explicit_mag_br
  // explicit_quad_br
  // explicit_imu_br
  // drive_quad_br
  return true;
}

void
can_interfaces__msg__MobilitySensorData__fini(can_interfaces__msg__MobilitySensorData * msg)
{
  if (!msg) {
    return;
  }
  // explicit_mag_fl
  // explicit_quad_fl
  // explicit_imu_fl
  // drive_quad_fl
  // explicit_mag_fr
  // explicit_quad_fr
  // explicit_imu_fr
  // drive_quad_fr
  // explicit_mag_bl
  // explicit_quad_bl
  // explicit_imu_bl
  // drive_quad_bl
  // explicit_mag_br
  // explicit_quad_br
  // explicit_imu_br
  // drive_quad_br
}

bool
can_interfaces__msg__MobilitySensorData__are_equal(const can_interfaces__msg__MobilitySensorData * lhs, const can_interfaces__msg__MobilitySensorData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // explicit_mag_fl
  if (lhs->explicit_mag_fl != rhs->explicit_mag_fl) {
    return false;
  }
  // explicit_quad_fl
  if (lhs->explicit_quad_fl != rhs->explicit_quad_fl) {
    return false;
  }
  // explicit_imu_fl
  if (lhs->explicit_imu_fl != rhs->explicit_imu_fl) {
    return false;
  }
  // drive_quad_fl
  if (lhs->drive_quad_fl != rhs->drive_quad_fl) {
    return false;
  }
  // explicit_mag_fr
  if (lhs->explicit_mag_fr != rhs->explicit_mag_fr) {
    return false;
  }
  // explicit_quad_fr
  if (lhs->explicit_quad_fr != rhs->explicit_quad_fr) {
    return false;
  }
  // explicit_imu_fr
  if (lhs->explicit_imu_fr != rhs->explicit_imu_fr) {
    return false;
  }
  // drive_quad_fr
  if (lhs->drive_quad_fr != rhs->drive_quad_fr) {
    return false;
  }
  // explicit_mag_bl
  if (lhs->explicit_mag_bl != rhs->explicit_mag_bl) {
    return false;
  }
  // explicit_quad_bl
  if (lhs->explicit_quad_bl != rhs->explicit_quad_bl) {
    return false;
  }
  // explicit_imu_bl
  if (lhs->explicit_imu_bl != rhs->explicit_imu_bl) {
    return false;
  }
  // drive_quad_bl
  if (lhs->drive_quad_bl != rhs->drive_quad_bl) {
    return false;
  }
  // explicit_mag_br
  if (lhs->explicit_mag_br != rhs->explicit_mag_br) {
    return false;
  }
  // explicit_quad_br
  if (lhs->explicit_quad_br != rhs->explicit_quad_br) {
    return false;
  }
  // explicit_imu_br
  if (lhs->explicit_imu_br != rhs->explicit_imu_br) {
    return false;
  }
  // drive_quad_br
  if (lhs->drive_quad_br != rhs->drive_quad_br) {
    return false;
  }
  return true;
}

bool
can_interfaces__msg__MobilitySensorData__copy(
  const can_interfaces__msg__MobilitySensorData * input,
  can_interfaces__msg__MobilitySensorData * output)
{
  if (!input || !output) {
    return false;
  }
  // explicit_mag_fl
  output->explicit_mag_fl = input->explicit_mag_fl;
  // explicit_quad_fl
  output->explicit_quad_fl = input->explicit_quad_fl;
  // explicit_imu_fl
  output->explicit_imu_fl = input->explicit_imu_fl;
  // drive_quad_fl
  output->drive_quad_fl = input->drive_quad_fl;
  // explicit_mag_fr
  output->explicit_mag_fr = input->explicit_mag_fr;
  // explicit_quad_fr
  output->explicit_quad_fr = input->explicit_quad_fr;
  // explicit_imu_fr
  output->explicit_imu_fr = input->explicit_imu_fr;
  // drive_quad_fr
  output->drive_quad_fr = input->drive_quad_fr;
  // explicit_mag_bl
  output->explicit_mag_bl = input->explicit_mag_bl;
  // explicit_quad_bl
  output->explicit_quad_bl = input->explicit_quad_bl;
  // explicit_imu_bl
  output->explicit_imu_bl = input->explicit_imu_bl;
  // drive_quad_bl
  output->drive_quad_bl = input->drive_quad_bl;
  // explicit_mag_br
  output->explicit_mag_br = input->explicit_mag_br;
  // explicit_quad_br
  output->explicit_quad_br = input->explicit_quad_br;
  // explicit_imu_br
  output->explicit_imu_br = input->explicit_imu_br;
  // drive_quad_br
  output->drive_quad_br = input->drive_quad_br;
  return true;
}

can_interfaces__msg__MobilitySensorData *
can_interfaces__msg__MobilitySensorData__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  can_interfaces__msg__MobilitySensorData * msg = (can_interfaces__msg__MobilitySensorData *)allocator.allocate(sizeof(can_interfaces__msg__MobilitySensorData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(can_interfaces__msg__MobilitySensorData));
  bool success = can_interfaces__msg__MobilitySensorData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
can_interfaces__msg__MobilitySensorData__destroy(can_interfaces__msg__MobilitySensorData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    can_interfaces__msg__MobilitySensorData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
can_interfaces__msg__MobilitySensorData__Sequence__init(can_interfaces__msg__MobilitySensorData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  can_interfaces__msg__MobilitySensorData * data = NULL;

  if (size) {
    data = (can_interfaces__msg__MobilitySensorData *)allocator.zero_allocate(size, sizeof(can_interfaces__msg__MobilitySensorData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = can_interfaces__msg__MobilitySensorData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        can_interfaces__msg__MobilitySensorData__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
can_interfaces__msg__MobilitySensorData__Sequence__fini(can_interfaces__msg__MobilitySensorData__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      can_interfaces__msg__MobilitySensorData__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

can_interfaces__msg__MobilitySensorData__Sequence *
can_interfaces__msg__MobilitySensorData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  can_interfaces__msg__MobilitySensorData__Sequence * array = (can_interfaces__msg__MobilitySensorData__Sequence *)allocator.allocate(sizeof(can_interfaces__msg__MobilitySensorData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = can_interfaces__msg__MobilitySensorData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
can_interfaces__msg__MobilitySensorData__Sequence__destroy(can_interfaces__msg__MobilitySensorData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    can_interfaces__msg__MobilitySensorData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
can_interfaces__msg__MobilitySensorData__Sequence__are_equal(const can_interfaces__msg__MobilitySensorData__Sequence * lhs, const can_interfaces__msg__MobilitySensorData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!can_interfaces__msg__MobilitySensorData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
can_interfaces__msg__MobilitySensorData__Sequence__copy(
  const can_interfaces__msg__MobilitySensorData__Sequence * input,
  can_interfaces__msg__MobilitySensorData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(can_interfaces__msg__MobilitySensorData);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    can_interfaces__msg__MobilitySensorData * data =
      (can_interfaces__msg__MobilitySensorData *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!can_interfaces__msg__MobilitySensorData__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          can_interfaces__msg__MobilitySensorData__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!can_interfaces__msg__MobilitySensorData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
