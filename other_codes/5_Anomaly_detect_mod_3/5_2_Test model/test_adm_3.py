import sys
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
import tensorflow as tf
import numpy as np
import math
import matplotlib.pyplot as plt
from other_codes.tfl_converter_tools import *
from test_adm_input import *
from normalize_dataset import *
import os
import re
print(os.getcwd())

#########################   GET MODEL   #########################
os.chdir(Model_dir1)
model = tf.keras.models.load_model(tf_model_name+'.h5')
os.chdir(Working_dir1)

#########################   GET INPUT WEIGHTS   #########################
Weights0 = model.layers[0].get_weights()[0]
print('Sum of absolute values of input layer weights per input layer neuron.')
weights_abs_sum = []
for i in range(len(Weights0)):
    weights_abs_sum.append(np.sum(np.abs(Weights0[i])))
weights_abs_sum = [0] * (N_series-1) + [weights_abs_sum[0]] +  [0] * (N_series-1) + [weights_abs_sum[1]] + \
                  [0] * (N_series-1) + [weights_abs_sum[2]] + [0] * (N_series-1) + [weights_abs_sum[3]] + \
                  [0] * (N_series-1) + [weights_abs_sum[4]] + weights_abs_sum[5:]
weight_arr = np.array(weights_abs_sum)
print('Input layer weights:')
print(weight_arr)
print('------------------------------')
# Plot scores using a heatmap
fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(weight_arr.reshape(9, N_series), cmap='hot')
plt.title(f'Sum of abs. weights per inp. layer neuron, {tf_model_name}')
plt.colorbar()
plt.show()
plot_name = f'{Report_dir1}/input_weights.png'
fig.savefig(plot_name)



#########################   TEST PERFORMANCE   #########################

