/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
/*
 * MCP2515-over-SPI1 driver, same library used by the rest of the rover's
 * CAN nodes (see gripper_migration.md / stm_reference). Provides uCAN_MSG,
 * dSTANDARD_CAN_MSG_ID_2_0B, and CANSPI_Initialize/Transmit/Receive().
 * Not included in this session - add the project's existing CANSPI.h/.c
 * (whatever the other CAN boards use) to this sketch/project before
 * building.
 */
#include "CANSPI.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/*
 * ---- CAN arbitration IDs (PLACEHOLDER) ----
 * can_controller/arbitration_id.py (the rover-wide nodeid/msgtype scheme
 * that gripperrr.py's arb.Gripper / arb.gripper_command / arb.sensor_data
 * reference) was not available in this session - see gripper_migration.md
 * Open Item 3. The values below are placeholders composed as
 * (nodeid << 6) | msgtype, then masked to 11 bits the same way
 * stm_reference's cast_to_arbid() does. MUST be reconciled with the real
 * arbitration_id.py values before this is trusted on the physical bus -
 * a collision with another node's ID here would cause silent cross-talk.
 */
#define GRIPPER_NODE_ID            0x05U  /* TODO: real arb.Gripper value */
#define MSGTYPE_GRIPPER_COMMAND    0x01U  /* TODO: real arb.gripper_command value */
#define MSGTYPE_SENSOR_DATA        0x02U  /* TODO: real arb.sensor_data value */
#define MSGTYPE_HEARTBEAT          0x3EU  /* TODO: rover-wide heartbeat convention */
#define MSGTYPE_START_NODE         0x3FU  /* TODO: rover-wide start/handshake convention */
#define MSGTYPE_SENSOR_CHECK       0x3DU  /* TODO: rover-wide sensor-check convention */

#define CAN_ARB_ID(nodeid, msgtype) \
  ((uint16_t)(((uint16_t)(nodeid) << 6 | (uint16_t)(msgtype)) & 0x7FFU))

#define gripper_command_msg  CAN_ARB_ID(GRIPPER_NODE_ID, MSGTYPE_GRIPPER_COMMAND)
#define sensor_data_msg      CAN_ARB_ID(GRIPPER_NODE_ID, MSGTYPE_SENSOR_DATA)
#define heartbeat_msg        CAN_ARB_ID(GRIPPER_NODE_ID, MSGTYPE_HEARTBEAT)
#define start_node_msg       CAN_ARB_ID(GRIPPER_NODE_ID, MSGTYPE_START_NODE)
#define sensor_check_msg     CAN_ARB_ID(GRIPPER_NODE_ID, MSGTYPE_SENSOR_CHECK)

/* Watchdog: if this many main-loop iterations pass with no CAN frame
 * received at all, assume the bus/supervisor is gone, zero the outputs,
 * and require a fresh start_node handshake before actuating again -
 * mirrors stm_reference's CAN_failed_counter pattern exactly. */
#define CAN_FAILED_THRESHOLD       10000U

/* Sensor telemetry (GripperEncoders equivalent) broadcast period. */
#define SENSOR_BROADCAST_PERIOD_MS 50U

/* PWM: TIM3 fixed to a real 50Hz/20ms servo-rate period (see main.c review
 * doc - the original ARR=65535/PSC=0 gave ~1.1kHz, which is far too fast
 * for a hobby servo and was flagged as an unresolved bug in
 * gripper_migration.md). At 72MHz APB1 timer clock, PSC=71 gives a 1MHz
 * (1us/tick) counter; ARR=19999 gives a 20000us=20ms period. N20 and servo
 * share this timer/period (PB4/PB5 are only ever TIM3_CH1/CH2 on this
 * package - no alternate timer is available on those pins), so N20 now
 * also runs at 50Hz; per the md this is an accepted trade-off if N20
 * doesn't audibly whine at that rate - re-verify on hardware.
 */
#define SERVO_PWM_PERIOD_TICKS     20000U  /* ARR+1, i.e. 20ms at 1us/tick */
#define SERVO_PULSE_MIN_US         500U
#define SERVO_PULSE_MAX_US         2400U
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;

SPI_HandleTypeDef hspi1;

