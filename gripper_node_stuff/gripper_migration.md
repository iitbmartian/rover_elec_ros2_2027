# Gripper Subsystem — STM32 + ROS2 Migration Notes

Covers: BlackPill (STM32F411CE) firmware, UART bridge to RPi5, and CAN
integration with the rest of the rover's ROS2 stack.

---

## 1. Hardware / Pin Mapping

Board: `YAAJ_BlackPill_Part_Like_SWD_Breakout` (STM32F411CEU6, UFQFPN48)

| Signal              | Pin | Peripheral / Function        |
|---------------------|-----|-------------------------------|
| PWM_SERVO           | PB5 | TIM3_CH2 (PWM out)             |
| PWM_N20             | PB4 | TIM3_CH1 (PWM out)             |
| A (quadrature)      | PA0 | TIM2_CH1 (Encoder Mode)        |
| B (quadrature)      | PA1 | TIM2_CH2 (Encoder Mode)        |
| CURR_SENS_OUT_3V3   | PA2 | ADC1_IN2                       |
| CS / SCK / MISO / MOSI | PA4–PA7 | SPI1 (master)         |
| UART to RPi5 (added)| PA9 (TX), PA10 (RX) | USART1        |

Note: PB4/PB5 share **TIM3**, so N20 and servo PWM share one
frequency/prescaler — no independent tuning between them.

---

## 2. CubeMX / Firmware Notes

- **TIM3 bug found & fixed**: `.ioc` originally had TIM3 Slave Mode =
  *External Clock Mode 1*, which reconfigures CH1/CH2 as clock/trigger
  inputs instead of PWM outputs. Must be **Slave Mode: Disable** with
  Channel1/2 = PWM Generation.
- **TIM2 Encoder Mode**: Combined Channels → Encoder Mode, CH1=PA0,
  CH2=PA1, both polarities Rising, ARR left at max (`0xFFFFFFFF` on
  this 32-bit timer) for full-range wraparound. Not currently
  transmitted over UART/CAN (see Open Items).
- **ADC1**: single channel (IN2/PA2), software-triggered, 12-bit,
  single conversion mode (no DMA).
- **TIM3 PWM frequency**: currently ARR=65535, PSC=0 → timer clock
  72 MHz / 65536 ≈ **1.1 kHz**. Fine for N20, **too fast for a hobby
  servo** (needs ~50 Hz / 20 ms period for standard 1–2 ms pulses).
  Not yet fixed — servo control will not behave correctly until this
  is addressed (separate timer, or correct PSC/ARR pair for 50 Hz if
  N20 whine at that frequency is acceptable).
- **USART1 GPIO config**: added manually in `MX_GPIO_Init` (PA9/PA10,
  AF7, `GPIO_MODE_AF_PP`) because the project's `.ioc` wasn't
  regenerated with USART1 added — no `stm32f4xx_hal_msp.c` on hand to
  edit properly. Recommend adding USART1 in CubeMX and regenerating so
  this moves into `HAL_UART_MspInit` normally.

---

## 3. UART Protocol (STM32 ↔ RPi5)

115200 baud, 8N1, newline-terminated ASCII, interrupt-driven RX
(byte-at-a-time, accumulated until `\n`/`\r`).

**RPi5 → STM32:**
| Line | Meaning |
|---|---|
| `M<uint16>\n` | N20 motor PWM compare value, raw `TIM3_CH1` (0–65535) |
| `S<uint16>\n` | Servo PWM compare value, raw `TIM3_CH2` (0–65535) |

**STM32 → RPi5** (sent every 50 ms):
| Line | Meaning |
|---|---|
| `C<uint32>\n` | Raw ADC1 current sensor reading (PA2, 0–4095) |

All values are raw firmware/timer/ADC counts — **no unit conversion**
(RPM, degrees, mA) happens in firmware or in `gripperrr.py`. Do that
scaling in the ROS layer, and only once the TIM3 frequency issue above
is resolved for the servo.