#List to estimate accuracy
all_act = []
all_mod = []
for test_file in os.listdir(Dataset_dir1):
    os.chdir(Dataset_dir1)
    x_test_rows = []
    x_test_dat_1 = []
    x_test_dat_2 = []
    x_test_dat_3 = []
    x_test_dat_4 = []
    y_test_rows1 = []
    y_test_rows2 = []
    y_test_rows3 = []
    y_test_rows4 = []
    with open(test_file, "r") as f:
        for line in f:
            # Split the line into values
            values = line.strip().split()
            #values = normalize_list(values, normal_min, normal_max, already_normalised_indx)
            if len(values) == N_i + N_o + 4 + 68:
                # Extract the input and output values
                #x = [float(v) for v in values[-N_i:]]
                x = [float(v) for v in values[8:]]
                x = x[:5] + x[15+7:25] + x[35+7:45] +x[55+7:65] +x[75+7:85]
                x_test_rows.append(x)
                x_test_dat_1.append(x[N_series + 4])
                x_test_dat_2.append(x[2*N_series + 4])
                x_test_dat_3.append(x[3*N_series + 4])
                x_test_dat_4.append(x[4*N_series + 4])
                y1 = float(values[0]) # ANOMALY STATUS p1 +X
                y_test_rows1.append(y1)
                y2 = float(values[1])  # ANOMALY STATUS p2 -X
                y_test_rows2.append(y2)
                y3 = float(values[2])  # ANOMALY STATUS p3 +Y
                y_test_rows3.append(y3)
                y4 = float(values[3])  # ANOMALY STATUS p4 -Y
                y_test_rows4.append(y4)
                #y2 = float(values[1]) #PREDICTION
                #y_test_rows2.append(denormalize_value(y1, normal_min, normal_max))
    x_test_dat_1 = denormalise_list(x_test_dat_1, normal_min, normal_max, None)
    x_test_dat_2 = denormalise_list(x_test_dat_2, normal_min, normal_max, None)
    x_test_dat_3 = denormalise_list(x_test_dat_3, normal_min, normal_max, None)
    x_test_dat_4 = denormalise_list(x_test_dat_4, normal_min, normal_max, None)
    if not 'x' in test_file:
        predictions = model.predict(np.array(x_test_rows))
    #predictions1 = predictions[:, 0] #CHANGED TEMPORARILY  #PREDICTION
    #print('1:       ', predictions0)
    #predictions1 = denormalise_array(predictions1, normal_min, normal_max, None)
    #print('2:       ', predictions0)
    predictions1 = predictions[:, 0] #CHANGED TEMPORARILY   #ANOMALY STATUS p1
    predictions2 = predictions[:, 1]  # CHANGED TEMPORARILY   #ANOMALY STATUS p2
    predictions3 = predictions[:, 2]  # CHANGED TEMPORARILY   #ANOMALY STATUS p3
    predictions4 = predictions[:, 3]  # CHANGED TEMPORARILY   #ANOMALY STATUS p4
    pred_lst01 = predictions1.flatten().tolist()
    pred_lst02 = predictions2.flatten().tolist()
    pred_lst03 = predictions3.flatten().tolist()
    pred_lst04 = predictions4.flatten().tolist()
    pred_lst1 = []
    pred_lst2 = []
    pred_lst3 = []
    pred_lst4 = []
    if filter_thrshld:
        for p in pred_lst01:
            if p < threshold_out:
                pred_lst1.append(0)
            else:
                pred_lst1.append(1)
        for p in pred_lst02:
            if p < threshold_out:
                pred_lst2.append(0)
            else:
                pred_lst2.append(1)
        for p in pred_lst03:
            if p < threshold_out:
                pred_lst3.append(0)
            else:
                pred_lst3.append(1)
        for p in pred_lst04:
            if p < threshold_out:
                pred_lst4.append(0)
            else:
                pred_lst4.append(1)
    else:
        if limit_val:
            for p in pred_lst01:
                if p < 0:
                    pred_lst1.append(0)
                elif p > 1:
                    pred_lst1.append(1)
                else:
                    pred_lst1.append(p)
            for p in pred_lst02:
                if p < 0:
                    pred_lst2.append(0)
                elif p > 1:
                    pred_lst2.append(1)
                else:
                    pred_lst2.append(p)
            for p in pred_lst03:
                if p < 0:
                    pred_lst3.append(0)
                elif p > 1:
                    pred_lst3.append(1)
                else:
                    pred_lst3.append(p)
            for p in pred_lst04:
                if p < 0:
                    pred_lst4.append(0)
                elif p > 1:
                    pred_lst4.append(1)
                else:
                    pred_lst4.append(p)
        else:
            pred_lst1 = pred_lst01
            pred_lst2 = pred_lst02
            pred_lst3 = pred_lst03
            pred_lst4 = pred_lst04
    #TIME
    '''
    x_time = []
    t = 0
    for i in range(len(y_test_rows)):
        x_time.append(t)
        t+=1
    '''
    #TIME WITH REFERENCE
    x_time_o = telemetry_to_str_list('clock_1187.txt', Time_dir1)
    x_time_o = str_to_float_list(x_time_o)[20:-1] #Replaced N_series with 20

    x_time = range(len(x_time_o))

    if ('1187' in test_file):
        #add up all model inference results for later acuracy analysis
        all_act += y_test_rows1 + y_test_rows2 + y_test_rows3 + y_test_rows4
        all_mod += pred_lst1 + pred_lst2 + pred_lst3 + pred_lst4 #predictions1.flatten().tolist()
        #print current test file name
        print(test_file)

    if plot_tests and ('1187' in test_file):
        #    +X     Model classification output vs actual label
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Actual +X vs model {tf_model_name}, {test_file}')
        plt.plot(x_time, y_test_rows1, 'black', linewidth=3, label='Actual anomaly label')
        plt.plot(x_time, pred_lst1, 'b', label='Model output')
        #for time:
        plt.xticks(x_time, [int(t) for t in x_time_o])
        plt.locator_params(axis='x', nbins=20)
        plt.legend()
        plt.xlabel('Time [min]')
        plt.ylabel('Anomaly probability [-]')
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        x_values = np.array(x_test_rows)
        y_values = np.array(y_test_rows1)
        plot_name = f'{Report_dir1}/{test_file}_mod1.png'
        fig.savefig(plot_name)
        plt.clf()

        #    -X     Model classification output vs actual label
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Actual -X vs model {tf_model_name}, {test_file}')
        plt.plot(x_time, y_test_rows2, 'black', linewidth=3, label='Actual anomaly label')
        plt.plot(x_time, pred_lst2, 'r', label='Model output')
        # for time:
        plt.xticks(x_time, [int(t) for t in x_time_o])
        plt.locator_params(axis='x', nbins=20)
        plt.legend()
        plt.xlabel('Time [min]')
        plt.ylabel('Anomaly probability [-]')
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        plot_name = f'{Report_dir1}/{test_file}_mod2.png'
        fig.savefig(plot_name)
        plt.clf()

        #    +Y     Model classification output vs actual label
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Actual +Y vs model {tf_model_name}, {test_file}')
        plt.plot(x_time, y_test_rows3, 'black', linewidth=3, label='Actual anomaly label')
        plt.plot(x_time, pred_lst3, 'g', label='Model output')
        # for time:
        plt.xticks(x_time, [int(t) for t in x_time_o])
        plt.locator_params(axis='x', nbins=20)
        plt.legend()
        plt.xlabel('Time [min]')
        plt.ylabel('Anomaly probability [-]')
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        plot_name = f'{Report_dir1}/{test_file}_mod3.png'
        fig.savefig(plot_name)
        plt.clf()

        #    -Y     Model classification output vs actual label
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Actual -Y vs model {tf_model_name}, {test_file}')
        plt.plot(x_time, y_test_rows4, 'black', linewidth=3, label='Actual anomaly label')
        plt.plot(x_time, pred_lst4, 'c', label='Model output')
        # for time:
        plt.xticks(x_time, [int(t) for t in x_time_o])
        plt.locator_params(axis='x', nbins=20)
        plt.legend()
        plt.xlabel('Time [min]')
        plt.ylabel('Anomaly probability [-]')
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        plot_name = f'{Report_dir1}/{test_file}_mod4.png'
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
        plt.plot(x_time, x_test_dat_4, 'c', label='Panel 4 (-Y)')
        # for time:
        plt.xticks(x_time, [int(t) for t in x_time_o])
        plt.locator_params(axis='x', nbins=20)
        plt.legend()
        plt.xlabel('Time [min]')
        plt.ylabel('Temperature [deg C]')
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        plot_name = f'{Report_dir1}/{test_file}_sens.png'
        fig.savefig(plot_name)
        plt.clf()

        # Model prediction vs actual sensor
        '''
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.clf()
        plt.title(f'Actual vs model prediction {tf_model_name}, {test_file}')
        plt.plot(x_time, y_test_rows0, 'b', linewidth=3, label='Actual sensor panel 1')
        plt.plot(x_time, predictions0, 'r', label='Model prediction')
        # for time:
        plt.xticks(x_time, [int(t) for t in x_time_o])
        plt.locator_params(axis='x', nbins=20)

        plt.legend()
        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
        # plt.show()
        plot_name = f'{report_dir}/{test_file}_pred.png'
        fig.savefig(plot_name)
        plt.clf()
        '''

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


