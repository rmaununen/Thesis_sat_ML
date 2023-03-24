import sys
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
import tensorflow as tf
import numpy as np
import math
import matplotlib.pyplot as plt
from other_codes.tfl_converter_tools import *
import os
os.chdir('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Simple_therm_model_1')
print(os.getcwd())

x_values, y_values = read_lists_from_txt('mod1_actual.txt')
x_values = np.array(x_values)
y_values = np.array(y_values)

tflite_model_name = 'therm_model_1'  # Will be given .tflite suffix
c_model_name = 'therm_model_1'       # Will be given .h suffix

model = tf.keras.models.load_model(tflite_model_name+'.h5')

predictions = model.predict(x_values)

# Convert Keras model to a tflite model
nsamples = 200     # Number of samples to use as a representative dataset
np.random.seed(1234)
x_val = np.random.uniform(low=0, high=(2 * math.pi), size=nsamples).astype(np.float32)
def representative_dataset():
  for i in range(200):
    yield([x_val[i].reshape(1, 1)])

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

# Write TFLite model to a C source (or header) file
with open(c_model_name + '.h', 'w') as file:
  file.write(hex_to_c_array(tflite_model, c_model_name))