TIM_HandleTypeDef htim1;
TIM_HandleTypeDef htim2;
TIM_HandleTypeDef htim3;

/* USER CODE BEGIN PV */
/*
 * Gripper CAN protocol (matches gripperrr.py's GripperPositionCommand /
 * GripperEncoders exactly):
 *
 * ROS -> STM32 (gripper_command_msg, dlc=2):
 *   data0 = dcm1  N20 motor command, 0-255 raw byte
 *   data1 = dcm2  Servo command,     0-255 raw byte
 *   ("0 is horizontal wrt gearbox and parallel to gearbox" per
 *   gripperrr.py's own comment on dcm1/dcm2 - dcm2 is treated below as a
 *   linear 0-255 -> SERVO_PULSE_MIN_US..MAX_US mapping accordingly.)
 *
 * STM32 -> ROS (sensor_data_msg, dlc=5, every SENSOR_BROADCAST_PERIOD_MS):
 *   data0 = quad_1     TIM2 quadrature encoder count, low byte of the
 *                       running count (only real encoder on this board -
 *                       see note on quad_2 below)
 *   data1 = quad_2      always 0 - this board has only ONE quadrature
 *                       encoder (TIM2, PA0/PA1). GripperEncoders/
 *                       GripperPositionCommand's dual quad_1/quad_2 +
 *                       acs_1/acs_2 shape implies a 2-motor-with-feedback
 *                       board; gripper_migration.md's hardware table only
 *                       documents one encoder + one ADC channel. Needs
 *                       reconciling with whoever owns the message
 *                       definition - not fabricated here.
 *   data2 = acs_1      ADC1/PA2 current sensor reading (12-bit, so this
 *                       alone loses range - see review doc)
 *   data3 = acs_2      always 0 - no second current-sense channel wired
 *                       on this board (see quad_2 note above)
 *   data4 = up_check    always 0 - no discrete status/limit-switch inputs
 *                       are documented on this board; gripperrr.py unpacks
 *                       this as 4 bits, meaning matters TBD
 */
volatile uint8_t dcm1 = 0;    /* N20 motor command, 0-255 */
volatile uint8_t dcm2 = 128;  /* Servo command, 0-255, ~center on boot */

uCAN_MSG rx;
uCAN_MSG tx_heartbeat;
uCAN_MSG tx_sensor;

volatile bool beat_pls = false;
volatile uint8_t heartbeater = 0;

volatile bool start_node = false;
volatile bool start_node_init = false;
volatile uint32_t CAN_failed_counter = 0;

