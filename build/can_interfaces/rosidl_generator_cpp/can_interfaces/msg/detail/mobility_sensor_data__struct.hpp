// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from can_interfaces:msg/MobilitySensorData.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/mobility_sensor_data.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__STRUCT_HPP_
#define CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__can_interfaces__msg__MobilitySensorData __attribute__((deprecated))
#else
# define DEPRECATED__can_interfaces__msg__MobilitySensorData __declspec(deprecated)
#endif

namespace can_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MobilitySensorData_
{
  using Type = MobilitySensorData_<ContainerAllocator>;

  explicit MobilitySensorData_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->explicit_mag_fl = 0l;
      this->explicit_quad_fl = 0l;
      this->explicit_imu_fl = 0l;
      this->drive_quad_fl = 0l;
      this->explicit_mag_fr = 0l;
      this->explicit_quad_fr = 0l;
      this->explicit_imu_fr = 0l;
      this->drive_quad_fr = 0l;
      this->explicit_mag_bl = 0l;
      this->explicit_quad_bl = 0l;
      this->explicit_imu_bl = 0l;
      this->drive_quad_bl = 0l;
      this->explicit_mag_br = 0l;
      this->explicit_quad_br = 0l;
      this->explicit_imu_br = 0l;
      this->drive_quad_br = 0l;
    }
  }

  explicit MobilitySensorData_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->explicit_mag_fl = 0l;
      this->explicit_quad_fl = 0l;
      this->explicit_imu_fl = 0l;
      this->drive_quad_fl = 0l;
      this->explicit_mag_fr = 0l;
      this->explicit_quad_fr = 0l;
      this->explicit_imu_fr = 0l;
      this->drive_quad_fr = 0l;
      this->explicit_mag_bl = 0l;
      this->explicit_quad_bl = 0l;
      this->explicit_imu_bl = 0l;
      this->drive_quad_bl = 0l;
      this->explicit_mag_br = 0l;
      this->explicit_quad_br = 0l;
      this->explicit_imu_br = 0l;
      this->drive_quad_br = 0l;
    }
  }

  // field types and members
  using _explicit_mag_fl_type =
    int32_t;
  _explicit_mag_fl_type explicit_mag_fl;
  using _explicit_quad_fl_type =
    int32_t;
  _explicit_quad_fl_type explicit_quad_fl;
  using _explicit_imu_fl_type =
    int32_t;
  _explicit_imu_fl_type explicit_imu_fl;
  using _drive_quad_fl_type =
    int32_t;
  _drive_quad_fl_type drive_quad_fl;
  using _explicit_mag_fr_type =
    int32_t;
  _explicit_mag_fr_type explicit_mag_fr;
  using _explicit_quad_fr_type =
    int32_t;
  _explicit_quad_fr_type explicit_quad_fr;
  using _explicit_imu_fr_type =
    int32_t;
  _explicit_imu_fr_type explicit_imu_fr;
  using _drive_quad_fr_type =
    int32_t;
  _drive_quad_fr_type drive_quad_fr;
  using _explicit_mag_bl_type =
    int32_t;
  _explicit_mag_bl_type explicit_mag_bl;
  using _explicit_quad_bl_type =
    int32_t;
  _explicit_quad_bl_type explicit_quad_bl;
  using _explicit_imu_bl_type =
    int32_t;
  _explicit_imu_bl_type explicit_imu_bl;
  using _drive_quad_bl_type =
    int32_t;
  _drive_quad_bl_type drive_quad_bl;
  using _explicit_mag_br_type =
    int32_t;
  _explicit_mag_br_type explicit_mag_br;
  using _explicit_quad_br_type =
    int32_t;
  _explicit_quad_br_type explicit_quad_br;
  using _explicit_imu_br_type =
    int32_t;
  _explicit_imu_br_type explicit_imu_br;
  using _drive_quad_br_type =
    int32_t;
  _drive_quad_br_type drive_quad_br;

  // setters for named parameter idiom
  Type & set__explicit_mag_fl(
    const int32_t & _arg)
  {
    this->explicit_mag_fl = _arg;
    return *this;
  }
  Type & set__explicit_quad_fl(
    const int32_t & _arg)
  {
    this->explicit_quad_fl = _arg;
    return *this;
  }
  Type & set__explicit_imu_fl(
    const int32_t & _arg)
  {
    this->explicit_imu_fl = _arg;
    return *this;
  }
  Type & set__drive_quad_fl(
    const int32_t & _arg)
  {
    this->drive_quad_fl = _arg;
    return *this;
  }
  Type & set__explicit_mag_fr(
    const int32_t & _arg)
  {
    this->explicit_mag_fr = _arg;
    return *this;
  }
  Type & set__explicit_quad_fr(
    const int32_t & _arg)
  {
    this->explicit_quad_fr = _arg;
    return *this;
  }
  Type & set__explicit_imu_fr(
    const int32_t & _arg)
  {
    this->explicit_imu_fr = _arg;
    return *this;
  }
  Type & set__drive_quad_fr(
    const int32_t & _arg)
  {
    this->drive_quad_fr = _arg;
    return *this;
  }
  Type & set__explicit_mag_bl(
    const int32_t & _arg)
  {
    this->explicit_mag_bl = _arg;
    return *this;
  }
  Type & set__explicit_quad_bl(
    const int32_t & _arg)
  {
    this->explicit_quad_bl = _arg;
    return *this;
  }
  Type & set__explicit_imu_bl(
    const int32_t & _arg)
  {
    this->explicit_imu_bl = _arg;
    return *this;
  }
  Type & set__drive_quad_bl(
    const int32_t & _arg)
  {
    this->drive_quad_bl = _arg;
    return *this;
  }
  Type & set__explicit_mag_br(
    const int32_t & _arg)
  {
    this->explicit_mag_br = _arg;
    return *this;
  }
  Type & set__explicit_quad_br(
    const int32_t & _arg)
  {
    this->explicit_quad_br = _arg;
    return *this;
  }
  Type & set__explicit_imu_br(
    const int32_t & _arg)
  {
    this->explicit_imu_br = _arg;
    return *this;
  }
  Type & set__drive_quad_br(
    const int32_t & _arg)
  {
    this->drive_quad_br = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    can_interfaces::msg::MobilitySensorData_<ContainerAllocator> *;
  using ConstRawPtr =
    const can_interfaces::msg::MobilitySensorData_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      can_interfaces::msg::MobilitySensorData_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      can_interfaces::msg::MobilitySensorData_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__can_interfaces__msg__MobilitySensorData
    std::shared_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__can_interfaces__msg__MobilitySensorData
    std::shared_ptr<can_interfaces::msg::MobilitySensorData_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MobilitySensorData_ & other) const
  {
    if (this->explicit_mag_fl != other.explicit_mag_fl) {
      return false;
    }
    if (this->explicit_quad_fl != other.explicit_quad_fl) {
      return false;
    }
    if (this->explicit_imu_fl != other.explicit_imu_fl) {
      return false;
    }
    if (this->drive_quad_fl != other.drive_quad_fl) {
      return false;
    }
    if (this->explicit_mag_fr != other.explicit_mag_fr) {
      return false;
    }
    if (this->explicit_quad_fr != other.explicit_quad_fr) {
      return false;
    }
    if (this->explicit_imu_fr != other.explicit_imu_fr) {
      return false;
    }
    if (this->drive_quad_fr != other.drive_quad_fr) {
      return false;
    }
    if (this->explicit_mag_bl != other.explicit_mag_bl) {
      return false;
    }
    if (this->explicit_quad_bl != other.explicit_quad_bl) {
      return false;
    }
    if (this->explicit_imu_bl != other.explicit_imu_bl) {
      return false;
    }
    if (this->drive_quad_bl != other.drive_quad_bl) {
      return false;
    }
    if (this->explicit_mag_br != other.explicit_mag_br) {
      return false;
    }
    if (this->explicit_quad_br != other.explicit_quad_br) {
      return false;
    }
    if (this->explicit_imu_br != other.explicit_imu_br) {
      return false;
    }
    if (this->drive_quad_br != other.drive_quad_br) {
      return false;
    }
    return true;
  }
  bool operator!=(const MobilitySensorData_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MobilitySensorData_

// alias to use template instance with default allocator
using MobilitySensorData =
  can_interfaces::msg::MobilitySensorData_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace can_interfaces

#endif  // CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__STRUCT_HPP_
