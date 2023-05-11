import sys
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
import tensorflow as tf
import numpy as np
import math
import matplotlib.pyplot as plt
from other_codes.tfl_converter_tools import *
from test_adm_input import *
import os
import re
Working_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1'
Telemetry_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/Telemetry'
Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/Dataset_2'
report_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/TF_test_report'
print(os.getcwd())

convert = False
gradcam = False
plot_tests = True
make_report = True
N_i = 60
N_o = 2

tflite_model_name = 'adm_1'  # Will be given .tflite suffix
c_model_name = 'adm_1'       # Will be given .h suffix

os.chdir(Working_dir)
model = tf.keras.models.load_model(tf_model_name+'.h5')
Weights0 = model.layers[0].get_weights()[0]
print('Sum of absolute values of input layer weights per input layer neuron.')
weights_abs_sum = []
for i in range(len(Weights0)):
    weights_abs_sum.append(np.sum(np.abs(Weights0[i])))
weight_arr = np.array(weights_abs_sum)
print(weight_arr)
print('------------------------------')
# Visualize the importance scores using a heatmap
fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(weight_arr.reshape(3, 20), cmap='hot')
plt.title(f'Sum of abs. weights per input layer neuron. {tf_model_name}')
plt.colorbar()
plt.show()
plot_name = f'{report_dir}/input_weights.png'
fig.savefig(plot_name)
# Define a function to calculate the gradient of the output with respect to each input
def get_gradients(model, inputs):
    with tf.GradientTape() as tape:
        tape.watch(inputs)
        outputs = model(inputs)
    grads = tape.gradient(outputs, inputs)
    return grads

#List to estimate accuracy
all_act = []
all_mod = []

#TEST PERFORMANCE
for test_file in os.listdir(Dataset_dir):
    os.chdir(Dataset_dir)
    x_test_rows = []
    x_test_dat_1 = []
    x_test_dat_2 = []
    x_test_dat_3 = []
    y_test_rows = []
    y_test_rows0 = []
    with open(test_file, "r") as f:
        for line in f:
            # Split the line into values
            values = line.strip().split()
            if len(values) == N_i + 2:
                # Extract the input and output values
                x = [float(v) for v in values[N_o:]]
                x_test_rows.append(x)
                x_test_dat_1.append(x[19])
                x_test_dat_2.append(x[39])
                x_test_dat_3.append(x[59])
                y = float(values[1])
                y_test_rows.append(y)
                y0 = float(values[0])
                y_test_rows0.append(y0)

    predictions = model.predict(np.array(x_test_rows))
    predictions0 = predictions[:, 0]
    predictions1 = predictions[:, 1]
    pred1_lst0 = predictions1.flatten().tolist()
    pred1_lst = []
    for p in pred1_lst0:
        if p< threshold_out:
            pred1_lst.append(0)
        else:
            pred1_lst.append(1)
    x_time = []
    t = 0
    for i in range(len(y_test_rows)):
        x_time.append(t)
        t+=1
    if ('1187' in test_file):
        #add up all model inference results for later acuracy analysis
        all_act += y_test_rows
        all_mod += pred1_lst#predictions1.flatten().tolist()
        #print current test file name
        print(test_file)

    if plot_tests and ('1187' in test_file):
        #Model classification output vs actual label
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Actual vs model {tf_model_name}, {test_file}')
        plt.plot(x_time, y_test_rows, 'b', linewidth=3, label='Actual anomaly label')
        plt.plot(x_time, pred1_lst, 'r', label='Model output')
        plt.legend()
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        #plt.show()
        x_values = np.array(x_test_rows)
        y_values = np.array(y_test_rows)
        plot_name = f'{report_dir}/{test_file}_mod.png'
        fig.savefig(plot_name)
        plt.clf()

        # Telemetry from the three panel sensors
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Temperature sensors, {test_file}')
        plt.plot(x_time, x_test_dat_1, 'b', label='Panel 1 (+X)')
        plt.plot(x_time, x_test_dat_2, 'r', label='Panel 2 (-X)')
        plt.plot(x_time, x_test_dat_3, 'g', label='Panel 3 (+Y)')
        plt.legend()
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        # plt.show()
        plot_name = f'{report_dir}/{test_file}_sens.png'
        fig.savefig(plot_name)
        plt.clf()

        # Model prediction vs actual sensor
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Actual vs model prediction {tf_model_name}, {test_file}')
        plt.plot(x_time, y_test_rows0, 'b', linewidth=3, label='Actual sensor panel 1')
        plt.plot(x_time, predictions0, 'r', label='Model prediction')
        plt.legend()
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        # plt.show()
        plot_name = f'{report_dir}/{test_file}_pred.png'
        fig.savefig(plot_name)
        plt.clf()

    if gradcam:
        for indx, x_test_row in enumerate(x_test_rows):
            # Calculate the importance scores for each input feature
            grads = get_gradients(model, tf.convert_to_tensor(np.reshape(x_test_row, (1, 60))))
            scores = tf.reduce_mean(grads, axis=0).numpy()
            #print(indx, scores)
            # Visualize the importance scores using a heatmap
            plt.title(f'Grad-CAM {tf_model_name}, {test_file}, {indx}')
            plt.imshow(scores.reshape(3, 20), cmap='hot')
            plt.colorbar()
            plt.show()

