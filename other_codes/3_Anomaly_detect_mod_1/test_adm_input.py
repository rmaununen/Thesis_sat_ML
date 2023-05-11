'''
This is the input file to test an anomaly detecting model (TF, NOT TFL)
    *   DO NOT CHANGE THE FILE NAME.
    *   DO NOT CHANGE THE VARIABLE NAMES.
    *   Use absolute paths for directories.
'''
import datetime

#REPORT PARAMETERS
id = 1.5 #test ID that will be printed in the report name header
#report_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Test_TFL_on_MSP"

#MODEL PARAMETERS
#model_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1"
threshold_out = 0.2
model_name = f'adm_13.h  (WITH THRESHOLD OUTPUT CLASSIFICATION {threshold_out})'
tf_model_name = 'adm_13'  #The existing model

model_type = 'MLP'
model_desc = '60x32x32x32x2 MLP to detect based on the previous 20 points from 3 panels, and predict the next point on panel 1. Tested on previously unseen data.'
model_size = 'NA'
n_points_inp = 60

#TELEMETRY PARAMETERS
#telemetry_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1/telemetry_FUNCUBE"
#individual_files = []#["output_bp_286.txt"] # The code makes tests on all telemetry pieces in the telemetry_directory,
# however, if you make this list not empty, the tests will be done only on the files you specify in the list, eg. ["output_ab_123.txt", "output_cd_456.txt"]

#DATETIME PARAMETERS
now = datetime.datetime.now()
formatted_date_time = now.strftime("%d/%m/%Y %H:%M")
date_time = '05.05.2023'#formatted_date_time #Change this if you want the time to be something else