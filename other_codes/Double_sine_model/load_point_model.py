import sys
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
import tensorflow as tf
import numpy as np
import math
import matplotlib.pyplot as plt
from other_codes.tfl_converter_tools import *
import os
os.chdir('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Double_sine_model')
print(os.getcwd())
nsamples = 200     # Number of samples to use as a dataset
np.random.seed(1234)
x_values = np.random.uniform(low=0, high=(2 * math.pi), size=nsamples).astype(np.float32)
y_values = np.sin(x_values*2)# + (0.1 * np.random.randn(x_values.shape[0]))

tflite_model_name = 'point_model'  # Will be given .tflite suffix
c_model_name = 'point_model'       # Will be given .h suffix

model = tf.keras.models.load_model(tflite_model_name+'.h5')

predictions = model.predict(x_values)

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

# Write TFLite model to a C source (or header) file
with open(c_model_name + '.h', 'w') as file:
  file.write(hex_to_c_array(tflite_model, c_model_name))