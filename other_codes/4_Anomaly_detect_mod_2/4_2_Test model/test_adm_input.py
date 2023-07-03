'''
This is the input file to test an anomaly detecting model (TF, NOT TFL)
    *   DO NOT CHANGE THE FILE NAME.
    *   DO NOT CHANGE THE VARIABLE NAMES.
    *   Use absolute paths for directories.
'''

#DIRECTORIES
Working_dir1 = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/4_2_Test model'
Dataset_dir1 = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Dataset'
Report_dir1 = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/4_2_Test model/TF_test_report'
Training_dir1 = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/4_1_Train model'
Time_dir1 = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Clock_telemetry'
Model_dir1 = Training_dir1

#REPORT PARAMETERS
id = '2.9' #test ID that will be printed in the report name header

#MODEL PARAMETERS
model_name = f'adm_2_9  (No threshold. follows anomalies. value limits 1/0 applied. Normalization applied.)' #(WITH THRESHOLD OUTPUT CLASSIFICATION {threshold_out}) same as adm_13 but trained not to follow anomalies'
tf_model_name = 'adm_2_9'  #The existing model
tflite_model_name = tf_model_name  # Will be given .tflite suffix
c_model_name = tf_model_name       # Will be given .h suffix
model_type = 'MLP'
model_desc = '85x32x32x32x8 MLP to detect anomalies on 4 panels based on the previous 20 points from 4 panels + 1 time point + derivatives of 4 panels. Tested on previously unseen data. Trained to detect sensor spikes, const regions, temp shifts and bumps'# (removed duplicates)'# and costant regions, temperature shifts and bumps. '
model_size = 'NA'
N_i = 85
N_o = 8
N_series = 20 #Number of temperature points used
normal_min = -40
normal_max = 50


#FUNCTIONS TO BE EXECUTED
convert = True
gradcam = False
plot_tests = False
make_report = False

#PROCESSING ANOMALY STATUSES
filter_thrshld = False
threshold_out = 0.15
limit_val = True

#DATETIME PARAMETERS
import datetime
now = datetime.datetime.now()
formatted_date_time = now.strftime("%d/%m/%Y %H:%M")
date_time = '30.06.2023'#formatted_date_time #Change this if you want the time to be something else


#CONVERSION TO TFLITE
rep_dataset = 'dataset_44_0'
nsamples = 60   # Number of samples to use as a representative dataset (<len(rep_dataset))
n_decimals_x = 4 # max number of decimals in the input tensor values
safety_factor = 1.6 # all input tensor values will be multiplied by this factor
# to make sure there will be no overflow during inferences on datasets with greater dynamic range



#TELEMETRY PARAMETERS
#telemetry_directory = "/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/2_Predicting_therm_model_1/telemetry_FUNCUBE"
#individual_files = []#["output_bp_286.txt"] # The code makes tests on all telemetry pieces in the telemetry_directory,
# however, if you make this list not empty, the tests will be done only on the files you specify in the list, eg. ["output_ab_123.txt", "output_cd_456.txt"]

n_points_inp = N_i

# For GRADCAM:   Define a function to calculate the gradient of the output with respect to each input
import tensorflow as tf
def get_gradients(model, inputs):
    with tf.GradientTape() as tape:
        tape.watch(inputs)
        outputs = model(inputs)
    grads = tape.gradient(outputs, inputs)
    return grads