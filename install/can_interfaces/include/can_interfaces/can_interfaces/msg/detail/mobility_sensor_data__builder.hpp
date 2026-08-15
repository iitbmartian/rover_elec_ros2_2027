// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from can_interfaces:msg/MobilitySensorData.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "can_interfaces/msg/mobility_sensor_data.hpp"


#ifndef CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__BUILDER_HPP_
#define CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "can_interfaces/msg/detail/mobility_sensor_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace can_interfaces
{

namespace msg
{

namespace builder
{

class Init_MobilitySensorData_drive_quad_br
{
public:
  explicit Init_MobilitySensorData_drive_quad_br(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  ::can_interfaces::msg::MobilitySensorData drive_quad_br(::can_interfaces::msg::MobilitySensorData::_drive_quad_br_type arg)
  {
    msg_.drive_quad_br = std::move(arg);
    return std::move(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_imu_br
{
public:
  explicit Init_MobilitySensorData_explicit_imu_br(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_drive_quad_br explicit_imu_br(::can_interfaces::msg::MobilitySensorData::_explicit_imu_br_type arg)
  {
    msg_.explicit_imu_br = std::move(arg);
    return Init_MobilitySensorData_drive_quad_br(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_quad_br
{
public:
  explicit Init_MobilitySensorData_explicit_quad_br(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_imu_br explicit_quad_br(::can_interfaces::msg::MobilitySensorData::_explicit_quad_br_type arg)
  {
    msg_.explicit_quad_br = std::move(arg);
    return Init_MobilitySensorData_explicit_imu_br(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_mag_br
{
public:
  explicit Init_MobilitySensorData_explicit_mag_br(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_quad_br explicit_mag_br(::can_interfaces::msg::MobilitySensorData::_explicit_mag_br_type arg)
  {
    msg_.explicit_mag_br = std::move(arg);
    return Init_MobilitySensorData_explicit_quad_br(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_drive_quad_bl
{
public:
  explicit Init_MobilitySensorData_drive_quad_bl(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_mag_br drive_quad_bl(::can_interfaces::msg::MobilitySensorData::_drive_quad_bl_type arg)
  {
    msg_.drive_quad_bl = std::move(arg);
    return Init_MobilitySensorData_explicit_mag_br(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_imu_bl
{
public:
  explicit Init_MobilitySensorData_explicit_imu_bl(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_drive_quad_bl explicit_imu_bl(::can_interfaces::msg::MobilitySensorData::_explicit_imu_bl_type arg)
  {
    msg_.explicit_imu_bl = std::move(arg);
    return Init_MobilitySensorData_drive_quad_bl(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_quad_bl
{
public:
  explicit Init_MobilitySensorData_explicit_quad_bl(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_imu_bl explicit_quad_bl(::can_interfaces::msg::MobilitySensorData::_explicit_quad_bl_type arg)
  {
    msg_.explicit_quad_bl = std::move(arg);
    return Init_MobilitySensorData_explicit_imu_bl(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_mag_bl
{
public:
  explicit Init_MobilitySensorData_explicit_mag_bl(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_quad_bl explicit_mag_bl(::can_interfaces::msg::MobilitySensorData::_explicit_mag_bl_type arg)
  {
    msg_.explicit_mag_bl = std::move(arg);
    return Init_MobilitySensorData_explicit_quad_bl(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_drive_quad_fr
{
public:
  explicit Init_MobilitySensorData_drive_quad_fr(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_mag_bl drive_quad_fr(::can_interfaces::msg::MobilitySensorData::_drive_quad_fr_type arg)
  {
    msg_.drive_quad_fr = std::move(arg);
    return Init_MobilitySensorData_explicit_mag_bl(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_imu_fr
{
public:
  explicit Init_MobilitySensorData_explicit_imu_fr(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_drive_quad_fr explicit_imu_fr(::can_interfaces::msg::MobilitySensorData::_explicit_imu_fr_type arg)
  {
    msg_.explicit_imu_fr = std::move(arg);
    return Init_MobilitySensorData_drive_quad_fr(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_quad_fr
{
public:
  explicit Init_MobilitySensorData_explicit_quad_fr(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_imu_fr explicit_quad_fr(::can_interfaces::msg::MobilitySensorData::_explicit_quad_fr_type arg)
  {
    msg_.explicit_quad_fr = std::move(arg);
    return Init_MobilitySensorData_explicit_imu_fr(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_mag_fr
{
public:
  explicit Init_MobilitySensorData_explicit_mag_fr(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_quad_fr explicit_mag_fr(::can_interfaces::msg::MobilitySensorData::_explicit_mag_fr_type arg)
  {
    msg_.explicit_mag_fr = std::move(arg);
    return Init_MobilitySensorData_explicit_quad_fr(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_drive_quad_fl
{
public:
  explicit Init_MobilitySensorData_drive_quad_fl(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_mag_fr drive_quad_fl(::can_interfaces::msg::MobilitySensorData::_drive_quad_fl_type arg)
  {
    msg_.drive_quad_fl = std::move(arg);
    return Init_MobilitySensorData_explicit_mag_fr(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_imu_fl
{
public:
  explicit Init_MobilitySensorData_explicit_imu_fl(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_drive_quad_fl explicit_imu_fl(::can_interfaces::msg::MobilitySensorData::_explicit_imu_fl_type arg)
  {
    msg_.explicit_imu_fl = std::move(arg);
    return Init_MobilitySensorData_drive_quad_fl(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_quad_fl
{
public:
  explicit Init_MobilitySensorData_explicit_quad_fl(::can_interfaces::msg::MobilitySensorData & msg)
  : msg_(msg)
  {}
  Init_MobilitySensorData_explicit_imu_fl explicit_quad_fl(::can_interfaces::msg::MobilitySensorData::_explicit_quad_fl_type arg)
  {
    msg_.explicit_quad_fl = std::move(arg);
    return Init_MobilitySensorData_explicit_imu_fl(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

class Init_MobilitySensorData_explicit_mag_fl
{
public:
  Init_MobilitySensorData_explicit_mag_fl()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MobilitySensorData_explicit_quad_fl explicit_mag_fl(::can_interfaces::msg::MobilitySensorData::_explicit_mag_fl_type arg)
  {
    msg_.explicit_mag_fl = std::move(arg);
    return Init_MobilitySensorData_explicit_quad_fl(msg_);
  }

private:
  ::can_interfaces::msg::MobilitySensorData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::can_interfaces::msg::MobilitySensorData>()
{
  return can_interfaces::msg::builder::Init_MobilitySensorData_explicit_mag_fl();
}

}  // namespace can_interfaces

#endif  // CAN_INTERFACES__MSG__DETAIL__MOBILITY_SENSOR_DATA__BUILDER_HPP_