#########################   CALCULATE ACCURACY   #########################
count_1 = 0
sum_1 = 0
sum_2 = 0
TP = 0
TN = 0
FP = 0
FN = 0
for a, b in zip(all_act, all_mod):
    if a == 1:
        count_1 += 1
        sum_1 += b
        if b == 1:
            TP += 1
        else:
            FN += 1
    else:
        sum_2 += (1-b)
        if b == 0:
            TN += 1
        else:
            FP += 1

acc_1 = sum_1/count_1
acc_2 = sum_2/(len(all_act) - count_1)

recall = TP/(TP+FN)
precision = TP/(TP + FP)
F1 = (2*precision*recall)/(precision+recall)
FAR = FP/(TN+FP)
print('\n****************************\n')
print(f'{tf_model_name} accuracy on NO anomalies (0): ', round(acc_2, 4))
print(f'{tf_model_name} accuracy on ANOMALIES (1): ', round(acc_1, 4))

print(f'\n{tf_model_name} recall: ', round(recall, 4))
print(f'{tf_model_name} precision: ', round(precision, 4))
print(f'{tf_model_name} F1: ', round(F1, 4))
print(f'{tf_model_name} FAR: ', round(FAR, 4))



#########################   MAKE REPORT   #########################
if make_report:
    # Generate the HTML report
    print('\nMaking HTML report file [...in progress...]')
    # Create an HTML page with captions for each plot
    html_template = '<html><head><title>TF test report {}</title></head><body><h1>TF test report {}</h1><h3>Test time: {}</h3><h3>Model name: {}</h3><h3>Model type: {}</h3><h3>Model description: {}</h3><h3>Model data size: {}</h3><br><h2>Test results:</h2><h3>Accuracy on NO anomalies (0): {}</h3><h3>Accuracy on ANOMALIES (1): {}</h3><h3>recall: {}</h3><h3>precision: {}</h3><h3>F1 score: {}</h3><h3>False alarm rate: {}</h3>{}</body></html>'
    figure_template3 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"><img src="{}"></div><figcaption>{}</figcaption></figure>'
    figure_template1 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"><img src="{}"></div></figure>'
    figure_template0 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"></div></figure>'
    figure_template2 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"></div><figcaption>{}</figcaption></figure>'
    # find couple plots
    files = os.listdir(Report_dir1)
    couples = []
    for filename in files:
        match = re.match(r'^(.*)_mod1\.png$', filename)
        if match:
            couple = [match.group(1) + '_sens.png', match.group(1) + '_mod1.png', match.group(1) + '_mod2.png', match.group(1) + '_mod3.png', match.group(1) + '_mod4.png']
            if couple[1] in files:
                couples.append(couple)
    figure_html = ''
    plt_id = 0
    plot_file1 = 'nn2.png'
    plot_file2 = 'input_weights.png'
    fig_caption = f'Figure {plt_id}: a) model structure (made with http://alexlenail.me/NN-SVG/index.html)     b) Input data weight comparison'
    figure_html += figure_template3.format(plot_file1, plot_file2, fig_caption)
    plt_id += 1
    for i in range(n_test_sets + 1):
        str_key = '1187_' + str(i) + '_'
        for couple in couples:
            if str_key in couple[0]:
                plot_file0 = couple[0]
                plot_file1 = couple[1]
                plot_file2 = couple[2]
                plot_file3 = couple[3]
                plot_file4 = couple[4]
                fig_caption = f'Figure {plt_id}: model inferences on {plot_file1}'
                figure_html += figure_template0.format(plot_file0)
                figure_html += figure_template1.format(plot_file1, plot_file2)
                figure_html += figure_template3.format(plot_file3, plot_file4, fig_caption)
                plt_id += 1
    html_content = html_template.format(id, id, date_time, model_name, model_type, model_desc, model_size, round(acc_2, 4), round(acc_1, 4), round(recall, 4), round(precision, 4), round(F1, 4), round(FAR, 4),
                                        figure_html)
    with open(f'{Report_dir1}/test_report_{id}.html', 'w') as f:
        f.write(html_content)
    print('HTML report file has been made')

