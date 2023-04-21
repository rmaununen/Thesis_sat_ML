import matplotlib.pyplot as plt
import serial
import time
import os
import re
import sys
import numpy as np

model_name = 'ptm_1.h'
model_desc = ''
model_size = ''
date_time = ''
n_points_inp = 30

current_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Test_TFL_on_MSP"
telemetry_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Predicting_therm_model_1/telemetry_FUNCUBE"
model_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Predicting_therm_model_1"

id = 0
report_directory_name = f'TFL_test_report_{id}'
if not os.path.exists(report_directory_name):
    os.makedirs(report_directory_name)

serialcom = serial.Serial('/dev/cu.usbmodemM43210051', baudrate=115200, timeout=0.01) #Change port name to the one you are using


#SENDING MODEL DATA
print('Sending model data to MSP [...in progress...]')
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
    time_init = time.time_ns() // 1000000
    time_now = time_init
    '''
        while (time_now - time_init) <= 50: #<- FOR DEBUGGING
        time_now = time.time_ns() // 1000000
        # Read line from serial (if there is anything to read)
        l = serialcom.readline().decode().rstrip()
        if len(l) > 0:
            print(l)
    '''
    time.sleep(0.005)
    #print(m)
#Write finish flag to Serial
#finish_flag = '---\n'
#serialcom.write(finish_flag.encode())
print('Model data has been sent\n')

#Check for any error reports from MSP
time_init = time.time_ns() // 1000000
time_now = time_init
while (time_now - time_init) <= 1000:
    time_now = time.time_ns() // 1000000
    # Read line from serial (if there is anything to read)
    l = serialcom.readline().decode().rstrip()
    if len(l) > 4:
        print(l)

#SENDING INFERENCE DATA
reading = True
while reading:
    for output_file_name in os.listdir(telemetry_directory):
        if output_file_name.startswith("output_") and (output_file_name == "output_bp_286.txt"):
            os.chdir(telemetry_directory)
            with open(output_file_name, "r") as f:
                x_time = []
                t = 0
                y_act = []
                y_mod = []
                print("Testing on", output_file_name, " [...in progress...]")
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
                    while (time_now - time_init) <= 50:
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
            #Make plot in the current directory
            os.chdir(current_directory)
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
            plt.legend()
            plt.ylim(ymin, ymax)
            plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
            plt.show()
            # Save the plot to a file
            plot_name = f'{report_directory_name}/{output_file_name}_results.png'
            fig.savefig(plot_name)
            #Make absolute error plot
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.clf()
            plt.title("Difference between predictions and actual data (absolute value)")
            diff = abs(np.array(y_act)-np.array(y_mod))
            plt.plot(x_time, diff, 'b')
            ymin = 1.05 * min(diff)
            ymax = 1.05 * max(diff)
            y_st = [ymin, 0, ymax]
            plt.plot(x_st, y_st, 'darkgreen')
            plt.ylim(ymin, ymax)
            plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
            plt.show()
            # Save the plot to a file
            plot_name = f'{report_directory_name}/{output_file_name}_error.png'
            fig.savefig(plot_name)

    # Generate the HTML report
    print('Making HTML report file')
    nplots = 57*2
    # Create an HTML page with captions for each plot
    html_template = '<html><head><title>TFL test report {}</title></head><body><h1>TFL test report {}</h1>{}</body></html>'
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
    print(couples)

    figure_html = ''
    plt_id = 1
    for couple in couples:
        plot_file1 = couple[0]
        plot_file2 = couple[1]
        fig_caption = f'Figure {plt_id}: model predictions on {plot_file1}'
        figure_html += figure_template.format(plot_file1, plot_file2, fig_caption)
        plt_id += 1

    html_content = html_template.format(id, id, figure_html)
    with open(f'{report_directory_name}/test_report_{id}.html', 'w') as f:
        f.write(html_content)
    print('HTML report file has been made')
    # Close serial port
    serialcom.close()
    print('Done')
    reading = False