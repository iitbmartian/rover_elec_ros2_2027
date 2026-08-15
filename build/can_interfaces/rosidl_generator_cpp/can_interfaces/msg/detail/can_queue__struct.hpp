// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from can_interfaces:msg/CANQueue.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/can_queue.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__STRUCT_HPP_
#define CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__can_interfaces__msg__CANQueue __attribute__((deprecated))
#else
# define DEPRECATED__can_interfaces__msg__CANQueue __declspec(deprecated)
#endif

namespace can_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CANQueue_
{
  using Type = CANQueue_<ContainerAllocator>;

  explicit CANQueue_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->arb_id = 0l;
    }
  }

  explicit CANQueue_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->arb_id = 0l;
    }
  }

  // field types and members
  using _arb_id_type =
    int32_t;
  _arb_id_type arb_id;
  using _data_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__arb_id(
    const int32_t & _arg)
  {
    this->arb_id = _arg;
    return *this;
  }
  Type & set__data(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    can_interfaces::msg::CANQueue_<ContainerAllocator> *;
  using ConstRawPtr =
    const can_interfaces::msg::CANQueue_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      can_interfaces::msg::CANQueue_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      can_interfaces::msg::CANQueue_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__can_interfaces__msg__CANQueue
    std::shared_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__can_interfaces__msg__CANQueue
    std::shared_ptr<can_interfaces::msg::CANQueue_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CANQueue_ & other) const
  {
    if (this->arb_id != other.arb_id) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const CANQueue_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CANQueue_

// alias to use template instance with default allocator
using CANQueue =
  can_interfaces::msg::CANQueue_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace can_interfaces

#endif  // CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__STRUCT_HPP_
