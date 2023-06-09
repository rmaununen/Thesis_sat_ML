import tensorflow as tf
import numpy as np
import random

def predict_tflite(tflite_model, x_test, inp_size):
  # Prepare the test data
  x_test_ = x_test.copy()
  x_test_ = x_test_.reshape((len(x_test), inp_size))
  x_test_ = x_test_.astype(np.float32)

  # Initialize the TFLite interpreter
  interpreter = tf.lite.Interpreter(model_content=tflite_model,
                                    experimental_op_resolver_type=tf.lite.experimental.OpResolverType.BUILTIN_REF)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()[0]
  output_details = interpreter.get_output_details()[0]

  # If required, quantize the input layer (from float to integer)
  input_scale, input_zero_point = input_details["quantization"]
  if (input_scale, input_zero_point) != (0.0, 0):
    x_test_ = x_test_ / input_scale + input_zero_point
    x_test_ = x_test_.astype(input_details["dtype"])

  # Invoke the interpreter
  y_pred = np.empty(len(x_test_), dtype=output_details["dtype"])
  for i in range(len(x_test_)):
    interpreter.set_tensor(input_details["index"], [x_test_[i]])
    interpreter.invoke()
    y_pred[i] = interpreter.get_tensor(output_details["index"])[0]

  # If required, dequantized the output layer (from integer to float)
  output_scale, output_zero_point = output_details["quantization"]
  if (output_scale, output_zero_point) != (0.0, 0):
    y_pred = y_pred.astype(np.float32)
    y_pred = (y_pred - output_zero_point) * output_scale

  return y_pred


# Function: Convert some hex value into an array for C programming
def hex_to_c_array(hex_data, var_name):

  c_str = ''

  # Create header guard
  c_str += '#ifndef ' + var_name.upper() + '_H\n'
  c_str += '#define ' + var_name.upper() + '_H\n\n'

  # Add array length at top of file
  c_str += '\nunsigned int ' + var_name + '_len = ' + str(len(hex_data)) + ';\n'

  # Declare C variable
  c_str += 'unsigned char ' + var_name + '[] = {'
  hex_array = []
  for i, val in enumerate(hex_data) :

    # Construct string from hex
    hex_str = format(val, '#04x')

    # Add formatting so each line stays within 80 characters
    if (i + 1) < len(hex_data):
      hex_str += ','
    if (i + 1) % 12 == 0:
      hex_str += '\n '
    hex_array.append(hex_str)

  # Add closing brace
  c_str += '\n ' + format(' '.join(hex_array)) + '\n};\n\n'

  # Close out header guard
  c_str += '#endif //' + var_name.upper() + '_H'

  return c_str

def read_lists_from_txt(filename):
  list1 = []
  list2 = []
  with open(filename, 'r') as f:
    for line in f:
      item1, item2 = line.strip().split('\t')
      list1.append(float(item1))
      list2.append(float(item2))
  return list1, list2

def read_ptm_dataset(N, N_o, filename):
  x_rows = []
  y_rows = []
  with open(filename, "r") as f:
    for line in f:
      # Split the line into values
      values = line.strip().split()
      if len(values) == N + N_o:
        # Extract the input and output values
        x = [float(v) for v in values[N_o:]] #values[:-1]]
        y = [float(v) for v in values[0:N_o]]
        x_rows.append(x)
        y_rows.append(y)
      else:
        print('Warning: length of a row is not', N + N_o, '. Counted is', len(values))
    # Shuffle
    # Combine x and y into a list of tuples
    xy_pairs = list(zip(x_rows, y_rows))
    # Shuffle the list of tuples
    random.shuffle(xy_pairs)
    # Separate the tuples back into two lists
    x_rows, y_rows = zip(*xy_pairs)
  return np.array(x_rows), np.array(y_rows)

import numpy as np

def numpy_to_cpp_array(arr, filename):
    """
    Converts a NumPy array into a C++ array and writes it to a text file.

    Parameters:
    arr (numpy.ndarray): The NumPy array to be converted.
    filename (str): The name of the file to which the C++ array will be written.

    Returns:
    None
    """
    # Open the file in write mode
    with open(filename, 'w') as f:

        # Write the C++ array declaration
        f.write(f"int arr{arr.shape} = {{\n")

        # Write the elements of the array
        for i in range(arr.shape[0]):
            f.write("  {")
            for j in range(arr.shape[1]):
                f.write(str(arr[i][j]))
                if j != arr.shape[1] - 1:
                    f.write(", ")
            f.write("}")
            if i != arr.shape[0] - 1:
                f.write(",\n")

        # Write the closing curly brace and semicolon
        f.write("\n};\n")

    print(f"The C++ array has been written to {filename}")
