/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/
//#include <ti/devices/MSP432p4xx/inc/msp432p401r.h>
//#include <ti/devices/DeviceFamily.h>
//#define DeviceFamily_ID             DeviceFamily_ID_MSP432P401x
//#define DeviceFamily_DIRECTORY      msp432p4xx
//#define DeviceFamily_PARENT         DeviceFamily_PARENT_MSP432P401R
#include <ti/drivers/UART.h>
#include "ti_drivers_config.h"
//#include <ti/drivers/uart/UARTMSP432.h>
//#include "ti_drivers_config.h"
//#include <msp.h>
//#include <ti/devices/msp432p4xx/driverlib/driverlib.h>

#include <TFL_TEST/constants.h>
#include <TFL_TEST/input_data.h>
#include <TFL_TEST/main_functions.h>
#include <TFL_TEST/output_handler.h>
#include <TFL_TEST/therm_model_data.h>
#include "tensorflow/lite/micro/all_ops_resolver.h"
//#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/micro/micro_allocator.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace {
//tflite::ErrorReporter* error_reporter = nullptr;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
int inference_count = 0;

constexpr int kTensorArenaSize = 2000;
uint8_t tensor_arena[kTensorArenaSize];

tflite::MicroAllocator* ma = nullptr; // <-- ADDED during thesis meeting 17.02.2023

UART_Handle uart;

}  // namespace

//tflite::MicroAllocator  ma(tensor_arena, kTensorArenaSize);

// The name of this function is important for Arduino compatibility.
void setup() {
  tflite::InitializeTarget();

  // Set up logging. Google style is to avoid globals or statics because of
  // lifetime uncertainty, but since this has a trivial destructor it's okay.
  // NOLINTNEXTLINE(runtime-global-variables)
  //static tflite::MicroErrorReporter micro_error_reporter;
  //error_reporter = &micro_error_reporter;

  // Map the model into a usable data structure. This doesn't involve any
  // copying or parsing, it's a very lightweight operation.
  model = tflite::GetModel(g_therm_model_data);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    //TF_LITE_REPORT_ERROR(error_reporter,
    //                     "Model provided is schema version %d not equal "
    //                     "to supported version %d.",
    //                     model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // This pulls in all the operation implementations we need.
  // NOLINTNEXTLINE(runtime-global-variables)
  static tflite::AllOpsResolver resolver;

  ma = tflite::MicroAllocator::Create(tensor_arena, kTensorArenaSize); // <-- ADDED during thesis meeting 17.02.2023

  // Build an interpreter to run the model with.
  static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize); //20.02.23 removed "(... ,error_reporter)"
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors.
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    //TF_LITE_REPORT_ERROR(error_reporter, "AllocateTensors() failed");
    return;
  }

  // Obtain pointers to the model's input and output tensors.
  input = interpreter->input(0);
  output = interpreter->output(0);

  // Keep track of how many inferences we have performed.
  inference_count = 0;

  //UART

  // One-time initialization of UART driver
  UART_init();
  // Initialize UART parameters
  UART_Params params;
  UART_Params_init(&params);
  params.baudRate = 115200;
  params.readMode = UART_MODE_BLOCKING;
  params.writeMode = UART_MODE_BLOCKING;
  params.readTimeout = UART_WAIT_FOREVER;
  params.writeTimeout = UART_WAIT_FOREVER;
  params.dataLength = UART_LEN_8;
  params.parityType = UART_PAR_NONE;
  params.stopBits = UART_STOP_ONE;
  // Open the UART
  uart = UART_open(CONFIG_UART_0, &params);
}

// The name of this function is important for Arduino compatibility.
void loop() {
  // Calculate an x value to feed into the model. We compare the current
  // inference_count to the number of inferences per cycle to determine
  // our position within the range of possible x values the model was
  // trained on, and use this to calculate a value.
  //float position = static_cast<float>(inference_count) /
  //                 static_cast<float>(kInferencesPerCycle); //Changed kInferencesPerCycle from 20 to 50 24.03.23
  //float x = position * kXrange;

  // Quantize the input from floating-point to integer
  //int8_t x_quantized = x / input->params.scale + input->params.zero_point;
  // Place the quantized input in the model's input tensor
  //input->data.int8[0] = x_quantized;


  // Set up the input tensor with the input data
  //float input_data[30] = {20.14, 22.8, 20.14, 18.44, 21.63, 19.78, 17.52, 19.95, 19.25, 17.38, 17.67, 18.53, 17.14, 15.6, 13.97, 12.75, 11.04, 8.98, 7.88, 6.75, 4.9, 3.84, 3.34, 1.68, 0.6, 0.22, -1.17, -2.18, -2.61, -3.36}; // <-- TEST MLP
  float input_row[30];
  for (int j = 0; j < 30; j++) {
    input_row[j] = input_data_MLP_2a2[inference_count][j];  // copy the jth element of row i from input_data to input_row
  }
  // Quantize
  int8_t quantized_input_data[30];
  for (int i = 0; i < 30; i++) {
    quantized_input_data[i] = static_cast<int8_t>(input_row[i] / input->params.scale + input->params.zero_point);
  }
  memcpy(input->data.int8, quantized_input_data, 30 * sizeof(int8_t));

  // Run inference, and report any error
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    //TF_LITE_REPORT_ERROR(error_reporter, "Invoke failed on x: %f\n",
    //                     static_cast<double>(inference_count));
    return;
  }

  // Obtain the quantized output from model's output tensor
  int8_t y_quantized = output->data.int8[0];
  // Dequantize the output from integer to floating-point
  float y = (y_quantized - output->params.zero_point) * output->params.scale;

  // Output the results. A custom HandleOutput function can be implemented
  // for each supported hardware target.
  //HandleOutput(error_reporter, inference_count, y);

  //UART
  //UART_write(uart, "Hello, world!\r\n", 15);
  char readBuf[100]; // Buffer to read incoming data from UART
  int i;
  int j;

  // Read string from UART if available
  int count = UART_read(uart, readBuf, sizeof(readBuf));
  if (count > 0) {
      // Write "string read from UART: " followed by the string read from UART. Repeat 20 times.
      for (j = 0; j < 30000000; j++) {

      }
      for (i = 0; i < 20; i++) {
          UART_write(uart, "string read from UART: ", 22);
          UART_write(uart, readBuf, count);
          UART_write(uart, "\n", 1); // start the next write on a new line
          for (j = 0; j < 10000000; j++) {

          }
      }
  }

  // Increment the inference_counter, and reset it if we have reached
  // the total number per cycle
  inference_count += 1;
  if (inference_count >= kInferencesPerCycle) inference_count = 0;
  //__delay_cycles(100000); //1 s delay introduced 24.03.23
}
