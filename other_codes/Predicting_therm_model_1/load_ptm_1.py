import sys
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
import tensorflow as tf
import numpy as np
import math
import matplotlib.pyplot as plt
from other_codes.tfl_converter_tools import *
import os
os.chdir('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Predicting_therm_model_1')
print(os.getcwd())

convert = True
N_i = 30
x_test_rows = []
y_test_rows = []
with open("1test_a1.txt", "r") as f:
    for line in f:
        # Split the line into values
        values = line.strip().split()
        if len(values) == N_i + 1:
            # Extract the input and output values
            x = [float(v) for v in values[:-1]]
            x_test_rows.append(x)
            y = float(values[-1])
            y_test_rows.append(y)

tflite_model_name = 'ptm_1'  # Will be given .tflite suffix
c_model_name = 'ptm_1'       # Will be given .h suffix

model = tf.keras.models.load_model(tflite_model_name+'.h5')

predictions = model.predict(np.array(x_test_rows))
x_time = []
t = 0
for i in range(len(y_test_rows)):
    x_time.append(t)
    t+=1

fig = plt.figure()
ax = fig.add_subplot(111)
plt.clf()
plt.title("Comparison of predictions to actual values (every 2nd inference)")
plt.plot(x_time, y_test_rows, 'b', label='Actual values')
plt.plot(x_time, predictions, 'r', label='Model predictions')
plt.legend()
plt.show()
x_values = np.array(x_test_rows)
y_values = np.array(y_test_rows)

if convert:
    # Convert Keras model to a tflite model
    nsamples = 115     # Number of samples to use as a representative dataset
    # Get representative dataset from one of the test orbits
    os.chdir('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Predicting_therm_model_1')
    x_rep, y_rep = read_ptm_dataset(N_i, '2test_0.txt')
    print('x_rep', np.shape(x_rep), 'y_rep:', np.shape(y_rep))

    def representative_dataset():
      for i in range(nsamples):
        yield([x_rep[i].reshape(1, N_i).astype(np.float32)])

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

    y_test_pred_tflite = predict_tflite(tflite_model, x_values, N_i)
    print('test inference of tflite model was performed')

    # Compare predictions
    plt.clf()
    plt.title('Comparison of models against actual values')
    plt.plot(x_time, y_test_rows, 'bo', label='Actual values')
    plt.plot(x_time, predictions, 'ro', label='TF predictions')
    plt.plot(x_time, y_test_pred_tflite, 'g', label='TFLite quantized predictions')
    plt.legend()
    plt.show()

    # Write TFLite model to a C source (or header) file
    with open(c_model_name + '.h', 'w') as file:
      file.write(hex_to_c_array(tflite_model, c_model_name))