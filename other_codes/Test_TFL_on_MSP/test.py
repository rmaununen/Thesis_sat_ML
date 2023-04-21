import matplotlib.pyplot as plt
import serial
import time
import os
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

#SENDING MODEL DATA
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
            #if '0' in ar[0]:
            #    for a in ar:
            #        ar.replace(',', '')
            #    mod_dat.append(ar)
    print(mod_dat)
    print(len(mod_dat))
for m in mod_dat:
    print(m)