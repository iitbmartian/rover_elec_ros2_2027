// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/drive_command.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__STRUCT_HPP_
#define CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__can_interfaces__msg__DriveCommand __attribute__((deprecated))
#else
# define DEPRECATED__can_interfaces__msg__DriveCommand __declspec(deprecated)
#endif

namespace can_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DriveCommand_
{
  using Type = DriveCommand_<ContainerAllocator>;

  explicit DriveCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit DriveCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _drive_direction_type =
    std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>>;
  _drive_direction_type drive_direction;
  using _drive_pwm_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _drive_pwm_type drive_pwm;
  using _explicit_direction_type =
    std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>>;
  _explicit_direction_type explicit_direction;
  using _explicit_pwm_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _explicit_pwm_type explicit_pwm;

  // setters for named parameter idiom
  Type & set__drive_direction(
    const std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>> & _arg)
  {
    this->drive_direction = _arg;
    return *this;
  }
  Type & set__drive_pwm(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->drive_pwm = _arg;
    return *this;
  }
  Type & set__explicit_direction(
    const std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>> & _arg)
  {
    this->explicit_direction = _arg;
    return *this;
  }
  Type & set__explicit_pwm(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->explicit_pwm = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    can_interfaces::msg::DriveCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const can_interfaces::msg::DriveCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      can_interfaces::msg::DriveCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      can_interfaces::msg::DriveCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__can_interfaces__msg__DriveCommand
    std::shared_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__can_interfaces__msg__DriveCommand
    std::shared_ptr<can_interfaces::msg::DriveCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DriveCommand_ & other) const
  {
    if (this->drive_direction != other.drive_direction) {
      return false;
    }
    if (this->drive_pwm != other.drive_pwm) {
      return false;
    }
    if (this->explicit_direction != other.explicit_direction) {
      return false;
    }
    if (this->explicit_pwm != other.explicit_pwm) {
      return false;
    }
    return true;
  }
  bool operator!=(const DriveCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DriveCommand_

// alias to use template instance with default allocator
using DriveCommand =
  can_interfaces::msg::DriveCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace can_interfaces

#endif  // CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__STRUCT_HPP_
