// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "can_interfaces/msg/detail/drive_command__struct.h"
#include "can_interfaces/msg/detail/drive_command__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool can_interfaces__msg__drive_command__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[47];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("can_interfaces.msg._drive_command.DriveCommand", full_classname_dest, 46) == 0);
  }
  can_interfaces__msg__DriveCommand * ros_message = _ros_message;
  {  // drive_direction
    PyObject * field = PyObject_GetAttrString(_pymsg, "drive_direction");
    if (!field) {
      return false;
    }
    if (PyObject_CheckBuffer(field)) {
      // Optimization for converting arrays of primitives
      Py_buffer view;
      int rc = PyObject_GetBuffer(field, &view, PyBUF_SIMPLE);
      if (rc < 0) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = view.len / sizeof(bool);
      if (!rosidl_runtime_c__boolean__Sequence__init(&(ros_message->drive_direction), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create boolean__Sequence ros_message");
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      bool * dest = ros_message->drive_direction.data;
      rc = PyBuffer_ToContiguous(dest, &view, view.len, 'C');
      if (rc < 0) {
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      PyBuffer_Release(&view);
    } else {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'drive_direction'");
      if (!seq_field) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = PySequence_Size(field);
      if (-1 == size) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      if (!rosidl_runtime_c__boolean__Sequence__init(&(ros_message->drive_direction), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create boolean__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      bool * dest = ros_message->drive_direction.data;
      for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject * item = PySequence_Fast_GET_ITEM(seq_field, i);
        if (!item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        assert(PyBool_Check(item));
        bool tmp = (item == Py_True);
        memcpy(&dest[i], &tmp, sizeof(bool));
      }
      Py_DECREF(seq_field);
    }
    Py_DECREF(field);
  }
  {  // drive_pwm
    PyObject * field = PyObject_GetAttrString(_pymsg, "drive_pwm");
    if (!field) {
      return false;
    }
    if (PyObject_CheckBuffer(field)) {
      // Optimization for converting arrays of primitives
      Py_buffer view;
      int rc = PyObject_GetBuffer(field, &view, PyBUF_SIMPLE);
      if (rc < 0) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = view.len / sizeof(int32_t);
      if (!rosidl_runtime_c__int32__Sequence__init(&(ros_message->drive_pwm), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create int32__Sequence ros_message");
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      int32_t * dest = ros_message->drive_pwm.data;
      rc = PyBuffer_ToContiguous(dest, &view, view.len, 'C');
      if (rc < 0) {
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      PyBuffer_Release(&view);
    } else {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'drive_pwm'");
      if (!seq_field) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = PySequence_Size(field);
      if (-1 == size) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      if (!rosidl_runtime_c__int32__Sequence__init(&(ros_message->drive_pwm), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create int32__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      int32_t * dest = ros_message->drive_pwm.data;
      for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject * item = PySequence_Fast_GET_ITEM(seq_field, i);
        if (!item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        assert(PyLong_Check(item));
        int32_t tmp = (int32_t)PyLong_AsLong(item);
        memcpy(&dest[i], &tmp, sizeof(int32_t));
      }
      Py_DECREF(seq_field);
    }
    Py_DECREF(field);
  }
  {  // explicit_direction
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_direction");
    if (!field) {
      return false;
    }
    if (PyObject_CheckBuffer(field)) {
      // Optimization for converting arrays of primitives
      Py_buffer view;
      int rc = PyObject_GetBuffer(field, &view, PyBUF_SIMPLE);
      if (rc < 0) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = view.len / sizeof(bool);
      if (!rosidl_runtime_c__boolean__Sequence__init(&(ros_message->explicit_direction), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create boolean__Sequence ros_message");
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      bool * dest = ros_message->explicit_direction.data;
      rc = PyBuffer_ToContiguous(dest, &view, view.len, 'C');
      if (rc < 0) {
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      PyBuffer_Release(&view);
    } else {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'explicit_direction'");
      if (!seq_field) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = PySequence_Size(field);
      if (-1 == size) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      if (!rosidl_runtime_c__boolean__Sequence__init(&(ros_message->explicit_direction), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create boolean__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      bool * dest = ros_message->explicit_direction.data;
      for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject * item = PySequence_Fast_GET_ITEM(seq_field, i);
        if (!item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        assert(PyBool_Check(item));
        bool tmp = (item == Py_True);
        memcpy(&dest[i], &tmp, sizeof(bool));
      }
      Py_DECREF(seq_field);
    }
    Py_DECREF(field);
  }
  {  // explicit_pwm
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_pwm");
    if (!field) {
      return false;
    }
    if (PyObject_CheckBuffer(field)) {
      // Optimization for converting arrays of primitives
      Py_buffer view;
      int rc = PyObject_GetBuffer(field, &view, PyBUF_SIMPLE);
      if (rc < 0) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = view.len / sizeof(int32_t);
      if (!rosidl_runtime_c__int32__Sequence__init(&(ros_message->explicit_pwm), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create int32__Sequence ros_message");
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      int32_t * dest = ros_message->explicit_pwm.data;
      rc = PyBuffer_ToContiguous(dest, &view, view.len, 'C');
      if (rc < 0) {
        PyBuffer_Release(&view);
        Py_DECREF(field);
        return false;
      }
      PyBuffer_Release(&view);
    } else {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'explicit_pwm'");
      if (!seq_field) {
        Py_DECREF(field);
        return false;
      }
      Py_ssize_t size = PySequence_Size(field);
      if (-1 == size) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      if (!rosidl_runtime_c__int32__Sequence__init(&(ros_message->explicit_pwm), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create int32__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      int32_t * dest = ros_message->explicit_pwm.data;
      for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject * item = PySequence_Fast_GET_ITEM(seq_field, i);
        if (!item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        assert(PyLong_Check(item));
        int32_t tmp = (int32_t)PyLong_AsLong(item);
        memcpy(&dest[i], &tmp, sizeof(int32_t));
      }
      Py_DECREF(seq_field);
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * can_interfaces__msg__drive_command__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of DriveCommand */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("can_interfaces.msg._drive_command");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "DriveCommand");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  can_interfaces__msg__DriveCommand * ros_message = (can_interfaces__msg__DriveCommand *)raw_ros_message;
  {  // drive_direction
    PyObject * field = NULL;
    size_t size = ros_message->drive_direction.size;
    bool * src = ros_message->drive_direction.data;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    for (size_t i = 0; i < size; ++i) {
      int rc = PyList_SetItem(field, i, PyBool_FromLong(src[i] ? 1 : 0));
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "drive_direction", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // drive_pwm
    PyObject * field = NULL;
    field = PyObject_GetAttrString(_pymessage, "drive_pwm");
    if (!field) {
      return NULL;
    }
    assert(field->ob_type != NULL);
    assert(field->ob_type->tp_name != NULL);
    assert(strcmp(field->ob_type->tp_name, "array.array") == 0);
    // ensure that itemsize matches the sizeof of the ROS message field
    PyObject * itemsize_attr = PyObject_GetAttrString(field, "itemsize");
    assert(itemsize_attr != NULL);
    size_t itemsize = PyLong_AsSize_t(itemsize_attr);
    Py_DECREF(itemsize_attr);
    if (itemsize != sizeof(int32_t)) {
      PyErr_SetString(PyExc_RuntimeError, "itemsize doesn't match expectation");
      Py_DECREF(field);
      return NULL;
    }
    // clear the array, poor approach to remove potential default values
    Py_ssize_t length = PyObject_Length(field);
    if (-1 == length) {
      Py_DECREF(field);
      return NULL;
    }
    if (length > 0) {
      PyObject * pop = PyObject_GetAttrString(field, "pop");
      assert(pop != NULL);
      for (Py_ssize_t i = 0; i < length; ++i) {
        PyObject * ret = PyObject_CallFunctionObjArgs(pop, NULL);
        if (!ret) {
          Py_DECREF(pop);
          Py_DECREF(field);
          return NULL;
        }
        Py_DECREF(ret);
      }
      Py_DECREF(pop);
    }
    if (ros_message->drive_pwm.size > 0) {
      // populating the array.array using the frombytes method
      PyObject * frombytes = PyObject_GetAttrString(field, "frombytes");
      assert(frombytes != NULL);
      int32_t * src = &(ros_message->drive_pwm.data[0]);
      PyObject * data = PyBytes_FromStringAndSize((const char *)src, ros_message->drive_pwm.size * sizeof(int32_t));
      assert(data != NULL);
      PyObject * ret = PyObject_CallFunctionObjArgs(frombytes, data, NULL);
      Py_DECREF(data);
      Py_DECREF(frombytes);
      if (!ret) {
        Py_DECREF(field);
        return NULL;
      }
      Py_DECREF(ret);
    }
    Py_DECREF(field);
  }
  {  // explicit_direction
    PyObject * field = NULL;
    size_t size = ros_message->explicit_direction.size;
    bool * src = ros_message->explicit_direction.data;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    for (size_t i = 0; i < size; ++i) {
      int rc = PyList_SetItem(field, i, PyBool_FromLong(src[i] ? 1 : 0));
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_direction", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_pwm
    PyObject * field = NULL;
    field = PyObject_GetAttrString(_pymessage, "explicit_pwm");
    if (!field) {
      return NULL;
    }
    assert(field->ob_type != NULL);
    assert(field->ob_type->tp_name != NULL);
    assert(strcmp(field->ob_type->tp_name, "array.array") == 0);
    // ensure that itemsize matches the sizeof of the ROS message field
    PyObject * itemsize_attr = PyObject_GetAttrString(field, "itemsize");
    assert(itemsize_attr != NULL);
    size_t itemsize = PyLong_AsSize_t(itemsize_attr);
    Py_DECREF(itemsize_attr);
    if (itemsize != sizeof(int32_t)) {
      PyErr_SetString(PyExc_RuntimeError, "itemsize doesn't match expectation");
      Py_DECREF(field);
      return NULL;
    }
    // clear the array, poor approach to remove potential default values
    Py_ssize_t length = PyObject_Length(field);
    if (-1 == length) {
      Py_DECREF(field);
      return NULL;
    }
    if (length > 0) {
      PyObject * pop = PyObject_GetAttrString(field, "pop");
      assert(pop != NULL);
      for (Py_ssize_t i = 0; i < length; ++i) {
        PyObject * ret = PyObject_CallFunctionObjArgs(pop, NULL);
        if (!ret) {
          Py_DECREF(pop);
          Py_DECREF(field);
          return NULL;
        }
        Py_DECREF(ret);
      }
      Py_DECREF(pop);
    }
    if (ros_message->explicit_pwm.size > 0) {
      // populating the array.array using the frombytes method
      PyObject * frombytes = PyObject_GetAttrString(field, "frombytes");
      assert(frombytes != NULL);
      int32_t * src = &(ros_message->explicit_pwm.data[0]);
      PyObject * data = PyBytes_FromStringAndSize((const char *)src, ros_message->explicit_pwm.size * sizeof(int32_t));
      assert(data != NULL);
      PyObject * ret = PyObject_CallFunctionObjArgs(frombytes, data, NULL);
      Py_DECREF(data);
      Py_DECREF(frombytes);
      if (!ret) {
        Py_DECREF(field);
        return NULL;
      }
      Py_DECREF(ret);
    }
    Py_DECREF(field);
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
