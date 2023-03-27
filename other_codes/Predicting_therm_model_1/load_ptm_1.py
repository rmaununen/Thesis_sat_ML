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


N_i = 30
x_test_rows = []
y_test_rows = []
with open("2test_a2.txt", "r") as f:
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