// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from can_interfaces:msg/MobilitySensorData.idl
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
#include "can_interfaces/msg/detail/mobility_sensor_data__struct.h"
#include "can_interfaces/msg/detail/mobility_sensor_data__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool can_interfaces__msg__mobility_sensor_data__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[60];
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
    assert(strncmp("can_interfaces.msg._mobility_sensor_data.MobilitySensorData", full_classname_dest, 59) == 0);
  }
  can_interfaces__msg__MobilitySensorData * ros_message = _ros_message;
  {  // explicit_mag_fl
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_mag_fl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_mag_fl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_quad_fl
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_quad_fl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_quad_fl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_imu_fl
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_imu_fl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_imu_fl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // drive_quad_fl
    PyObject * field = PyObject_GetAttrString(_pymsg, "drive_quad_fl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->drive_quad_fl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_mag_fr
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_mag_fr");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_mag_fr = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_quad_fr
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_quad_fr");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_quad_fr = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_imu_fr
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_imu_fr");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_imu_fr = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // drive_quad_fr
    PyObject * field = PyObject_GetAttrString(_pymsg, "drive_quad_fr");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->drive_quad_fr = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_mag_bl
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_mag_bl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_mag_bl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_quad_bl
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_quad_bl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_quad_bl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_imu_bl
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_imu_bl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_imu_bl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // drive_quad_bl
    PyObject * field = PyObject_GetAttrString(_pymsg, "drive_quad_bl");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->drive_quad_bl = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_mag_br
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_mag_br");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_mag_br = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_quad_br
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_quad_br");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_quad_br = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // explicit_imu_br
    PyObject * field = PyObject_GetAttrString(_pymsg, "explicit_imu_br");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->explicit_imu_br = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // drive_quad_br
    PyObject * field = PyObject_GetAttrString(_pymsg, "drive_quad_br");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->drive_quad_br = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * can_interfaces__msg__mobility_sensor_data__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of MobilitySensorData */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("can_interfaces.msg._mobility_sensor_data");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "MobilitySensorData");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  can_interfaces__msg__MobilitySensorData * ros_message = (can_interfaces__msg__MobilitySensorData *)raw_ros_message;
  {  // explicit_mag_fl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_mag_fl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_mag_fl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_quad_fl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_quad_fl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_quad_fl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_imu_fl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_imu_fl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_imu_fl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // drive_quad_fl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->drive_quad_fl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "drive_quad_fl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_mag_fr
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_mag_fr);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_mag_fr", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_quad_fr
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_quad_fr);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_quad_fr", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_imu_fr
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_imu_fr);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_imu_fr", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // drive_quad_fr
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->drive_quad_fr);
    {
      int rc = PyObject_SetAttrString(_pymessage, "drive_quad_fr", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_mag_bl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_mag_bl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_mag_bl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_quad_bl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_quad_bl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_quad_bl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_imu_bl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_imu_bl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_imu_bl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // drive_quad_bl
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->drive_quad_bl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "drive_quad_bl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_mag_br
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_mag_br);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_mag_br", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_quad_br
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_quad_br);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_quad_br", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // explicit_imu_br
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->explicit_imu_br);
    {
      int rc = PyObject_SetAttrString(_pymessage, "explicit_imu_br", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // drive_quad_br
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->drive_quad_br);
    {
      int rc = PyObject_SetAttrString(_pymessage, "drive_quad_br", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
