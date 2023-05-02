'''
This is the input file for TFL Micro testing framework for MSP432.
    *   DO NOT CHANGE THE FILE NAME.
    *   DO NOT CHANGE THE VARIABLE NAMES.
    *   Use absolute paths for directories.
'''
import datetime

#REPORT PARAMETERS
id = 0.1 #test ID that will be printed in the report name header
report_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Test_TFL_on_MSP"

#MODEL PARAMETERS
model_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1"
model_name = 'ptm_1_1.h'
model_type = 'MLP'
model_desc = '30x16x16x16x1 MLP to predict the next temperature point based on the previous 30 points \n (Same as ptm_1.h, but with improved quantization)'
model_size = 3952
n_points_inp = 30

#SERIAL PORT PARAMETERS
serial_port_name = '/dev/cu.usbmodemM43210051'
serial_baudrate = 115200
serial_timeout = 0.01 # Delay for reading

#TELEMETRY PARAMETERS
telemetry_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1/telemetry_FUNCUBE"
individual_files = []#["output_bp_286.txt"] # The code makes tests on all telemetry pieces in the telemetry_directory,
# however, if you make this list not empty, the tests will be done only on the files you specify in the list, eg. ["output_ab_123.txt", "output_cd_456.txt"]

#DATETIME PARAMETERS
now = datetime.datetime.now()
formatted_date_time = now.strftime("%d/%m/%Y %H:%M")
date_time = formatted_date_time #Change this if you want the time to be something else