import matplotlib.pyplot as plt
from dataset_functions import *
import fnmatch
import random

#Working_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2'
Telemetry_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Telemetry'
Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Dataset'
main_panel = '+X'

test_anomaly_functions = False

overwrite_telemetries_with_a = False
t_a_free = False
t_a_spike = False
t_a_const = False
t_a_shift = False
t_a_bump = False
ind = 16

normal_min = -40
normal_max = 50

training_dataset_name = 'training_dataset_2_0.txt'

'''************   FUNCTION TO CONVERT TELEMETRY FILES (with and without anomalies) TO A (part of a) DATASET  ************'''
def telemetry_files_to_dataset(N, filenames, out_file_name, directory, normal_min, normal_max):
    # N is the length of each panel time series
    filename_1, filename_2, filename_3 = filenames[0], filenames[1], filenames[2]
    # Create a new file for the concatenated sequences
    os.chdir(directory)
    with open(out_file_name, "w") as output_file:
        # Read the values from the telemetry files into lists
        values1 = telemetry_to_str_list(filename_1, Telemetry_dir)
        values2 = telemetry_to_str_list(filename_2, Telemetry_dir)
        values3 = telemetry_to_str_list(filename_3, Telemetry_dir)

        #Make all possible series of N consecutive points
        for i in range(len(values1) - (N+1)):

            sequence1 = values1[i:i + N]
            sequence2 = values2[i:i + N]
            sequence3 = values3[i:i + N]

            # ADD NEXT POINT PREDICTION OUTPUT
            sequence02 = [str(values1[i+N+1])]

            # ADD AMOMALY PROBABILITY OUTPUT
            sequence03 = get_current_anomaly_status(sequence1)

            # Remove the 'a' labels from data
            sequence1 = remove_anomaly_labels(sequence1)
            sequence02 = remove_anomaly_labels(sequence02)

            # Normalize lists that need to be normalized
            sequence1 = normalize_list(sequence1, normal_min, normal_max, None)
            sequence2 = normalize_list(sequence2, normal_min, normal_max, None)
            sequence3 = normalize_list(sequence3, normal_min, normal_max, None)
            sequence02 = normalize_list(sequence02, normal_min, normal_max, None)

            # ADD SENSOR DATA SLOPE OUTPUT
            sequence01 = get_current_sensor_slope(sequence1)

            sequence = sequence01 + sequence02 + sequence03 + sequence1 + sequence2 + sequence3
            output_file.write(" ".join(str(v) for v in sequence) + "\n")