#########################   CONVERT TO TF LITE AND C ARRAY   #########################
if convert:
    # Convert Keras model to a tflite model
    # Get representative dataset from one of the test orbits
    os.chdir(Dataset_dir1)
    x_rep, y_rep = read_ptm_dataset(N_i, N_o, rep_dataset)
    x_rep = safety_factor * x_rep
    x_rep = np.round(x_rep, decimals=n_decimals_x)
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

    os.chdir(Working_dir1)
    open(tflite_model_name + '.tflite', 'wb').write(tflite_model)
    print('tflite model was saved')

    # Write TFLite model to a C source (or header) file
    with open(c_model_name + '.h', 'w') as file:
      file.write(hex_to_c_array(tflite_model, c_model_name))
    print('model was saved as C array')


    '''
    # Compare predictions
    y_test_pred_tflite = predict_tflite(tflite_model, x_rep, N_i)
    print('test inference of tflite model was performed')
    
    plt.clf()
    plt.title('Comparison of models against actual values')
    plt.plot(x_time, y_test_rows1, 'bo', label='Actual values')
    #plt.plot(x_time, predictions, 'ro', label='TF predictions')
    plt.plot(x_time, y_test_pred_tflite, 'g', label='TFLite quantized predictions')
    plt.legend()
    plt.show()
    '''
