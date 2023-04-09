/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

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


#include <TFL_TEST/output_handler.h>

/*
void HandleOutput(tflite::ErrorReporter* error_reporter, float x_value,
                  float y_value) {
  // Log the current X and Y values
  TF_LITE_REPORT_ERROR(error_reporter, "x_value: %f, y_value: %f\n",
                       static_cast<double>(x_value),
                       static_cast<double>(y_value));
}
*/


void float_to_strGPT(char* buf, uint32_t bufsize, uint32_t num_decimal_places, float f) {
  if (bufsize < MAX_FLOAT_STR_LEN) {
    return;
  }

  // handle negative numbers
  int is_negative = 0;
  if (f < 0) {
    is_negative = 1;
    f = -f;
  }

  uint32_t integer_part = (uint32_t) f;
  float fractional_part = f - integer_part;

  uint32_t index = 0;

  if (is_negative) {
      buf[index++] = '-';
  }

  do {
    buf[index++] = '0' + integer_part % 10;
    integer_part /= 10;
  } while (integer_part > 0);
  buf[index] = '\0';

  uint32_t i = 0;
  uint32_t j = index - 1;

  if (is_negative) {
      ++i;
  }

  while (i < j) {
    char temp = buf[i];
    buf[i++] = buf[j];
    buf[j--] = temp;
  }

  buf[index++] = '.';
  while (num_decimal_places-- > 0) {
    fractional_part *= 10;
    uint32_t digit = (uint32_t) fractional_part;
    buf[index++] = '0' + digit;
    fractional_part -= digit;
  }

  buf[index] = '\0';
}


float string_to_float(const char* str) {
    float result = 0.0f;
    int32_t wholePart = 0;
    float fracPart = 0.0f;
    int32_t sign = 1;
    //bool hasDecimal = false;
    //bool hasSign = false;

    // skip leading whitespace
    while (*str == ' ') {
        ++str;
    }

    // check for sign
    if (*str == '-') {
        sign = -1;
        //hasSign = true;
        ++str;
    } else if (*str == '+') {
        //hasSign = true;
        ++str;
    }

    // read whole part
    while (*str >= '0' && *str <= '9') {
        wholePart = wholePart * 10 + (*str - '0');
        ++str;
    }

    // read fractional part
    if (*str == '.') {
        //hasDecimal = true;
        ++str;
        float fracMultiplier = 0.1f;
        while (*str >= '0' && *str <= '9') {
            fracPart += (*str - '0') * fracMultiplier;
            fracMultiplier *= 0.1f;
            ++str;
        }
    }

    // combine whole and fractional parts
    result = static_cast<float>(wholePart) + fracPart;

    // apply sign
    result *= sign;

    return result;
}
