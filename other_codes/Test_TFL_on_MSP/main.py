'''
This is the exe file for TFL Micro testing framework for MSP432.
    *   All input variables can be changed in main_input.py
    *   The order in which the data is sent to MSP is IMPORTANT, do not change.
'''

import matplotlib.pyplot as plt
import serial
import time
import os
import re
import numpy as np
from main_input import *
from normalize_functions import *

report_directory_name = f'TFL_test_report_{id}'
if not os.path.exists(report_directory_name):
    os.makedirs(report_directory_name)

serialcom = serial.Serial(serial_port_name, baudrate=serial_baudrate, timeout=serial_timeout)


time_init = time.time_ns() // 1000000
time_start = time_init
print('Starting time:', 0, '[s]')

com_tag = '>>>>>>>'

#SENDING MODEL DATA SIZE
print('\nSending model data size to MSP [...in progress...]')
serialcom.write((str(model_size)+'\n').encode())
print('Model data size has been sent\n')
time_init = time.time_ns() // 1000000
time_now = time_init
while (time_now - time_init) <= 20:#[ms]
    time_now = time.time_ns() // 1000000
    # Read line from serial (if there is anything to read)
    l = serialcom.readline().decode().rstrip()
    if len(l) > 5:
        print(com_tag+l)

#SENDING MODEL INPUT SIZE
print('\nSending model input size to MSP [...in progress...]')
serialcom.write((str(n_points_inp)+'\n').encode())
print('Model input size has been sent\n')
time_init = time.time_ns() // 1000000
time_now = time_init
while (time_now - time_init) <= 20:#[ms]
    time_now = time.time_ns() // 1000000
    # Read line from serial (if there is anything to read)
    l = serialcom.readline().decode().rstrip()
    if len(l) > 5:
        print(com_tag+l)

#SENDING MODEL OUTPUT SIZE
print('\nSending model output size to MSP [...in progress...]')
serialcom.write((str(n_points_out)+'\n').encode())
print('Model output size has been sent\n')
time_init = time.time_ns() // 1000000
time_now = time_init
while (time_now - time_init) <= 20:#[ms]
    time_now = time.time_ns() // 1000000
    # Read line from serial (if there is anything to read)
    l = serialcom.readline().decode().rstrip()
    if len(l) > 5:
        print(com_tag+l)
print('Current time:', (time_now-time_start)/1000, '[s]')

#SENDING MODEL DATA
print('\nSending model data to MSP [...in progress...]')
os.chdir(model_directory)
mod_dat = []
with open(model_name, "r") as f:
    for line in f:
        # Split the line into values
        array = line.strip().split(', ')
        for ar in array:
            if (len(ar)>2) and ('0x' in ar):
                mo = ar.replace(',', '')
                mod_dat.append(mo)
# Close file
f.close()
#mod_dat = ['0x00']
for m in mod_dat:
    m += '\n'
    serialcom.write(m.encode())
    '''
    time_init = time.time_ns() // 1000000
    time_now = time_init
        while (time_now - time_init) <= 50: #<- FOR DEBUGGING
        time_now = time.time_ns() // 1000000
        # Read line from serial (if there is anything to read)
        l = serialcom.readline().decode().rstrip()
        if len(l) > 0:
            print(l)
    '''
print('Model data has been sent\n')

#Check for status reports from MSP
time_init = time.time_ns() // 1000000
time_now = time_init
while (time_now - time_init) <= 1000: #[ms] Try to increase this value if there are problems with initialization
    time_now = time.time_ns() // 1000000
    # Read line from serial (if there is anything to read)
    l = serialcom.readline().decode().rstrip()
    if len(l) > 4:
        print(com_tag+l)
print('Current time:', (time_now-time_start)/1000, '[s]')