Firmware source: `main.c` (HAL-generated CubeMX structure, comments
and `USER CODE` markers preserved; additions live in those blocks plus
one new `MX_USART1_UART_Init()` function and `huart1` handle).

---

## 4. ROS2 Nodes

### `gripperrr.py` — UART bridge (runs on RPi5)
- Node name: `gripperrr`
- Params: `port` (default `/dev/ttyUSB0`), `baud` (default `115200`)
- Subscribes: `~/motor_cmd` (`std_msgs/UInt16`), `~/servo_cmd`
  (`std_msgs/UInt16`) → written to STM32 as `M<val>\n` / `S<val>\n`
- Publishes: `~/current_raw` (`std_msgs/UInt32`) ← parsed from
  `C<val>\n` lines
- Background thread reads/parses serial lines; `_write_line()` is
  lock-protected for thread-safe writes from callbacks.
- `destroy_node()` stops the reader thread and closes the serial port.

### `gripper_can.py` — CAN ↔ ROS2 topic bridge
Renamed/re-targeted from an existing `WristCan` pattern. Since the
gripper's STM32 is UART-attached (not CAN-attached like Wrist), this
node doesn't drive hardware directly — it translates between the
rover's CAN bus and `gripperrr`'s topics.

- Node name: `Gripper_CAN`
- **CAN → UART path**: subscribes `can_messages_received`
  (`CanMessage`). On `nodeid == arb.Gripper` and
  `msgtype == arb.gripper_command`, reads `data[0]`/`data[1]` (bytes,
  0–255), scales `×257` to fill the STM32's 16-bit range
  (`255 × 257 = 65535`), publishes to `/gripperrr/motor_cmd` and
  `/gripperrr/servo_cmd`.
- **UART → CAN path**: subscribes `/gripperrr/current_raw`
  (`std_msgs/UInt32`), splits the 12-bit ADC value into low/high
  bytes, publishes a `CanMessage` (`msgtype = arb.gripper_sensor_data`)
  on `can_bus_to_controller` so other CAN-side nodes see gripper
  current.
- Requires `can_controller/arbitration_id.py` to define `Gripper`,
  `gripper_command`, `gripper_sensor_data` (renamed from the `Wrist`
  equivalents — not edited here, file wasn't provided).
- Dropped from the original `WristCan` pattern: the standalone
  `wrist_command` topic (custom `WristPositionCommand` msg) that drove
  Wrist's own CAN-attached actuator directly. For the gripper, CAN
  traffic itself is the inbound command path since the real actuator
  sits behind UART.

### Topic map between the two nodes
```
CAN bus  --(gripper_command)-->  gripper_can  --/gripperrr/motor_cmd-->  gripperrr --UART--> STM32
                                              --/gripperrr/servo_cmd -->
STM32 --UART--> gripperrr --/gripperrr/current_raw--> gripper_can --(gripper_sensor_data)--> CAN bus
```

---

## 5. Open Items / Known Gaps

1. **TIM3 PWM frequency** — shared 1.1 kHz doesn't suit a standard
   hobby servo. Needs a proper prescaler/period choice (or moving N20
   PWM to a different timer if independent frequencies are required).
2. **Encoder telemetry not wired up** — TIM2 quadrature count
   (`__HAL_TIM_GET_COUNTER(&htim2)`) is running in firmware but not
   sent over UART or CAN. Would need a new `E<int32>\n` line in the
   firmware protocol, a subscriber/handler in `gripperrr.py`, and a
   forwarding path in `gripper_can.py`.
3. **`can_controller/arbitration_id.py`** needs `Gripper` /
   `gripper_command` / `gripper_sensor_data` defined — not available
   to edit in this session.
4. **`stm32f4xx_hal_msp.c`** — USART1 GPIO init should be moved from
   the manual block in `MX_GPIO_Init` into `HAL_UART_MspInit` once the
   `.ioc` is regenerated with USART1 added properly.
5. **No scaling/units layer** — all values raw (PWM compare counts,
   ADC counts, CAN bytes). Add real-world unit conversion once PWM
   frequency (item 1) is settled.
