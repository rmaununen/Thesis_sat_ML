import tensorflow as tf
import math
import numpy as np
import matplotlib.pyplot as plt

nsamples = 200     # Number of samples to use as a dataset
np.random.seed(1234)
x_values = np.random.uniform(low=0, high=(2 * math.pi), size=nsamples).astype(np.float32)
y_values = np.sin(x_values*2)# + (0.1 * np.random.randn(x_values.shape[0]))

tflite_model_name = 'point_model'  # Will be given .tflite suffix
c_model_name = 'point_model'       # Will be given .h suffix

model = tf.keras.models.load_model(tflite_model_name+'.h5')

predictions = model.predict(x_values)

def predict_tflite(tflite_model, x_test):
  # Prepare the test data
  x_test_ = x_test.copy()
  x_test_ = x_test_.reshape((x_test.size, 1))
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
  y_pred = np.empty(x_test_.size, dtype=output_details["dtype"])
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

# Convert Keras model to a tflite model
def representative_dataset():
  for i in range(200):
    yield([x_values[i].reshape(1, 1)])

converter = tf.lite.TFLiteConverter.from_keras_model(model)
print('converter object was created')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
print('converter optimizations were specified')
converter.representative_dataset = representative_dataset
print('representative dataset has been loaded')
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
print('quantization scheme was specified')
converter.inference_input_type = tf.int8  # or tf.uint8
print('input quantization was specified')
converter.inference_output_type = tf.int8  # or tf.uint8
print('output quantization was specified')
tflite_model = converter.convert()
print('conversion completed')

open(tflite_model_name + '.tflite', 'wb').write(tflite_model)
print('tflite model was saved')

y_test_pred_tflite = predict_tflite(tflite_model, x_values)
print('test inference of tflite model was performed')

# Compare predictions
plt.clf()
plt.title('Comparison of models against actual values')
plt.plot(x_values, y_values, 'bo', label='Actual values')
plt.plot(x_values, predictions, 'ro', label='TF predictions')
plt.plot(x_values, y_test_pred_tflite, 'gx', label='TFLite quantized predictions')
plt.legend()
plt.show()

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

# Write TFLite model to a C source (or header) file
with open(c_model_name + '.h', 'w') as file:
  file.write(hex_to_c_array(tflite_model, c_model_name))