#######################    SENDING INPUT DATA    #######################
all_diff = np.array([])
all_act = []
all_mod = []
while reading:
    open_file = True
    for dataset_file_name in os.listdir(dataset_dir):
        if (not single_sensor) and (dataset_file_name.startswith("dataset_")) and ('1187' in dataset_file_name):
            # Check if there are specific files to include in testing
            if len(individual_files) != 0:
                open_file = False
                for i in individual_files:
                    if i == dataset_file_name:
                        open_file = True
                        break
            # Read and transmit file contents
            if open_file:
                os.chdir(dataset_dir)
                # Pre-inference time check
                time_now = time.time_ns() // 1000000
                pre_inf_time = (time_now - time_start) / 1000

                with open(dataset_file_name, "r") as f:
                    x_time = []
                    x_time_act = []
                    t = 0
                    y_act_1 = []
                    y_act_2 = []
                    y_act_3 = []
                    y_act_4 = []
                    sens_1 = []
                    sens_2 = []
                    sens_3 = []
                    sens_4 = []
                    y_mod_1 = []
                    y_mod_2 = []
                    y_mod_3 = []
                    y_mod_4 = []
                    print("\nTesting on", dataset_file_name, " [...in progress...]")
                    for line in f:
                        # Split the line into values
                        values = line.strip().split()

                        y_act_1.append(
                            float(values[0]))  # (denormalize_value(float(values[0]), normal_min, normal_max))
                        y_act_2.append(float(values[1]))
                        y_act_3.append(float(values[2]))
                        y_act_4.append(float(values[3]))
                        sens_1.append(denormalize_value(float(values[12 + n_series]), normal_min,
                                                        normal_max))  # subject to change
                        sens_2.append(denormalize_value(float(values[12 + 2 * n_series]), normal_min,
                                                        normal_max))  # subject to change
                        sens_3.append(denormalize_value(float(values[12 + 3 * n_series]), normal_min,
                                                        normal_max))  # subject to change
                        sens_4.append(denormalize_value(float(values[12 + 4 * n_series]), normal_min,
                                                        normal_max))  # subject to change
                        x_time_act.append(
                            round(denormalize_value(float(values[12]), t_normal_min, t_normal_max)))  # subject to change
                        x_time.append(t)
                        t += 1
                        x_values = values[-n_points_inp:]
                        for v in x_values:
                            v = str(v) + "\n"
                            serialcom.write(v.encode())
                            # check for response:
                            '''
                            time_init = time.time_ns() // 1000000
                            time_now = time_init
                            while (time_now - time_init) <= 20: #<- FOR DEBUGGING
                                time_now = time.time_ns() // 1000000
                                # Read line from serial (if there is anything to read)
                                l = serialcom.readline().decode().rstrip()
                                if len(l) > 0:
                                    print(l)
                            '''
                        inference_flag = 'iii\n'
                        serialcom.write(inference_flag.encode())

                        # Look for inference results
                        outputs_lts = []
                        time_init = time.time_ns() // 1000000
                        time_now = time_init
                        while (
                                time_now - time_init) <= 100:  # [ms] Try to increase this value if there are problems with inferences or outputs
                            time_now = time.time_ns() // 1000000
                            # Read line from serial (if there is anything to read)
                            l = serialcom.readline().decode().rstrip()
                            # if len(l) > 0:
                            #    print(l)
                            if "Output" in l:
                                out = float(l[8:])
                                outputs_lts.append(out)
                            elif 'E' in l:  # check for errors
                                print(com_tag + l)
                        y_mod_1.append(outputs_lts[0])
                        y_mod_2.append(outputs_lts[1])
                        y_mod_3.append(outputs_lts[2])
                        y_mod_4.append(outputs_lts[3])
                # Write finish flag to Serial
                finish_flag = 'fff\n'
                serialcom.write(finish_flag.encode())
                # Post-inference time check
                time_now = time.time_ns() // 1000000
                post_inf_time = (time_now - time_start) / 1000
                t_per_inf = round((post_inf_time - pre_inf_time) / (t + 1), 3)
                print('Current time:', post_inf_time, '[s]')
                print('Time taken for all inferences: ', round(post_inf_time - pre_inf_time, 3), '[s]')
                print('Time per inference: ', t_per_inf, '[s]')
                # Close file
                f.close()
                #POST_PROCESS RECEIVED OUTPUTS
                pred_lst1 = []
                pred_lst2 = []
                pred_lst3 = []
                pred_lst4 = []
                if filter_thrshld:
                    for p in y_mod_1:
                        if p < threshold_out:
                            pred_lst1.append(0)
                        else:
                            pred_lst1.append(1)
                    for p in y_mod_2:
                        if p < threshold_out:
                            pred_lst2.append(0)
                        else:
                            pred_lst2.append(1)
                    for p in y_mod_3:
                        if p < threshold_out:
                            pred_lst3.append(0)
                        else:
                            pred_lst3.append(1)
                    for p in y_mod_4:
                        if p < threshold_out:
                            pred_lst4.append(0)
                        else:
                            pred_lst4.append(1)
                else:
                    if limit_val:
                        for p in y_mod_1:
                            if p < 0:
                                pred_lst1.append(0)
                            elif p > 1:
                                pred_lst1.append(1)
                            else:
                                pred_lst1.append(p)
                        for p in y_mod_2:
                            if p < 0:
                                pred_lst2.append(0)
                            elif p > 1:
                                pred_lst2.append(1)
                            else:
                                pred_lst2.append(p)
                        for p in y_mod_3:
                            if p < 0:
                                pred_lst3.append(0)
                            elif p > 1:
                                pred_lst3.append(1)
                            else:
                                pred_lst3.append(p)
                        for p in y_mod_4:
                            if p < 0:
                                pred_lst4.append(0)
                            elif p > 1:
                                pred_lst4.append(1)
                            else:
                                pred_lst4.append(p)
                    else:
                        pred_lst1 = y_mod_1
                        pred_lst2 = y_mod_2
                        pred_lst3 = y_mod_3
                        pred_lst4 = y_mod_4

                    # add up all model inference results for later acuracy analysis
                    all_act += y_act_1 + y_act_2 + y_act_3 + y_act_4
                    all_mod += pred_lst1 + pred_lst2 + pred_lst3 + pred_lst4

                    if plot_tests:
                        os.chdir(report_directory)
                        #    +X     Model classification output vs actual label
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        plt.clf()
                        plt.title(f'Actual +X vs model {tf_model_name}, {dataset_file_name}')
                        plt.plot(x_time, y_act_1, 'black', linewidth=3, label='Actual anomaly label')
                        plt.plot(x_time, pred_lst1, 'b', label='Model output')
                        # for time:
                        plt.xticks(x_time, [int(t) for t in x_time_act])
                        plt.locator_params(axis='x', nbins=20)
                        plt.legend()
                        plt.xlabel('Time [min]')
                        plt.ylabel('Anomaly probability [-]')
                        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                        plot_name = f'{report_directory_name}/{dataset_file_name}_mod1.png'
                        fig.savefig(plot_name)
                        plt.clf()

                        #    -X     Model classification output vs actual label
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        plt.clf()
                        plt.title(f'Actual -X vs model {tf_model_name}, {dataset_file_name}')
                        plt.plot(x_time, y_act_2, 'black', linewidth=3, label='Actual anomaly label')
                        plt.plot(x_time, pred_lst2, 'r', label='Model output')
                        # for time:
                        plt.xticks(x_time, [int(t) for t in x_time_act])
                        plt.locator_params(axis='x', nbins=20)
                        plt.legend()
                        plt.xlabel('Time [min]')
                        plt.ylabel('Anomaly probability [-]')
                        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                        plot_name = f'{report_directory_name}/{dataset_file_name}_mod2.png'
                        fig.savefig(plot_name)
                        plt.clf()

                        #    +Y     Model classification output vs actual label
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        plt.clf()
                        plt.title(f'Actual +Y vs model {tf_model_name}, {dataset_file_name}')
                        plt.plot(x_time, y_act_3, 'black', linewidth=3, label='Actual anomaly label')
                        plt.plot(x_time, pred_lst3, 'g', label='Model output')
                        # for time:
                        plt.xticks(x_time, [int(t) for t in x_time_act])
                        plt.locator_params(axis='x', nbins=20)
                        plt.legend()
                        plt.xlabel('Time [min]')
                        plt.ylabel('Anomaly probability [-]')
                        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                        plot_name = f'{report_directory_name}/{dataset_file_name}_mod3.png'
                        fig.savefig(plot_name)
                        plt.clf()

                        #    -Y     Model classification output vs actual label
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        plt.clf()
                        plt.title(f'Actual -Y vs model {tf_model_name}, {dataset_file_name}')
                        plt.plot(x_time, y_act_4, 'black', linewidth=3, label='Actual anomaly label')
                        plt.plot(x_time, pred_lst4, 'c', label='Model output')
                        # for time:
                        plt.xticks(x_time, [int(t) for t in x_time_act])
                        plt.locator_params(axis='x', nbins=20)
                        plt.legend()
                        plt.xlabel('Time [min]')
                        plt.ylabel('Anomaly probability [-]')
                        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                        plot_name = f'{report_directory_name}/{dataset_file_name}_mod4.png'
                        fig.savefig(plot_name)
                        plt.clf()

                        # Telemetry from the three panel sensors
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        plt.clf()
                        plt.title(f'Temperature sensors, {dataset_file_name}')
                        plt.plot(x_time, sens_1, 'b', label='Panel 1 (+X)')
                        plt.plot(x_time, sens_2, 'r', label='Panel 2 (-X)')
                        plt.plot(x_time, sens_3, 'g', label='Panel 3 (+Y)')
                        plt.plot(x_time, sens_4, 'c', label='Panel 4 (-Y)')
                        # for time:
                        plt.xticks(x_time, [int(t) for t in x_time_act])
                        plt.locator_params(axis='x', nbins=20)
                        plt.legend()
                        plt.xlabel('Time [min]')
                        plt.ylabel('Temperature [deg C]')
                        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                        plot_name = f'{report_directory_name}/{dataset_file_name}_sens.png'
                        fig.savefig(plot_name)
                        plt.clf()

        #****************************************   Old code for ptm model   ******************************************
        elif single_sensor:
            #Check if there are specific files to include in testing
            if dataset_file_name.startswith("output_"):
                if len(individual_files) != 0:
                    open_file = False
                    for i in individual_files:
                        if i == dataset_file_name:
                            open_file = True
                            break
                #Read and transmit file contents
                if open_file:
                    os.chdir(telemetry_directory)
                    with open(dataset_file_name, "r") as f:
                        x_time = []
                        t = 0
                        y_act = []
                        y_mod = []
                        print("Testing on", dataset_file_name, " [...in progress...]")
                        for line in f:
                            # Split the line into values
                            values = line.strip().split()
                            v = values[0] + "\n"
                            y_act.append(float(values[0]))
                            x_time.append(t)
                            t += 1
                            serialcom.write(v.encode())
                            time_init = time.time_ns() // 1000000
                            time_now = time_init
                            while (time_now - time_init) <= 20:
                                time_now = time.time_ns() // 1000000
                                # Read line from serial (if there is anything to read)
                                l = serialcom.readline().decode().rstrip()
                                #if len(l) > 0:
                                #    print(l)
                                if "Output" in l:
                                    out = float(l[8:])
                                    y_mod.append(out)
                    #Write finish flag to Serial
                    finish_flag = 'fff'
                    serialcom.write(finish_flag.encode())
                    # Close file
                    f.close()

                    #######################    PLOT RESULTS    #######################
                    if plot_tests:
                        #Make plot in the current directory
                        os.chdir(report_directory)
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        plt.clf()
                        plt.title("Comparison of predictions to actual values")
                        ymin = 1.05 * min(min(y_mod), min(y_act))
                        ymax = 1.05 * max(max(y_mod), max(y_act))
                        x_st = n_points_inp*np.ones(3)
                        y_st = [ymin, 0, ymax]
                        plt.plot(x_time, y_act, 'b', label='Actual values')
                        plt.plot(x_time, y_mod, 'r', label='Model predictions')
                        plt.plot(x_st, y_st, 'darkgreen')
                        plt.xlabel('time [min]')#, fontsize=20)
                        plt.ylabel('T [dec C]')#, fontsize=20)
                        plt.legend()
                        plt.ylim(ymin, ymax)
                        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                        plt.show()
                        # Save the plot to a file
                        plot_name = f'{report_directory_name}/{dataset_file_name}_results.png'
                        fig.savefig(plot_name)
                        #Make absolute error plot
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        plt.clf()
                        diff = abs(np.array(y_act)-np.array(y_mod))
                        all_diff = np.concatenate((all_diff, diff))
                        rms = np.sqrt(np.mean(diff ** 2))
                        plt.title(f"Absolute value of error.    RMS = {round(rms, 4)} deg C.")
                        plt.plot(x_time, diff, 'b')
                        ymin = 1.05 * min(diff)
                        ymax = 1.05 * max(diff)
                        y_st = [ymin, 0, ymax]
                        plt.plot(x_st, y_st, 'darkgreen')
                        plt.xlabel('time [min]')#, fontsize=20)
                        plt.ylabel('T [dec C]')#, fontsize=20)
                        plt.ylim(ymin, ymax)
                        plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                        plt.show()
                        # Save the plot to a file
                        plot_name = f'{report_directory_name}/{dataset_file_name}_error.png'
                        fig.savefig(plot_name)

    #########################   CALCULATE ACCURACY   #########################
    count_1 = 0
    sum_1 = 0
    sum_2 = 0
    for a, b in zip(all_act, all_mod):
        if a == 1:
            count_1 += 1
            sum_1 += b
        else:
            sum_2 += (1 - b)
    acc_1 = sum_1 / count_1
    acc_2 = sum_2 / (len(all_act) - count_1)
    print('\n****************************\n')
    print(f'{tf_model_name} accuracy on NO anomalies (0): ', round(acc_2, 4))
    print(f'{tf_model_name} accuracy on ANOMALIES (1): ', round(acc_1, 4))

    reading = False
