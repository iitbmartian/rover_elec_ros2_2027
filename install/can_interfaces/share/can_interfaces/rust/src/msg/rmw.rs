#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "can_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__can_interfaces__msg__DriveCommand() -> *const std::ffi::c_void;
}

#[link(name = "can_interfaces__rosidl_generator_c")]
extern "C" {
    fn can_interfaces__msg__DriveCommand__init(msg: *mut DriveCommand) -> bool;
    fn can_interfaces__msg__DriveCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DriveCommand>, size: usize) -> bool;
    fn can_interfaces__msg__DriveCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DriveCommand>);
    fn can_interfaces__msg__DriveCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DriveCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<DriveCommand>) -> bool;
}

// Corresponds to can_interfaces__msg__DriveCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DriveCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_direction: rosidl_runtime_rs::Sequence<bool>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_pwm: rosidl_runtime_rs::Sequence<i32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_direction: rosidl_runtime_rs::Sequence<bool>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_pwm: rosidl_runtime_rs::Sequence<i32>,

}



impl Default for DriveCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !can_interfaces__msg__DriveCommand__init(&mut msg as *mut _) {
        panic!("Call to can_interfaces__msg__DriveCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DriveCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__DriveCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__DriveCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__DriveCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DriveCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DriveCommand where Self: Sized {
  const TYPE_NAME: &'static str = "can_interfaces/msg/DriveCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__can_interfaces__msg__DriveCommand() }
  }
}


#[link(name = "can_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__can_interfaces__msg__CANQueue() -> *const std::ffi::c_void;
}

#[link(name = "can_interfaces__rosidl_generator_c")]
extern "C" {
    fn can_interfaces__msg__CANQueue__init(msg: *mut CANQueue) -> bool;
    fn can_interfaces__msg__CANQueue__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CANQueue>, size: usize) -> bool;
    fn can_interfaces__msg__CANQueue__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CANQueue>);
    fn can_interfaces__msg__CANQueue__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CANQueue>, out_seq: *mut rosidl_runtime_rs::Sequence<CANQueue>) -> bool;
}

// Corresponds to can_interfaces__msg__CANQueue
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CANQueue {

    // This member is not documented.
    #[allow(missing_docs)]
    pub arb_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data: rosidl_runtime_rs::Sequence<i32>,

}



impl Default for CANQueue {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !can_interfaces__msg__CANQueue__init(&mut msg as *mut _) {
        panic!("Call to can_interfaces__msg__CANQueue__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CANQueue {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__CANQueue__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__CANQueue__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__CANQueue__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CANQueue {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CANQueue where Self: Sized {
  const TYPE_NAME: &'static str = "can_interfaces/msg/CANQueue";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__can_interfaces__msg__CANQueue() }
  }
}


#[link(name = "can_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__can_interfaces__msg__MobilityData() -> *const std::ffi::c_void;
}

#[link(name = "can_interfaces__rosidl_generator_c")]
extern "C" {
    fn can_interfaces__msg__MobilityData__init(msg: *mut MobilityData) -> bool;
    fn can_interfaces__msg__MobilityData__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MobilityData>, size: usize) -> bool;
    fn can_interfaces__msg__MobilityData__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MobilityData>);
    fn can_interfaces__msg__MobilityData__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MobilityData>, out_seq: *mut rosidl_runtime_rs::Sequence<MobilityData>) -> bool;
}

// Corresponds to can_interfaces__msg__MobilityData
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MobilityData {

    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_mag_fl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_quad_fl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_imu_fl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_quad_fl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_mag_fr: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_quad_fr: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_imu_fr: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_quad_fr: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_mag_bl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_quad_bl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_imu_bl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_quad_bl: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_mag_br: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_quad_br: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_imu_br: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_quad_br: i32,

}



impl Default for MobilityData {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !can_interfaces__msg__MobilityData__init(&mut msg as *mut _) {
        panic!("Call to can_interfaces__msg__MobilityData__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MobilityData {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__MobilityData__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__MobilityData__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { can_interfaces__msg__MobilityData__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MobilityData {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MobilityData where Self: Sized {
  const TYPE_NAME: &'static str = "can_interfaces/msg/MobilityData";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__can_interfaces__msg__MobilityData() }
  }
}