'''************   FUNCTION TO MAKE TELEMETRY FILES WITH ANOMALIES   ************'''
def make_telemetry_files_with_anomalies(start_ind):
    t_parts = ['44', '163', '286', '529', '775', '1042', '1187']

    if overwrite_telemetries_with_a:
        for filename in os.listdir(Telemetry_dir):
            if '_a_' in filename:
                os.remove(os.path.join(Telemetry_dir, filename))

    for t_part in t_parts:

        ind = start_ind

        # GET THE THREE MAIN (ANOMALY-FREE) TELEMETRY FILES FOR THE CURRENT t_part
        pattern = f'*{t_part}*'
        # filter the list of files based on the pattern
        matching_files = [filename for filename in os.listdir(Telemetry_dir) if ((not "a" in filename) and fnmatch.fnmatch(filename, pattern))]
        # RESOLVE THE THREE PANELS
        file1 = ''  # +X
        file2 = ''  # -X
        file3 = ''  # +Y
        for fi in matching_files:
            if '+X' in fi:
                file1 = fi
        for fi in matching_files:
            if '-X' in fi:
                file2 = fi
        for fi in matching_files:
            if '+Y' in fi:
                file3 = fi

        if t_a_free:
            # make ANOMALY-FREE datasets
            ind = 0
            #filenames = [file1, file2, file3]
            #telemetry_files_to_dataset(20, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

        if t_a_spike:
            # make datasets with SPIKE ANOMALIES
            for i in range(7):
                ind += 1
                fil_lst = telemetry_to_str_list(file1, Telemetry_dir)
                fil_lst = str_to_float_list(fil_lst)
                k = random.randint(20, len(fil_lst) - 3)
                n = random.randint(1, 2)
                dir = random.randint(1, 2)
                if dir == 1:
                    a = 1
                else:
                    a = -1
                value = fil_lst[k] + a * random.randint(10, 30)
                list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
                spike_file = list_to_telemetry_file(list1, file1[:-4] + f'_a_{ind}.txt', Telemetry_dir)
                #filenames = [spike_file, file2, file3]
                #telemetry_files_to_dataset(20, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

        if t_a_const:
            # make datasets with CONSTANT ANOMALIES with no offset
            for i in range(3):
                ind += 1
                fil_lst = telemetry_to_str_list(file1, Telemetry_dir)
                n = random.randint(10, 30)
                k = random.randint(20, len(fil_lst) - n)
                list1 = make_const_sensor_anomaly(fil_lst, k, n, None)
                const_file = list_to_telemetry_file(list1, file1[:-4] + f'_a_{ind}.txt', Telemetry_dir)
                #filenames = [const_file, file2, file3]
                #telemetry_files_to_dataset(20, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

        if t_a_const:
            # make datasets with CONSTANT ANOMALIES with offsets
            for i in range(3):
                ind += 1
                fil_lst = telemetry_to_str_list(file1, Telemetry_dir)
                fil_lst = str_to_float_list(fil_lst)
                n = random.randint(10, 30)
                k = random.randint(20, len(fil_lst) - n)
                dir = random.randint(1, 2)
                if dir == 1:
                    a = 1
                else:
                    a = -1
                value = fil_lst[k] + a * random.randint(10, 30)
                list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
                const_file = list_to_telemetry_file(list1, file1[:-4] + f'_a_{ind}.txt', Telemetry_dir)
                #filenames = [const_file, file2, file3]
                #telemetry_files_to_dataset(20, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

        if t_a_const:
            # make datasets with CONSTANT ANOMALIES with offsets and not returning to normal
            for i in range(3):
                ind += 1
                fil_lst = telemetry_to_str_list(file1, Telemetry_dir)
                fil_lst = str_to_float_list(fil_lst)
                k = random.randint(20, len(fil_lst) - 30)
                n = len(fil_lst) - k
                dir = random.randint(1, 2)
                if dir == 1:
                    a = 1
                else:
                    a = -1
                value = fil_lst[k] + a * random.randint(10, 30)
                list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
                const_file = list_to_telemetry_file(list1, file1[:-4] + f'_a_{ind}.txt', Telemetry_dir)
                #filenames = [const_file, file2, file3]
                #telemetry_files_to_dataset(20, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

        if t_a_shift:
            # make telemetry files with TEMPERATURE SHIFT ANOMALIES
            for i in range(4):
                ind += 1
                fil_lst = telemetry_to_str_list(file1, Telemetry_dir)
                dir = random.randint(1, 2)
                if dir == 1:
                    a = 1
                else:
                    a = -1
                fil_lst = shift_temp(fil_lst, a, random.randint(10, 20))
                shift_file = list_to_telemetry_file(fil_lst, file1[:-4] + f'_a_{ind}.txt', Telemetry_dir)

        if t_a_bump:
            # make telemetry files with TEMPERATURE BUMP ANOMALIES
            for i in range(5):
                ind += 1
                fil_lst = telemetry_to_str_list(file1, Telemetry_dir)
                dir = random.randint(1, 2)
                if dir == 1:
                    a = 1
                else:
                    a = -1
                fil_lst = bump_temp(fil_lst, a, random.randint(10, len(fil_lst)-17), random.randint(9, 17), random.randint(80, 120))
                shift_file = list_to_telemetry_file(fil_lst, file1[:-4] + f'_a_{ind}.txt', Telemetry_dir)

#make_telemetry_files_with_anomalies(ind)

