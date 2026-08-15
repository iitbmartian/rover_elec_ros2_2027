// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from can_interfaces:msg/CANQueue.idl
// generated code does not contain a copyright notice
#include "can_interfaces/msg/detail/can_queue__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
can_interfaces__msg__CANQueue__init(can_interfaces__msg__CANQueue * msg)
{
  if (!msg) {
    return false;
  }
  // arb_id
  // data
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->data, 0)) {
    can_interfaces__msg__CANQueue__fini(msg);
    return false;
  }
  return true;
}

void
can_interfaces__msg__CANQueue__fini(can_interfaces__msg__CANQueue * msg)
{
  if (!msg) {
    return;
  }
  // arb_id
  // data
  rosidl_runtime_c__int32__Sequence__fini(&msg->data);
}

bool
can_interfaces__msg__CANQueue__are_equal(const can_interfaces__msg__CANQueue * lhs, const can_interfaces__msg__CANQueue * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // arb_id
  if (lhs->arb_id != rhs->arb_id) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
can_interfaces__msg__CANQueue__copy(
  const can_interfaces__msg__CANQueue * input,
  can_interfaces__msg__CANQueue * output)
{
  if (!input || !output) {
    return false;
  }
  // arb_id
  output->arb_id = input->arb_id;
  // data
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

can_interfaces__msg__CANQueue *
can_interfaces__msg__CANQueue__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  can_interfaces__msg__CANQueue * msg = (can_interfaces__msg__CANQueue *)allocator.allocate(sizeof(can_interfaces__msg__CANQueue), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(can_interfaces__msg__CANQueue));
  bool success = can_interfaces__msg__CANQueue__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
can_interfaces__msg__CANQueue__destroy(can_interfaces__msg__CANQueue * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    can_interfaces__msg__CANQueue__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
can_interfaces__msg__CANQueue__Sequence__init(can_interfaces__msg__CANQueue__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  can_interfaces__msg__CANQueue * data = NULL;

  if (size) {
    data = (can_interfaces__msg__CANQueue *)allocator.zero_allocate(size, sizeof(can_interfaces__msg__CANQueue), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = can_interfaces__msg__CANQueue__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        can_interfaces__msg__CANQueue__fini(&data[i - 1]);
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
can_interfaces__msg__CANQueue__Sequence__fini(can_interfaces__msg__CANQueue__Sequence * array)
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
      can_interfaces__msg__CANQueue__fini(&array->data[i]);
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

can_interfaces__msg__CANQueue__Sequence *
can_interfaces__msg__CANQueue__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  can_interfaces__msg__CANQueue__Sequence * array = (can_interfaces__msg__CANQueue__Sequence *)allocator.allocate(sizeof(can_interfaces__msg__CANQueue__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = can_interfaces__msg__CANQueue__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
can_interfaces__msg__CANQueue__Sequence__destroy(can_interfaces__msg__CANQueue__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    can_interfaces__msg__CANQueue__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
can_interfaces__msg__CANQueue__Sequence__are_equal(const can_interfaces__msg__CANQueue__Sequence * lhs, const can_interfaces__msg__CANQueue__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!can_interfaces__msg__CANQueue__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
can_interfaces__msg__CANQueue__Sequence__copy(
  const can_interfaces__msg__CANQueue__Sequence * input,
  can_interfaces__msg__CANQueue__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(can_interfaces__msg__CANQueue);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    can_interfaces__msg__CANQueue * data =
      (can_interfaces__msg__CANQueue *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!can_interfaces__msg__CANQueue__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          can_interfaces__msg__CANQueue__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!can_interfaces__msg__CANQueue__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
