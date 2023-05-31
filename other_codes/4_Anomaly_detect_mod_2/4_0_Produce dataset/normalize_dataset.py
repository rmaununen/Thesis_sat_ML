import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1'
Dataset_file = 'training_dataset_1_2.txt'
Normalized_dataset = 'training_dataset_1_2_n.txt'
already_normalised_indx = 1 #None
normal_min = -40
normal_max = 50

def normalize_in_file(Dataset_file, Normalized_dataset, already_normalised_indx, normal_min, normal_max):
    # Open the file in write mode and truncate its content
    with open(Normalized_dataset, "w") as file:
        file.truncate(0)
    print("Output file contents have been cleared\n")

    print("Normalizing dataset values\n")
    with open(Dataset_file,'r') as f:
        with open(Normalized_dataset, 'w') as out_f:
            for line in f:
                values = line.strip().split()
                output_values = []
                for i, v in enumerate(values):
                    if i == already_normalised_indx:
                        output_values.append(v+' ')
                    else:
                        normal_v = round((float(v) - normal_min) / (normal_max - normal_min), 4)
                        output_values.append(str(normal_v)+' ')
                output_values.append('\n')
                out_f.writelines(output_values)
                output_values = []
    print("Output file has been filled with normalized values")

def normalize_list (in_list, normal_min, normal_max, already_normalised_indx):
    out_list = []
    for i, v in enumerate(in_list):
        if i == already_normalised_indx:
            out_list.append(v)
        else:
            normal_v = round((float(v) - normal_min) / (normal_max - normal_min), 4)
            out_list.append(str(normal_v))
    return out_list

def denormalise_list (in_list, normal_min, normal_max, already_normalised_indx):
    out_list = []
    for i, v in enumerate(in_list):
        if (i != None) and (i == already_normalised_indx):
            out_list.append(v)
        else:
            denormal_v = round((float(v) * (normal_max - normal_min)) + normal_min, 2)
            out_list.append(str(denormal_v))
    return out_list

def denormalise_array (in_array, normal_min, normal_max, already_normalised_indx):
    out_list = []
    in_list = in_array.flatten().tolist()
    for i, v in enumerate(in_list):
        if (i != None) and (i == already_normalised_indx):
            out_list.append(v)
        else:
            denormal_v = round((float(v) * (normal_max - normal_min)) + normal_min, 2)
            out_list.append(denormal_v)
    return out_list

def denormalize_value (in_value, normal_min, normal_max):
    denormal_v = round((in_value * (normal_max - normal_min)) + normal_min, 2)
    return denormal_v