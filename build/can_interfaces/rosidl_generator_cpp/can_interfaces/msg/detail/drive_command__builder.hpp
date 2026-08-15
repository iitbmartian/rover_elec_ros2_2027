// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from can_interfaces:msg/DriveCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/drive_command.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__BUILDER_HPP_
#define CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "can_interfaces/msg/detail/drive_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace can_interfaces
{

namespace msg
{

namespace builder
{

class Init_DriveCommand_explicit_pwm
{
public:
  explicit Init_DriveCommand_explicit_pwm(::can_interfaces::msg::DriveCommand & msg)
  : msg_(msg)
  {}
  ::can_interfaces::msg::DriveCommand explicit_pwm(::can_interfaces::msg::DriveCommand::_explicit_pwm_type arg)
  {
    msg_.explicit_pwm = std::move(arg);
    return std::move(msg_);
  }

private:
  ::can_interfaces::msg::DriveCommand msg_;
};

class Init_DriveCommand_explicit_direction
{
public:
  explicit Init_DriveCommand_explicit_direction(::can_interfaces::msg::DriveCommand & msg)
  : msg_(msg)
  {}
  Init_DriveCommand_explicit_pwm explicit_direction(::can_interfaces::msg::DriveCommand::_explicit_direction_type arg)
  {
    msg_.explicit_direction = std::move(arg);
    return Init_DriveCommand_explicit_pwm(msg_);
  }

private:
  ::can_interfaces::msg::DriveCommand msg_;
};

class Init_DriveCommand_drive_pwm
{
public:
  explicit Init_DriveCommand_drive_pwm(::can_interfaces::msg::DriveCommand & msg)
  : msg_(msg)
  {}
  Init_DriveCommand_explicit_direction drive_pwm(::can_interfaces::msg::DriveCommand::_drive_pwm_type arg)
  {
    msg_.drive_pwm = std::move(arg);
    return Init_DriveCommand_explicit_direction(msg_);
  }

private:
  ::can_interfaces::msg::DriveCommand msg_;
};

class Init_DriveCommand_drive_direction
{
public:
  Init_DriveCommand_drive_direction()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DriveCommand_drive_pwm drive_direction(::can_interfaces::msg::DriveCommand::_drive_direction_type arg)
  {
    msg_.drive_direction = std::move(arg);
    return Init_DriveCommand_drive_pwm(msg_);
  }

private:
  ::can_interfaces::msg::DriveCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::can_interfaces::msg::DriveCommand>()
{
  return can_interfaces::msg::builder::Init_DriveCommand_drive_direction();
}

}  // namespace can_interfaces

#endif  // CAN_INTERFACES__MSG__DETAIL__DRIVE_COMMAND__BUILDER_HPP_
