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

#include <stdint.h>
#include <ti/drivers/UART.h>
#include "ti_drivers_config.h"
#include <TFLM/constants.h>
//#include <TFLM/therm_model_data.h>
#include <ti/devices/msp432p4xx/inc/msp432p401r.h>
#include <TFLM/main_functions.h>
#include <TFLM/conversion_functions.h>
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

// Globals
namespace {
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;

constexpr int kTensorArenaSize = 4000;
uint8_t tensor_arena[kTensorArenaSize];

UART_Handle uart;

bool firstval = true;
bool inference = false;

int input_size = 0;
int output_size = 0;
}


//Run once
void setup() {

  // One-time initialization of UART driver
  UART_init();
  UART_Params UARTparams;
  UART_Params_init(&UARTparams);
  UARTparams.baudRate = 115200;
  UARTparams.readMode = UART_MODE_BLOCKING;
  UARTparams.writeMode = UART_MODE_BLOCKING;
  UARTparams.readTimeout = UART_WAIT_FOREVER;
  UARTparams.writeTimeout = UART_WAIT_FOREVER;
  UARTparams.dataLength = UART_LEN_8;
  UARTparams.parityType = UART_PAR_NONE;
  UARTparams.stopBits = UART_STOP_ONE;
  uart = UART_open(CONFIG_UART_0, &UARTparams);

  // Receive the model data size through UART
  int model_data_size = 0;
  bool model_size_received = false;
  char readSize[32];
  while (!model_size_received) {
    int count = UART_read(uart, readSize, sizeof(readSize)); // Reads entire line
    if (count > 0) { // If a line is read
        model_data_size = strtoul(readSize, NULL, 10); // Parse the read value
        model_size_received = true;
    }
  }
  UART_write(uart, "Model data size has been received on MSP\n", 41);

  // Receive the model input size through UART
  bool inp_size_received = false;
  //char readSize[32];
  while (!inp_size_received) {
    int count = UART_read(uart, readSize, sizeof(readSize)); // Reads entire line
    if (count > 0) { // If a line is read
        input_size = strtoul(readSize, NULL, 10); // Parse the read value
        inp_size_received = true;
    }
  }
  UART_write(uart, "Model input size has been received on MSP\n", 42);


  // Receive the model output size through UART
  bool out_size_received = false;
  //char readSize[32];
  while (!out_size_received) {
    int count = UART_read(uart, readSize, sizeof(readSize)); // Reads entire line
    if (count > 0) { // If a line is read
        output_size = strtoul(readSize, NULL, 10); // Parse the read value
        out_size_received = true;
    }
  }
  UART_write(uart, "Model output size has been received on MSP\n", 43);

  // Receive the model data through UART
  uint8_t model_data[model_data_size] __attribute__((aligned(16))); // Model data array to be filled
  bool model_received = false;
  int k = 0;
  char readBuf0[100];
  while (!model_received) {
    int count = UART_read(uart, readBuf0, sizeof(readBuf0)); // Reads entire line (one value, like 0x00)
    if (count > 0) { // If a line is read
      char* ptr = strtok(readBuf0, "\n"); // Parse the read value
      model_data[k++] = strtoul(ptr, NULL, 16); // Add it to the model data array
    }
    if (k == model_data_size) { // If we've received the entire model data
      model_received = true;
    }
  }
  UART_write(uart, "Model data has been received on MSP\n", 36);

  tflite::InitializeTarget();

  // Map the model into a usable data structure (no copying or parsing, lightweight).
  model = tflite::GetModel(model_data); //g_therm_model_data    uart_model_data
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    UART_write(uart, "E: Model version is not compatible\n", 35);
    return;
  }

  // Get operation implementations.
  static tflite::MicroMutableOpResolver<1> resolver; //MicroMutableOpResolver or   static tflite::AllOpsResolver resolver;
  if (resolver.AddFullyConnected() != kTfLiteOk) {
    return;
  }

  // Build an interpreter to run the model with.
  static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize); //20.02.23 removed "(... ,error_reporter)"
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors.
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    //TF_LITE_REPORT_ERROR(error_reporter, "AllocateTensors() failed");      // <-- REPLACED BY UART DRIVER
      UART_write(uart, "E: AllocateTensors() failed\n", 28);
    return;
  }
  else{
      UART_write(uart, "TFLM model initialized successfully\n", 36);
  }

  // Obtain pointers to the model's input and output tensors.
  input = interpreter->input(0);
  output = interpreter->output(0);

}

//Run forever
void loop() {
  // Set up the input tensor (read input float from UART)
  float circularBuffer[input_size];
  char readBuf[100]; // Buffer to read incoming data from UART
  int count = UART_read(uart, readBuf, sizeof(readBuf)); // Read data from UART
  if (count > 0) {
      // Convert the received string to a float and store it in the circular buffer
      if (*readBuf == 'f'){  //"Data set file end" tag to clear circular buffer
          firstval = true;
      }
      else if (*readBuf == 'i'){  //"Go for inference" tag to perform inferences only when needed
          inference = true;
      }
      else{
          float newValue = string_to_float(readBuf);

          //char float_str0[100];
          //float_to_str(float_str0, sizeof(float_str0), 8, newValue);
          //UART_write(uart, "Last input: ", 12);
          //UART_write(uart, float_str0, strlen(float_str0)); //TEST2
          //UART_write(uart, "\n", 1);

          if (firstval == true) {
              // If this is the first value received, set all elements of the buffer to this value
              for (int i = 0; i < input_size; i++) {
                  circularBuffer[i] = newValue;
              }
              firstval = false;
          } else {
              // Shift the elements of the circular buffer by one position and add the new value
              for (int i = 0; i < (input_size-1); i++) {
                  circularBuffer[i] = circularBuffer[i + 1];
              }
              circularBuffer[(input_size-1)] = newValue;
          }
      }

  }

  if (inference == true) {
      // Quantize input <-- Integrate into tensor reading
      int8_t quantized_input_data[input_size];
      for (int i = 0; i < input_size; i++) {
        quantized_input_data[i] = static_cast<int8_t>(circularBuffer[i] / input->params.scale + input->params.zero_point);
      }
      memcpy(input->data.int8, quantized_input_data, input_size * sizeof(int8_t));

      // Run inference, and report any error
      TfLiteStatus invoke_status = interpreter->Invoke();
      if (invoke_status != kTfLiteOk) {
        UART_write(uart, "E: Invoke failed", 16);
        return;
      }

      // Get from the output tensor
      for (int i = 0; i < output_size; ++i) {
        int8_t y_quantized = output->data.int8[i];
        // Dequantize output and send over UART
        float y = (y_quantized - output->params.zero_point) * output->params.scale;
        char yString[32];
        float_to_str(yString, 32, 8, y);
        UART_write(uart, "Output: ", 8);
        UART_write(uart, yString, strlen(yString));
        UART_write(uart, "\n", 1); // start the next write on a new line
      }
      inference = false; //Inference complete, set it back to false
  }

}
