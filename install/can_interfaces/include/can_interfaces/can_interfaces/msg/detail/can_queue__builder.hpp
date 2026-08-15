// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from can_interfaces:msg/CANQueue.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/can_queue.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__BUILDER_HPP_
#define CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "can_interfaces/msg/detail/can_queue__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace can_interfaces
{

namespace msg
{

namespace builder
{

class Init_CANQueue_data
{
public:
  explicit Init_CANQueue_data(::can_interfaces::msg::CANQueue & msg)
  : msg_(msg)
  {}
  ::can_interfaces::msg::CANQueue data(::can_interfaces::msg::CANQueue::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::can_interfaces::msg::CANQueue msg_;
};

class Init_CANQueue_arb_id
{
public:
  Init_CANQueue_arb_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CANQueue_data arb_id(::can_interfaces::msg::CANQueue::_arb_id_type arg)
  {
    msg_.arb_id = std::move(arg);
    return Init_CANQueue_data(msg_);
  }

private:
  ::can_interfaces::msg::CANQueue msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::can_interfaces::msg::CANQueue>()
{
  return can_interfaces::msg::builder::Init_CANQueue_arb_id();
}

}  // namespace can_interfaces

#endif  // CAN_INTERFACES__MSG__DETAIL__CAN_QUEUE__BUILDER_HPP_
