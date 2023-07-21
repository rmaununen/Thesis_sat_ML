import os
import re
import shutil
import matplotlib.pyplot as plt
from PIL import Image

'''************************************** SET INPUT PARAMS ***************************************'''
#REPORT PARAMETERS
id = '1.1' #'2.9.1' #test ID that will be printed in the report name header
report_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Test_TFL_on_MSP"
report_directory_name = f'TFL_test_report_{id}'

#MODEL PARAMETERS
model_name = 'adm_3_8.h'#'adm_2_9.h'
tf_model_name = 'adm_3_8'#'adm_2_9'
model_type = 'MLP' # (ignore recall, precision, F1 and FAR results)'
model_desc = '17x96x96x96x4 MLP to detect anomalies on 4 panels based on 4 x 10 temperature measurements + 4 derivatives + 1 time. Trained to detect sensor spikes, const regions, temp shifts and bumps. Tested on previously unseen data. Detection threshold = 0.85' #(removed duplicates)'# and costant regions, temperature shifts and bumps. '
model_size = 24368#24368 #8192
n_points_inp = 17#85
n_points_out = 4#8
n_series = 3#20
n_test_sets = 32

#RESCALE PLOTS
scale_factor = 0.6

#DATETIME PARAMETERS
import datetime
now = datetime.datetime.now()
formatted_date_time = now.strftime("%d/%m/%Y %H:%M")
date_time = '02.07.2023'#formatted_date_time #Change this if you want the time to be something else

acc_2 = 0.0000
acc_1 = 0.0000
t_per_inf = 0.126
end_time = 915.975
t_per_inf = 0.14
end_time = 1023.097
recall = 0.8588
precision = 0.8988
F1 = 0.8784
FAR = 0.0213


#Copy files into the new directory
os.chdir(report_directory)
report_directory_name_old = report_directory_name

report_directory_name += 'r'
if not os.path.exists(report_directory_name):
    os.makedirs(report_directory_name)
def copy_files(source_dir, destination_dir):
    try:
        # Check if the source directory exists
        if not os.path.exists(source_dir):
            print(f"Source directory '{source_dir}' does not exist.")
            return

        # Check if the destination directory exists, create it if not
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Get a list of all files in the source directory
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        # Copy each file to the destination directory
        for file in files:
            if not "test_report" in file:
                source_path = os.path.join(source_dir, file)
                destination_path = os.path.join(destination_dir, file)
                shutil.copy2(source_path, destination_path)
                #print(f"File '{file}' copied to '{destination_dir}'.")
        print("All files copied successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

copy_files(report_directory_name_old, report_directory_name)

#Rescale plots in the new directory
def rescale_plot(input_path, output_path, scale_factor):
    # Load the plot image
    image = Image.open(input_path)

    # Get the current size of the image
    current_width, current_height = image.size

    # Calculate the new size after scaling
    new_width = int(current_width * scale_factor)
    new_height = int(current_height * scale_factor)

    # Rescale the image
    resized_image = image.resize((new_width, new_height))

    # Save the rescaled image
    resized_image.save(output_path)

for filename in os.listdir(report_directory_name):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            input_path = os.path.join(report_directory_name, filename)
            output_path = input_path
            rescale_plot(input_path, output_path, scale_factor)


# Generate the HTML report
print('\nMaking HTML report file [...in progress...]')
# Create an HTML page with captions for each plot
html_template = '<html><head><title>TF Lite Micro test report {}</title></head><body><h1>TF Lite Micro test report {}</h1><h3>Test time: {}</h3><h3>Model name: {}</h3><h3>Model type: {}</h3><h3>Model description: {}</h3><h3>Model data size: {} [Bytes]</h3><br><br><br><br><br><br><br><br><h2>Test results:</h2><h3>Accuracy on NO anomalies (0): {}</h3><h3>Accuracy on ANOMALIES (1): {}</h3><h3>Time per inference: {} [s]</h3><h3>Total test time: {} [s]</h3><h3>recall: {}</h3><h3>precision: {}</h3><h3>F1 score: {}</h3><h3>False alarm rate: {}</h3><br><br><br><br><br><br><br><br><br><br><br><br><br><br><h2>Anomaly-free telemetry</h2>{}</body></html>'
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
            fig_caption = f'Figure {plt_id}: model inferences on {plot_file1[:-9]}'
            figure_html += figure_template0.format(plot_file0)
            figure_html += figure_template1.format(plot_file1, plot_file2)
            figure_html += figure_template3.format(plot_file3, plot_file4, fig_caption)
            if plt_id == 1:
                figure_html += '<br><br><br><br><br><br><br><br><br><br><br><br><h2>Outlier anomalies</h2>'
            if plt_id == 8:
                figure_html += '<br><br><br><br><br><br><br><br><br><br><br><br><h2>Flat regions</h2>'
            if plt_id == 20:
                figure_html += '<br><br><br><br><br><br><br><br><br><br><br><br><h2>Permanent bias</h2>'
            if plt_id == 26:
                figure_html += '<br><br><br><br><br><br><br><br><br><br><br><br><h2>Temporary bias</h2>'
            plt_id += 1

html_content = html_template.format(id, id, date_time, model_name, model_type, model_desc, model_size,
                                    'N/A', 'N/A', #round(acc_2, 4), round(acc_1, 4),
                                    t_per_inf, end_time, round(recall, 4), round(precision, 4), round(F1, 4), round(FAR, 4),
                                    figure_html)
with open(f'{report_directory_name}/test_report_{id}.html', 'w') as f:
    f.write(html_content)
print('HTML report file has been made')