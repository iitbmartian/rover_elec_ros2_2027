#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to can_interfaces__msg__DriveCommand

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DriveCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_direction: Vec<bool>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drive_pwm: Vec<i32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_direction: Vec<bool>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub explicit_pwm: Vec<i32>,

}



impl Default for DriveCommand {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DriveCommand::default())
  }
}

impl rosidl_runtime_rs::Message for DriveCommand {
  type RmwMsg = super::msg::rmw::DriveCommand;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        drive_direction: msg.drive_direction.into(),
        drive_pwm: msg.drive_pwm.into(),
        explicit_direction: msg.explicit_direction.into(),
        explicit_pwm: msg.explicit_pwm.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        drive_direction: msg.drive_direction.as_slice().into(),
        drive_pwm: msg.drive_pwm.as_slice().into(),
        explicit_direction: msg.explicit_direction.as_slice().into(),
        explicit_pwm: msg.explicit_pwm.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      drive_direction: msg.drive_direction
          .into_iter()
          .collect(),
      drive_pwm: msg.drive_pwm
          .into_iter()
          .collect(),
      explicit_direction: msg.explicit_direction
          .into_iter()
          .collect(),
      explicit_pwm: msg.explicit_pwm
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to can_interfaces__msg__CANQueue

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CANQueue {

    // This member is not documented.
    #[allow(missing_docs)]
    pub arb_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data: Vec<i32>,

}



impl Default for CANQueue {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::CANQueue::default())
  }
}

impl rosidl_runtime_rs::Message for CANQueue {
  type RmwMsg = super::msg::rmw::CANQueue;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        arb_id: msg.arb_id,
        data: msg.data.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      arb_id: msg.arb_id,
        data: msg.data.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      arb_id: msg.arb_id,
      data: msg.data
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to can_interfaces__msg__MobilityData

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MobilityData::default())
  }
}

impl rosidl_runtime_rs::Message for MobilityData {
  type RmwMsg = super::msg::rmw::MobilityData;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        explicit_mag_fl: msg.explicit_mag_fl,
        explicit_quad_fl: msg.explicit_quad_fl,
        explicit_imu_fl: msg.explicit_imu_fl,
        drive_quad_fl: msg.drive_quad_fl,
        explicit_mag_fr: msg.explicit_mag_fr,
        explicit_quad_fr: msg.explicit_quad_fr,
        explicit_imu_fr: msg.explicit_imu_fr,
        drive_quad_fr: msg.drive_quad_fr,
        explicit_mag_bl: msg.explicit_mag_bl,
        explicit_quad_bl: msg.explicit_quad_bl,
        explicit_imu_bl: msg.explicit_imu_bl,
        drive_quad_bl: msg.drive_quad_bl,
        explicit_mag_br: msg.explicit_mag_br,
        explicit_quad_br: msg.explicit_quad_br,
        explicit_imu_br: msg.explicit_imu_br,
        drive_quad_br: msg.drive_quad_br,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      explicit_mag_fl: msg.explicit_mag_fl,
      explicit_quad_fl: msg.explicit_quad_fl,
      explicit_imu_fl: msg.explicit_imu_fl,
      drive_quad_fl: msg.drive_quad_fl,
      explicit_mag_fr: msg.explicit_mag_fr,
      explicit_quad_fr: msg.explicit_quad_fr,
      explicit_imu_fr: msg.explicit_imu_fr,
      drive_quad_fr: msg.drive_quad_fr,
      explicit_mag_bl: msg.explicit_mag_bl,
      explicit_quad_bl: msg.explicit_quad_bl,
      explicit_imu_bl: msg.explicit_imu_bl,
      drive_quad_bl: msg.drive_quad_bl,
      explicit_mag_br: msg.explicit_mag_br,
      explicit_quad_br: msg.explicit_quad_br,
      explicit_imu_br: msg.explicit_imu_br,
      drive_quad_br: msg.drive_quad_br,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      explicit_mag_fl: msg.explicit_mag_fl,
      explicit_quad_fl: msg.explicit_quad_fl,
      explicit_imu_fl: msg.explicit_imu_fl,
      drive_quad_fl: msg.drive_quad_fl,
      explicit_mag_fr: msg.explicit_mag_fr,
      explicit_quad_fr: msg.explicit_quad_fr,
      explicit_imu_fr: msg.explicit_imu_fr,
      drive_quad_fr: msg.drive_quad_fr,
      explicit_mag_bl: msg.explicit_mag_bl,
      explicit_quad_bl: msg.explicit_quad_bl,
      explicit_imu_bl: msg.explicit_imu_bl,
      drive_quad_bl: msg.drive_quad_bl,
      explicit_mag_br: msg.explicit_mag_br,
      explicit_quad_br: msg.explicit_quad_br,
      explicit_imu_br: msg.explicit_imu_br,
      drive_quad_br: msg.drive_quad_br,
    }
  }
}


