import sys
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
import tensorflow as tf
import numpy as np
import math
import matplotlib.pyplot as plt
from other_codes.tfl_converter_tools import *
import os
Working_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1'
Telemetry_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/Telemetry'
Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/Dataset'

print(os.getcwd())

convert = False
N_i = 60

tf_model_name = 'adm_11'  #The existing model
tflite_model_name = 'adm_1'  # Will be given .tflite suffix
c_model_name = 'adm_1'       # Will be given .h suffix

os.chdir(Working_dir)
model = tf.keras.models.load_model(tf_model_name+'.h5')

#TEST PERFORMANCE
for test_file in os.listdir(Dataset_dir):
    os.chdir(Dataset_dir)
    x_test_rows = []
    y_test_rows = []
    with open(test_file, "r") as f:
        for line in f:
            # Split the line into values
            values = line.strip().split()
            if len(values) == N_i + 1:
                # Extract the input and output values
                x = [float(v) for v in values[1:]]
                x_test_rows.append(x)
                y = float(values[0])
                y_test_rows.append(y)

    predictions = model.predict(np.array(x_test_rows))
    x_time = []
    t = 0
    for i in range(len(y_test_rows)):
        x_time.append(t)
        t+=1

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.clf()
    plt.title(f'Actual vs model {tf_model_name}, {test_file}')
    plt.plot(x_time, y_test_rows, 'b', linewidth=3, label='Actual values')
    plt.plot(x_time, predictions, 'r', label='Model predictions')
    plt.legend()
    plt.show()
    x_values = np.array(x_test_rows)
    y_values = np.array(y_test_rows)

if convert:
    # Convert Keras model to a tflite model
    nsamples = 115     # Number of samples to use as a representative dataset
    # Get representative dataset from one of the test orbits
    os.chdir('/other_codes/2_Predicting_therm_model_1')
    x_rep, y_rep = read_ptm_dataset(N_i, 'Testing_with_30_point_arrays/2test_0.txt')
    x_rep = 1.6*x_rep
    x_rep = np.round(x_rep, decimals=2)
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