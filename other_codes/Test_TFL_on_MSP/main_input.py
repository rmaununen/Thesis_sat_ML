'''
This is the input file for TFL Micro testing framework for MSP432.
    *   DO NOT CHANGE THE FILE NAME.
    *   DO NOT CHANGE THE VARIABLE NAMES.
    *   Use absolute paths for directories.
'''

#REPORT PARAMETERS
id = '4.9' #'2.9.1' #test ID that will be printed in the report name header
report_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Test_TFL_on_MSP"
report_directory_name = f'TFL_test_report_{id}'

#TEST PARAMETERS
n_test_sets = 32
single_series = False #False
reading = True
plot_tests = True
make_report = True#True

#MODEL PARAMETERS
model_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/5_Anomaly_detect_mod_3/5_2_Test model" #'/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1'
model_name = 'adm_3_8.h'#'adm_2_9.h'
tf_model_name = 'adm_3_8'#'adm_2_9'
model_type = 'MLP. Threshold 0.85. Time error +6 min'#No threshold (ignore recall, precision, F1 and FAR results) '
model_desc = '17x96x96x96x4 MLP to detect anomalies on 4 panels based on 4 x 10 temperature msmnts + 4 derivatives + 1 time. Tested on previously unseen data. Trained to detect sensor spikes, const regions, temp shifts and bumps. Removed prediction outputs.' #(removed duplicates)'# and costant regions, temperature shifts and bumps. '
model_size = 1#24368 #8192
n_points_inp = 17#85
n_points_out = 4#8
n_series = 3#20

normal_min = -40
normal_max = 50
t_normal_min = 0
t_normal_max = 100

#PROCESSING ANOMALY STATUSES
filter_thrshld = True
threshold_out = 0.85
limit_val = False

#SERIAL PORT PARAMETERS
serial_port_name = '/dev/cu.usbmodemM43210051'
serial_baudrate = 115200
serial_timeout = 0.01 # Delay for reading

#INPUT DATA PARAMETERS
telemetry_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1/telemetry_FUNCUBE"
dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/5_Anomaly_detect_mod_3/Dataset' #'/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1/telemetry_FUNCUBE'
individual_files = []#["output_bp_286.txt"] # The code makes tests on all telemetry pieces in the telemetry_directory,
# however, if you make this list not empty, the tests will be done only on the files you specify in the list, eg. ["output_ab_123.txt", "output_cd_456.txt"]

#DATETIME PARAMETERS
import datetime
now = datetime.datetime.now()
formatted_date_time = now.strftime("%d/%m/%Y %H:%M")
date_time = '02.07.2023'#formatted_date_time #Change this if you want the time to be something else