bool CAN_checker = false;
uint32_t lastSensorBroadcastTick = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_SPI1_Init(void);
static void MX_TIM3_Init(void);
static void MX_ADC1_Init(void);
static void MX_TIM2_Init(void);
static void MX_TIM1_Init(void);
/* USER CODE BEGIN PFP */
static void CAN_Heartbeat(void);
static void CAN_Send_SensorData(void);
static void CAN_Send_SensorCheck(void);
static uint16_t cast_to_arbid(uint16_t id);
static void delay_us(uint16_t us);
static void ApplyGripperCommand(uint8_t motorByte, uint8_t servoByte);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI1_Init();
  MX_TIM3_Init();
  MX_ADC1_Init();
  MX_TIM2_Init();
  MX_TIM1_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);   /* PWM_N20  */
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);   /* PWM_SERVO */
  HAL_TIM_Encoder_Start(&htim2, TIM_CHANNEL_ALL);
  HAL_TIM_Base_Start(&htim1);                 /* free-running us tick for delay_us() */

  /* Boot-time CAN init, with a PC13 (onboard BlackPill LED) blink so a
   * failure is visible without a debugger attached - same intent as
   * stm_reference's boot-sequence blinks, trimmed to hardware this board
   * actually has. */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
  HAL_Delay(100);
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
  HAL_Delay(100);

  CAN_checker = CANSPI_Initialize();

  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
  HAL_Delay(100);
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
  HAL_Delay(100);

  lastSensorBroadcastTick = HAL_GetTick();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

    /* ---- CAN watchdog: silent bus/supervisor -> fail safe ----
     * Ported from stm_reference's CAN_failed_counter block. */
    if (CAN_failed_counter >= CAN_FAILED_THRESHOLD)
    {
      __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, 0);
      __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, 0);
      dcm1 = 0;
      start_node = false;
    }

    /* ---- start_node handshake ----
     * Ported from stm_reference's `if (!start_node) {...}` block: block
     * here (blinking PC13) until the supervisor sends start_node_msg, or
     * answer sensor_check_msg while waiting. */
    if (!start_node)
    {
      HAL_Delay(500);
      HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
      HAL_Delay(100);
      HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
      HAL_Delay(100);
      while (!CANSPI_Receive(&rx)) {}
      if (cast_to_arbid(rx.frame.id) == start_node_msg)
      {
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
        HAL_Delay(100);
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
        HAL_Delay(100);
        start_node = true;
        start_node_init = true;
        delay_us(50);
      }
      else if (cast_to_arbid(rx.frame.id) == sensor_check_msg)
      {
        CAN_Send_SensorCheck();
      }
      else if (start_node_init)
      {
        start_node = true;
      }
    }

    /* ---- periodic sensor telemetry (GripperEncoders source) ---- */
    if (start_node && (HAL_GetTick() - lastSensorBroadcastTick) >= SENSOR_BROADCAST_PERIOD_MS)
    {
      lastSensorBroadcastTick = HAL_GetTick();
      CAN_Send_SensorData();
    }

    /* ---- normal-operation CAN receive dispatch ---- */
    if (CANSPI_Receive(&rx))
    {
      CAN_failed_counter = 0;

      if (start_node && cast_to_arbid(rx.frame.id) == gripper_command_msg)
      {
        ApplyGripperCommand(rx.frame.data0, rx.frame.data1);
      }
      else if (cast_to_arbid(rx.frame.id) == heartbeat_msg)
      {
        /* Ported verbatim (semantics) from stm_reference: echo a
         * heartbeat derived from the supervisor's ping. */
        heartbeater = rx.frame.data0 + rx.frame.data1;
        beat_pls = true;
        CAN_Heartbeat();
      }
    }

    CAN_failed_counter++;
    delay_us(100);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 72;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV2;
  hadc1.Init.Resolution = ADC_RESOLUTION_12B;
  hadc1.Init.ScanConvMode = DISABLE;
  hadc1.Init.ContinuousConvMode = DISABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 1;
  hadc1.Init.DMAContinuousRequests = DISABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_2;
  sConfig.Rank = 1;
  sConfig.SamplingTime = ADC_SAMPLETIME_3CYCLES;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_MASTER;
  hspi1.Init.Direction = SPI_DIRECTION_2LINES;
  hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi1.Init.NSS = SPI_NSS_SOFT;
  hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_2;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief TIM1 Initialization Function - free-running microsecond tick used
  *        by delay_us(), ported from stm_reference's htim1 usage pattern.
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{
  /* USER CODE BEGIN TIM1_Init 0 */
  /*
   * TIM1 was not part of this project's original .ioc (same situation
   * USART1 was in before this rewrite - see the removed MX_USART1_UART_Init
   * comment history) so there is no HAL_TIM_Base_MspInit entry for it in
   * stm32f4xx_hal_msp.c yet. It needs no GPIO (internal clock source only,
   * no output channel used), so just enabling its clock here is sufficient;
   * add TIM1 in CubeMX and regenerate to move this into MSP properly.
   */
  __HAL_RCC_TIM1_CLK_ENABLE();
  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 71;      /* 72MHz APB2 timer clock / 72 = 1MHz -> 1 tick = 1us */
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 0xFFFF;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */
}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_Encoder_InitTypeDef sConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 0;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 4294967295;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  sConfig.EncoderMode = TIM_ENCODERMODE_TI1;
  sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC1Filter = 0;
  sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC2Filter = 0;
  if (HAL_TIM_Encoder_Init(&htim2, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM3_Init 1 */
  /*
   * Fixed vs. the original .ioc: was Prescaler=0/Period=65535 -> ~1.1kHz,
   * flagged in gripper_migration.md as "too fast for a hobby servo...
   * servo control will not behave correctly until this is addressed."
   * Now PSC=71/ARR=19999 -> 72MHz/72/20000 = 50Hz with 1us/tick
   * resolution, matching standard hobby-servo timing. N20 shares this
   * timer (PB4/PB5 are TIM3_CH1/CH2 only on this package) and now also
   * runs at 50Hz - re-verify it doesn't audibly whine at that rate.
   */
  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = 71;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = SERVO_PWM_PERIOD_TICKS - 1;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_PWM_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */
  HAL_TIM_MspPostInit(&htim3);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /* Onboard BlackPill LED, PC13, active-low - boot/heartbeat indicator. */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
  GPIO_InitStruct.Pin = GPIO_PIN_13;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/**
  * @brief  Applies an inbound gripper_command_msg to the N20/servo PWM
  *         outputs. motorByte/servoByte are raw 0-255 CAN payload bytes
  *         (gripperrr.py's dcm1/dcm2, unscaled).
  */
static void ApplyGripperCommand(uint8_t motorByte, uint8_t servoByte)
{
  dcm1 = motorByte;
  dcm2 = servoByte;

  uint32_t n20Compare = ((uint32_t)dcm1 * (SERVO_PWM_PERIOD_TICKS - 1)) / 255U;
  __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, n20Compare);

  uint32_t servoPulseUs = SERVO_PULSE_MIN_US +
      (((uint32_t)dcm2 * (SERVO_PULSE_MAX_US - SERVO_PULSE_MIN_US)) / 255U);
  __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, servoPulseUs);
}