#CALCULATE ACCURACY
count_1 = 0
sum_1 = 0
sum_2 = 0
for a, b in zip(all_act, all_mod):
    if a == 1:
        count_1 += 1
        sum_1 += b
    else:
        sum_2 += (1-b)
acc_1 = sum_1/count_1
acc_2 = sum_2/(len(all_act) - count_1)
print('\n****************************\n')
print(f'{tf_model_name} accuracy on NO anomalies (0): ', round(acc_2, 4))
print(f'{tf_model_name} accuracy on ANOMALIES (1): ', round(acc_1, 4))

#MAKE REPORT
if make_report:
    # Generate the HTML report
    print('\nMaking HTML report file [...in progress...]')
    # Create an HTML page with captions for each plot
    html_template = '<html><head><title>TF test report {}</title></head><body><h1>TF test report {}</h1><h3>Test time: {}</h3><h3>Model name: {}</h3><h3>Model type: {}</h3><h3>Model description: {}</h3><h3>Model data size: {}</h3><br><h2>Test results:</h2><h3>Accuracy on NO anomalies (0): {}</h3><h3>Accuracy on ANOMALIES (1): {}</h3>{}</body></html>'
    figure_template = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"><img src="{}"></div></figure>'
    figure_template1 = '<figure><div><img src="{}"></div><figcaption>{}</figcaption></figure>'
    # find couple plots
    files = os.listdir(report_dir)
    couples = []
    for filename in files:
        match = re.match(r'^(.*)_mod\.png$', filename)
        if match:
            couple = [match.group(1) + '_sens.png', match.group(1) + '_mod.png', match.group(1) + '_pred.png']
            if couple[1] in files:
                couples.append(couple)
    # print(couples)

    figure_html = ''
    plt_id = 0
    plot_file1 = 'nn2.png'
    plot_file2 = 'input_weights.png'
    fig_caption = f'Figure {plt_id}: a) model structure (made with http://alexlenail.me/NN-SVG/index.html)     b) Input data weight comparison'
    figure_html += figure_template.format(plot_file1, plot_file2, fig_caption)
    plt_id += 1
    for couple in couples:
        plot_file1 = couple[0]
        plot_file2 = couple[1]
        plot_file3 = couple[2]
        fig_caption = f'Figure {plt_id}: model inferences on {plot_file1}'
        figure_html += figure_template.format(plot_file1, plot_file2)
        figure_html += figure_template1.format(plot_file3, fig_caption)
        plt_id += 1

    html_content = html_template.format(id, id, date_time, model_name, model_type, model_desc, model_size, round(acc_2, 4), round(acc_1, 4),
                                        figure_html)
    with open(f'{report_dir}/test_report_{id}.html', 'w') as f:
        f.write(html_content)
    print('HTML report file has been made')

#CONVERT TO TF LITE AND C ARRAY
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