#########################   MAKE REPORT   #########################
if make_report:
    os.chdir(report_directory)
    # Generate the HTML report
    print('\nMaking HTML report file [...in progress...]')
    # Create an HTML page with captions for each plot
    html_template = '<html><head><title>TFLite Micro test report {}</title></head><body><h1>TFLite Micro test report {}</h1><h3>Test time: {}</h3><h3>Model name: {}</h3><h3>Model type: {}</h3><h3>Model description: {}</h3><h3>Model data size: {} [Bytes]</h3><br><h2>Test results:</h2><h3>Accuracy on NO anomalies (0): {}</h3><h3>Accuracy on ANOMALIES (1): {}</h3><h3>Time per inference: {} [s]</h3><h3>Total test time: {} [s]</h3>{}</body></html>'
    figure_template3 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"><img src="{}"></div><figcaption>{}</figcaption></figure>'
    figure_template1 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"><img src="{}"></div></figure>'
    figure_template0 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"></div></figure>'
    figure_template2 = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"></div><figcaption>{}</figcaption></figure>'
    # find couple plots
    files = os.listdir(report_directory_name)
    couples = []
    for filename in files:
        match = re.match(r'^(.*)_mod1\.png$', filename)
        if match:
            couple = [match.group(1) + '_sens.png', match.group(1) + '_mod1.png', match.group(1) + '_mod2.png',
                      match.group(1) + '_mod3.png', match.group(1) + '_mod4.png']
            if couple[1] in files:
                couples.append(couple)
    figure_html = ''
    plt_id = 1
    for i in range(n_test_sets+1):
        str_key = '1187_'+str(i)+'_'
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
    time_now = time.time_ns() // 1000000
    end_time = (time_now - time_start) / 1000
    #acc_2 = 0.8698
    #acc_1 = 0.7554
    #t_per_inf = 0.126
    #end_time = 915.975
    html_content = html_template.format(id, id, date_time, model_name, model_type, model_desc, model_size,
                                        round(acc_2, 4), round(acc_1, 4), t_per_inf, end_time,
                                        figure_html)
    with open(f'{report_directory_name}/test_report_{id}.html', 'w') as f:
        f.write(html_content)
    print('HTML report file has been made')