/**
  * @brief  Broadcasts current encoder/current-sense readings as a
  *         sensor_data_msg CAN frame (GripperEncoders source).
  */
static void CAN_Send_SensorData(void)
{
  uint32_t quad1 = __HAL_TIM_GET_COUNTER(&htim2);

  HAL_ADC_Start(&hadc1);
  uint16_t acs1 = 0;
  if (HAL_ADC_PollForConversion(&hadc1, 5) == HAL_OK)
  {
    acs1 = (uint16_t)HAL_ADC_GetValue(&hadc1);
  }

  tx_sensor.frame.idType = dSTANDARD_CAN_MSG_ID_2_0B;
  tx_sensor.frame.id = sensor_data_msg;
  tx_sensor.frame.dlc = 5;
  tx_sensor.frame.data0 = (uint8_t)(quad1 & 0xFFU);
  tx_sensor.frame.data1 = 0;                 /* quad_2 - no 2nd encoder on this board */
  tx_sensor.frame.data2 = (uint8_t)(acs1 & 0xFFU);
  tx_sensor.frame.data3 = 0;                 /* acs_2 - no 2nd current sense on this board */
  tx_sensor.frame.data4 = 0;                 /* up_check - no status bits documented */
  CANSPI_Transmit(&tx_sensor);
}

/**
  * @brief  Replies to a sensor_check_msg received while still waiting on
  *         the start_node handshake, by reporting current sensor values -
  *         same intent as stm_reference's CAN_Send_SensorCheck() call site
  *         (body not shown there; this is the gripper-specific version).
  */
static void CAN_Send_SensorCheck(void)
{
  CAN_Send_SensorData();
}

/**
  * @brief  Sends the current heartbeat frame if one is pending.
  *         Copied from stm_reference verbatim (semantics unchanged).
  */
static void CAN_Heartbeat(void)
{
  if (beat_pls)
  {
    tx_heartbeat.frame.idType = dSTANDARD_CAN_MSG_ID_2_0B;
    tx_heartbeat.frame.id = heartbeat_msg;
    tx_heartbeat.frame.dlc = 1;
    tx_heartbeat.frame.data0 = heartbeater;
    beat_pls = false;
    CANSPI_Transmit(&tx_heartbeat);
  }
}

/**
  * @brief  Masks a composed id down to the 11-bit standard CAN ID range.
  *         Copied from stm_reference verbatim.
  */
static uint16_t cast_to_arbid(uint16_t id)
{
  return (id & 0x7FFU);
}

/**
  * @brief  Busy-wait microsecond delay using TIM1 as a free-running
  *         1us-tick counter. Copied from stm_reference verbatim.
  */
static void delay_us(uint16_t us)
{
  __HAL_TIM_SET_COUNTER(&htim1, 0);
  while (__HAL_TIM_GET_COUNTER(&htim1) < us) {}
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
