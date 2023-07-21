import os
import numpy as np


'''*********************   FUNCTIONS TO MAKE ANOMALIES IN TIME SERIES (LISTS)   **************************'''

def make_const_sensor_anomaly(list, k, n, value=None): #INPUT LIST IS ANY TYPE
    # k is the starting index where the constant values should begin
    # n is the number of elements to make constant
    if value != None:
        constant_value = value
    else:
        constant_value = list[k]
    # Update the list to make the elements constant
    list_out = []
    for l in list:
        list_out.append(str(l))
    if n == 1:
        labl = 'a'
    else:
        labl = 'b'
    list_out[k:k + n] = [str(constant_value) + labl] * n
    return list_out #STRING


def shift_temp(list, dir, magnitude): #INPUT LIST IS ANY TYPE
    list_out = []
    if dir == 1: #dir 1 i up, 0 is down
        for v in list:
            list_out.append(str(round((float(v)+magnitude), 2)) + 'c')
    else:
        for v in list:
            list_out.append(str(round((float(v)-magnitude), 2)) + 'd')
    return list_out #STRING


def bump_temp(list, dir, k, n, peak_magn): #INPUT LIST IS ANY TYPE
    # k is the starting index where the bump should start
    # n is the number of elements for which the bump lasts
    lst = [float(l) for l in list]
    # Define the bell-shaped bump as a Gaussian distribution
    bump = [peak_magn * (1 / (n * 0.4 * (2 * 3.1415) ** 0.5)) * 2.71828 ** (-(i - n / 2) ** 2 / (2 * (n * 0.4) ** 2))
            for i in range(n)]
    # Modify the values in the list starting at index k
    for i in range(k, min(k + n, len(lst))):
        if dir == 1:
            lst[i] += bump[i - k]
        else:
            lst[i] -= bump[i - k]
    list_out = [str(round((l), 2)) for l in lst]
    for i in range(k, min(k + n, len(list_out))):
        list_out[i] += 'e'
    return list_out #STRING


def corrupt_clock(clk_list, factor): #INPUT LIST IS ANY TYPE
    list_out = []
    for l in clk_list:
        list_out.append(str(factor*float(l))+'a')
    return list_out #STRING

'''
Not used
def shift_clock(clk_list, shift):
    list_out = []
    if shift > 0:
        return 0
    for l in clk_list:
        list_out.append(str(factor * float(l)) + 'a')
    return list_out  # STRING
    '''



'''*********************   FUNCTIONS TO NORMALIZE AND DENORMALIZE VALUES   **************************'''

def normalize_list (in_list, normal_min, normal_max, already_normalised_indx): #INPUT LIST IS ANY TYPE
    out_list = []
    for i, v in enumerate(in_list):
        if i == already_normalised_indx:
            out_list.append(str(v))
        else:
            normal_v = round((float(v) - normal_min) / (normal_max - normal_min), 4)
            out_list.append(str(normal_v))
    return out_list #STRING

def denormalize_list (in_list, normal_min, normal_max, already_normalised_indx): #INPUT LIST IS ANY TYPE
    out_list = []
    for i, v in enumerate(in_list):
        if (i != None) and (i == already_normalised_indx):
            out_list.append(str(v))
        else:
            denormal_v = round((float(v) * (normal_max - normal_min)) + normal_min, 2)
            out_list.append(str(denormal_v))
    return out_list #STRING

def denormalize_value (in_value, normal_min, normal_max): #INPUT VALUE IS ANY TYPE
    denormal_v = round((float(in_value) * (normal_max - normal_min)) + normal_min, 2)
    return denormal_v #FLOAT

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

'''
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
    print("Output file has been filled with normalized values")
'''
#NOT IN USE ^




'''*********************   FUNCTIONS TO WRITE AND READ FILES AND LISTS   **************************'''

def telemetry_to_str_list(file_name, directory): #INPUT IS TELEMETRY FILE (SINGLE COLUMN)
    current_working_directory = os.getcwd()
    os.chdir(directory)
    # Read the values from the file into a list
    values = []
    with open(file_name, "r") as f:
        for line in f:
            values.append(line.strip())
    os.chdir(current_working_directory)
    return values

def str_to_float_list(list):
    out_list = [float(l) for l in list]
    return out_list

def list_to_telemetry_file(list, file, directory):
    current_working_directory = os.getcwd()
    os.chdir(directory)
    with open(file, 'w') as f:
        for val in list:
            f.write(str(val) + '\n')
    os.chdir(current_working_directory)
    return file



'''************   FUNCTIONS TO HELP CONVERT TELEMETRY FILES (with and without anomalies) TO DATASETS  ************'''

def get_current_anomaly_status(list): #INPUT VALUE IS STRING
    if any(char.isalpha() for char in str(list[-1])):
        out_list = ['1.0']
    else:
        out_list = ['0.0']
    return out_list

def get_current_sensor_slope(list):
    slope_inp = [float(list[-3]), float(list[-2]), float(list[-1])]
    der = np.gradient(slope_inp, 0.3)[-1]
    slope_val = round(min(1.0, abs(der)), 4)
    return [str(slope_val)]

def remove_anomaly_labels(list):
    out_list = []
    for l in list:
        out_list.append(l.replace('a', '').replace('b', '').replace('c', '').replace('d', '').replace('e', ''))
    return out_list