'''
#######################    Generate the HTML report    #######################
if make_report:
    print('\nMaking HTML report file [...in progress...]')
    rms = round(np.sqrt(np.mean(all_diff ** 2)), 4)
    # Create an HTML page with captions for each plot
    html_template = '<html><head><title>TFL test report {}</title></head><body><h1>TFL test report {}</h1><h3>Test time: {}</h3><h3>Model name: {}</h3><h3>Model type: {}</h3><h3>Model description: {}</h3><h3>Model data size: {}</h3><br><h2>Test results:</h2><h3>RMS on all tests: {} [deg C]</h3>{}</body></html>'
    figure_template = '<figure><div style="display: flex; flex-direction: row;"><img src="{}"><img src="{}"></div><figcaption>{}</figcaption></figure>'
    #find couple plots
    files = os.listdir(report_directory_name)
    couples = []
    for filename in files:
        match = re.match(r'^(.*)_results\.png$', filename)
        if match:
            couple = [match.group(1) + '_results.png', match.group(1) + '_error.png']
            if couple[1] in files:
                couples.append(couple)
    figure_html = ''
    plt_id = 1
    for couple in couples:
        plot_file1 = couple[0]
        plot_file2 = couple[1]
        fig_caption = f'Figure {plt_id}: model predictions on {plot_file1}'
        figure_html += figure_template.format(plot_file1, plot_file2, fig_caption)
        plt_id += 1
    html_content = html_template.format(id, id, date_time, model_name, model_type, model_desc, model_size, rms, figure_html)
    with open(f'{report_directory_name}/test_report_{id}.html', 'w') as f:
        f.write(html_content)
    print('HTML report file has been made')
'''

#######################    CLOSE SERIAL CONNECTION    #######################
serialcom.close()
print('\nDone')