import os
import sys
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
from other_codes.tfl_converter_tools import *
os.chdir('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Predicting_therm_model_1')

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
x_values = np.array(x_test_rows)
y_values = np.array([y_test_rows])
numpy_to_cpp_array(x_values, 'test_array.h')
numpy_to_cpp_array(y_values, 'test_array_out.h')
for i in y_test_rows:
    print(i)