def make_datasets(normal_min, normal_max):
    t_parts = ['44', '163', '286', '529', '775', '1042', '1187']
    for t_part in t_parts:
        ind = 1
        # GET THE THREE MAIN (ANOMALY-FREE) TELEMETRY FILES FOR THE CURRENT t_part
        pattern = f'*{t_part}*'
        # filter the list of files based on the pattern
        matching_files = [filename for filename in os.listdir(Telemetry_dir) if ((not "a" in filename) and fnmatch.fnmatch(filename, pattern))]
        # RESOLVE THE THREE PANELS
        file1 = ''  # +X
        file2 = ''  # -X
        file3 = ''  # +Y
        for fi in matching_files:
            if '+X' in fi:
                file1 = fi
        for fi in matching_files:
            if '-X' in fi:
                file2 = fi
        for fi in matching_files:
            if '+Y' in fi:
                file3 = fi

        # make ANOMALY-FREE datasets
        ind = 0
        filenames = [file1, file2, file3]
        telemetry_files_to_dataset(20, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)
        for i in range(25):
            ind += 1
            file1_a = file1[:-4] + f'_a_{ind}.txt'
            filenames = [file1_a, file2, file3]
            telemetry_files_to_dataset(20, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

#make_datasets(normal_min, normal_max)

# COMBINE DATASETS
def produce_dataset(training_dataset_name):
    with open(training_dataset_name, 'a') as output_file:
        for filename in os.listdir(Dataset_dir):
            if (not '1187' in filename):# and (filename[-1] == '0') and (filename[-2] == '_'):  # SELECT THE PART TO BE LEFT FOR TESTING,
                # in this case 1187 (and the anomaly-free parts because they are redundant for training)
                file_path = os.path.join(Dataset_dir, filename)
                with open(file_path, "r") as input_file:
                    # read all lines from the file
                    lines = input_file.readlines()
                    # write the lines to the output file
                    output_file.writelines(lines)

produce_dataset(training_dataset_name)

if test_anomaly_functions:
    for telemetry_file_name in os.listdir(Telemetry_dir):
        for i in range(5):
            if main_panel in telemetry_file_name and (telemetry_file_name == f'output_+X_163_a_{21+i}.txt'):
                list = telemetry_to_str_list(telemetry_file_name, Telemetry_dir)
                #list = str_to_float_list(list)
                # list1 = make_const_sensor_anomaly(list, 30, len(list)-30, value=35)
                #list = shift_temp(list, -1, 10)

                #dir = random.randint(1, 2)
                #if dir == 1:
                #    a = 1
                #else:
                #    a = -1

                #list = bump_temp(list, a, random.randint(10, len(list)-17), random.randint(9, 17), random.randint(80, 120))
                #list = bump_temp(list, 1, 10, 10, 80)
                #list = [0] * 30 + list[:len(list) - 30] #SHIFT TIME
                list = remove_anomaly_labels(list)
                list = str_to_float_list(list)
                plt.plot(list, label='Modified', c="g")
                plt.xlabel('time', fontsize=15)
                plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                plt.minorticks_on()
                plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                plt.legend()
                plt.show()




'''
                    #FOR ANOMALLY FREE PREDICTIONS
                    l44 = []
                    l163 = []
                    l286 = []
                    l529 = []
                    l775 = []
                    l1042 = []
                    prev_line = []
                    for line in f:
                        # Split the line into values
                        values = line.strip().split()
                        val = [str(v) + ' ' for v in values[:]]
                        prev_line.insert(0, val[20])
                        if len(prev_line) > 2:
                            if '44' in filename:
                                l44.append(prev_line[0])
                            elif '163' in filename:
                                l163.append(prev_line[0])
                            elif '286' in filename:
                                l286.append(prev_line[0])
                            elif '529' in filename:
                                l529.append(prev_line[0])
                            elif '775' in filename:
                                l775.append(prev_line[0])
                            elif '1042' in filename:
                                l1042.append(prev_line[0])
                            prev_line.append('\n')
                            # output_file.writelines(prev_line)
                        prev_line = val

        # loop through all files in the directory§
        for filename in os.listdir(Dataset_dir):
            if not '1187' in filename:  # SELECT THE PART TO BE LEFT FOR TESTING, in this case 1187
                # get the full path of the file
                file_path = os.path.join(Dataset_dir, filename)

                with open(file_path, "r") as f:
                    prev_line = []
                    i = -1
                    for line in f:
                        # Split the line into values
                        values = line.strip().split()
                        val = [str(v) + ' ' for v in values[:]]
                        # prev_line.insert(0, val[20])
                        if i > -1:
                            if '44' in filename:
                                prev_line.insert(0, l44[i])
                            elif '163' in filename:
                                prev_line.insert(0, l163[i])
                            elif '286' in filename:
                                prev_line.insert(0, l286[i])
                            elif '529' in filename:
                                prev_line.insert(0, l529[i])
                            elif '775' in filename:
                                prev_line.insert(0, l775[i])
                            elif '1042' in filename:
                                prev_line.insert(0, l1042[i])
                        i += 1
                        if len(prev_line) > 2:
                            prev_line.append('\n')
                            output_file.writelines(prev_line)
                        prev_line = val
                    '''

'''
            else:
                # get the full path of the file
                file_path = os.path.join(Dataset_dir, filename)

                with open(file_path, "r") as f:
                    with open(f'{filename}_new.txt', 'w') as out_file:
                        prev_line = []
                        for line in f:
                            # Split the line into values
                            values = line.strip().split()
                            val = [str(v) + ' ' for v in values[:]]
                            prev_line.insert(0, val[20])
                            if len(prev_line) > 2:
                                prev_line.append('\n')
                                out_file.writelines(prev_line)
                            prev_line = val
                # open the file in read mode
                with open(file_path, 'r') as input_file:

                    # read all lines from the file
                    lines = input_file.readlines()

                    # write the lines to the output file
                    output_file.writelines(lines)
                '''