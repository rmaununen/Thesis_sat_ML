'''
This is the input file for TFL Micro testing framework for MSP432.
    *   DO NOT CHANGE THE FILE NAME.
    *   DO NOT CHANGE THE VARIABLE NAMES.
    *   Use absolute paths for directories.
'''

#REPORT PARAMETERS
reading = False
plot_tests = False
make_report = True

single_sensor = False
id = 2.9 #test ID that will be printed in the report name header
report_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Test_TFL_on_MSP"

#MODEL PARAMETERS
model_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/4_2_Test model"
model_name = 'adm_2_9.h'
tf_model_name = 'adm_2_9'
model_type = 'MLP'
model_desc = '85x32x32x32x8 MLP to detect anomalies on 4 panels based on the previous 20 points from 4 panels + 1 time point + derivatives of 4 panels. Tested on previously unseen data. Trained to detect sensor spikes, const regions, temp shifts and bumps'# (removed duplicates)'
model_size = 8192
n_points_inp = 85
n_points_out = 8
n_series = 20

normal_min = -40
normal_max = 50
t_normal_min = 0
t_normal_max = 100

n_test_sets = 32

#PROCESSING ANOMALY STATUSES
filter_thrshld = False
threshold_out = 0.15
limit_val = True

#SERIAL PORT PARAMETERS
serial_port_name = '/dev/cu.usbmodemM43210051'
serial_baudrate = 115200
serial_timeout = 0.01 # Delay for reading

#INPUT DATA PARAMETERS
telemetry_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1/telemetry_FUNCUBE"
dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Dataset'
individual_files = []#["output_bp_286.txt"] # The code makes tests on all telemetry pieces in the telemetry_directory,
# however, if you make this list not empty, the tests will be done only on the files you specify in the list, eg. ["output_ab_123.txt", "output_cd_456.txt"]

#DATETIME PARAMETERS
import datetime
now = datetime.datetime.now()
formatted_date_time = now.strftime("%d/%m/%Y %H:%M")
date_time = '30.06.2023'#formatted_date_time #Change this if you want the time to be something else