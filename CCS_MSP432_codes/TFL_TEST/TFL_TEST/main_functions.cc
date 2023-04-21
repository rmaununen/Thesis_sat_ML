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

#include <ti/drivers/UART.h>
#include "ti_drivers_config.h"

#include <TFL_TEST/constants.h>
#include <TFL_TEST/input_data.h>
#include <TFL_TEST/main_functions.h>
#include <TFL_TEST/output_handler.h>      // <-- REPLACED functions
//#include <TFL_TEST/therm_model_data.h>
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
int inference_count = 0;

constexpr int kTensorArenaSize = 2000;
uint8_t tensor_arena[kTensorArenaSize];

UART_Handle uart;

float circularBuffer[30];
bool firstval = true;

#define MODEL_DATA_SIZE 3952
// Define the C array that will hold the model data
//alignas(16) uint8_t therm_model_data[MODEL_DATA_SIZE] = { 0 };
// Define the model data array
uint8_t model_data[MODEL_DATA_SIZE] __attribute__((aligned(16)));
}

// Function to receive the model data over UART
#include <stdint.h>
/*#include <stdio.h>
// Function to receive the model data through UART
void receive_model_data(UART_Handle uart) {
  // Define a buffer to store the received data
  char buffer[256];
  int i = 0;

  // Receive data until we receive the entire model data
  while (i < MODEL_DATA_SIZE) {
    // Receive a line of data through UART
    UART_read(uart, &buffer[i], 1);

    // If we receive a newline character, move to the next line
    if (buffer[i] == 'x') {
      i++;
    }
  }

  // Parse the received data and store it in a C array
  char* ptr = strtok((char*)buffer, "\n");
  while (ptr != NULL) {
    model_data[i++] = strtoul(ptr, NULL, 16);
    ptr = strtok(NULL, "\n");
  }
}*/


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

  //GET MODEL DATA FROM UART
  /*bool model_received = false;
  unsigned char uart_model_data[3952];
  int k = 0;
  while (not model_received){
      char readBuf0[100]; // Buffer to read incoming data from UART
      int count = UART_read(uart, readBuf0, sizeof(readBuf0)); // Read data from UART
      if (count > 0) {
          if (*readBuf0 == '0'){ //if 0 is in string (checks whether model data is being received)
              unsigned char uc = reinterpret_cast<unsigned char&>(readBuf0);
              //char c = reinterpret_cast<char&>(uc);
              //UART_write(uart, *c, strlen(*c)); //TEST0
              uart_model_data[k] = uc;
              k++;
          }
          if (*readBuf0 == '-'){ //if - is in string (checks for data transfer end flag)
              model_received = true;
          }
      }
  }*/
  // Receive the model data through UART
  bool model_received = false;
  int k = 0;
  char readBuf0[100];
  while (!model_received) {
    int count = UART_read(uart, readBuf0, sizeof(readBuf0)); // Reads entire line (one value, like 0x00)
    if (count > 0) { // If a line is read
      char* ptr = strtok(readBuf0, "\n"); // Parse the read value
      //while (ptr != NULL) {
      model_data[k++] = strtoul(ptr, NULL, 16); // Add it to the model data array
      //ptr = strtok(NULL, "\n");
      //}
    }
    if (k == MODEL_DATA_SIZE) { // If we've received the entire model data
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
  static tflite::AllOpsResolver resolver;

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

  // Obtain pointers to the model's input and output tensors.
  input = interpreter->input(0);
  output = interpreter->output(0);

  // Keep track of how many inferences we have performed.
  inference_count = 0;

}

//Run forever
void loop() {
  // Set up the input tensor (read input float from UART)
  char readBuf[100]; // Buffer to read incoming data from UART
  int count = UART_read(uart, readBuf, sizeof(readBuf)); // Read data from UART
  if (count > 0) {
      // Convert the received string to a float and store it in the circular buffer
      //UART_write(uart, readBuf, strlen(readBuf));  //TEST1
      if (*readBuf == 'f'){
          firstval = true;
      }
      else{
          float newValue = string_to_float(readBuf);

          char float_str0[100];
          float_to_str(float_str0, sizeof(float_str0), 8, newValue);
          UART_write(uart, "Last input: ", 12);
          UART_write(uart, float_str0, strlen(float_str0)); //TEST2
          UART_write(uart, "\n", 1);

          if (firstval == true) {
              // If this is the first value received, set all elements of the buffer to this value
              for (int i = 0; i < 30; i++) {
                  circularBuffer[i] = newValue;
              }
              firstval = false;
              //UART_write(uart, "firstval", 8); //TEST
          } else {
              // Shift the elements of the circular buffer by one position and add the new value
              for (int i = 0; i < 29; i++) {
                  circularBuffer[i] = circularBuffer[i + 1];
              }
              circularBuffer[29] = newValue;
              //UART_write(uart, "second", 6); //TEST
          }
          /*
          // Print the received float values for debugging purposes
          for (int i = 0; i < 30; i++) {
              UART_write(uart, "Array value: ", 13);
              char float_str[100];
              float_to_str(float_str, sizeof(float_str), 8, circularBuffer[i]);
              UART_write(uart, float_str, strlen(float_str));
              UART_write(uart, "\n", 1); // start the next write on a new line
          }
          */
      }

  }

  // Quantize input <-- Integrate into tensor reading
  int8_t quantized_input_data[30];
  for (int i = 0; i < 30; i++) {
    quantized_input_data[i] = static_cast<int8_t>(circularBuffer[i] / input->params.scale + input->params.zero_point);
  }
  memcpy(input->data.int8, quantized_input_data, 30 * sizeof(int8_t));

  // Run inference, and report any error
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    UART_write(uart, "E: Invoke failed", 16);
    return;
  }

  // Get from the output tensor
  int8_t y_quantized = output->data.int8[0];
  // Dequantize output and send over UART
  float y = (y_quantized - output->params.zero_point) * output->params.scale;

  char yString[32];
  float_to_str(yString, 32, 8, y);

  UART_write(uart, "Output: ", 8);
  UART_write(uart, yString, strlen(yString));
  UART_write(uart, "\n", 1); // start the next write on a new line

  // Increment the inference_counter, and reset it if we have reached
  // the total number per cycle
  if (inference_count >= kInferencesPerCycle) inference_count = 0;
}
