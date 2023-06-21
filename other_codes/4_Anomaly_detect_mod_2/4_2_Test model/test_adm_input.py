'''
This is the input file to test an anomaly detecting model (TF, NOT TFL)
    *   DO NOT CHANGE THE FILE NAME.
    *   DO NOT CHANGE THE VARIABLE NAMES.
    *   Use absolute paths for directories.
'''
import datetime

#REPORT PARAMETERS
id = '2.4' #test ID that will be printed in the report name header
#report_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Test_TFL_on_MSP"

#MODEL PARAMETERS
#model_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1"
threshold_out = 0.15
model_name = f'adm_2_4  (No threshold. follows anomalies. value limits 1/0 applied. Normalization applied.)' #(WITH THRESHOLD OUTPUT CLASSIFICATION {threshold_out}) same as adm_13 but trained not to follow anomalies'
tf_model_name = 'adm_2_4'  #The existing model

model_type = 'MLP'
model_desc = '83x32x32x32x6 MLP to detect anomalies on 3 panels based on the previous 20 points from 3 panels + 20 time points + derivatives of 3 panels. Tested on previously unseen data. Trained to detect sensor spikes and const regions only.'# and costant regions, temperature shifts and bumps. '
model_size = 'NA'
n_points_inp = 83

#TELEMETRY PARAMETERS
#telemetry_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1/telemetry_FUNCUBE"
#individual_files = []#["output_bp_286.txt"] # The code makes tests on all telemetry pieces in the telemetry_directory,
# however, if you make this list not empty, the tests will be done only on the files you specify in the list, eg. ["output_ab_123.txt", "output_cd_456.txt"]

#DATETIME PARAMETERS
now = datetime.datetime.now()
formatted_date_time = now.strftime("%d/%m/%Y %H:%M")
date_time = '16.06.2023'#formatted_date_time #Change this if you want the time to be something else