import matplotlib.pyplot as plt
from dataset_functions import *
import fnmatch
import random

#Working_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2'
Telemetry_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Telemetry_multipanel'
Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Dataset'
Time_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Clock_telemetry'
Output_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/4_1_Train model'
#main_panel = '+X'


make_tel = False
make_time = False
make_sets = True
produce = True
balance = True
test_anomaly_functions = False

single_panel = False
overwrite_telemetries_with_a = False
t_a_free = False
t_a_spike = False
t_a_const = False
t_a_shift = False
t_a_bump = False
ind = 0
n_anomaly_files = 32

normal_min = -40
normal_max = 50

N_series = 20

training_dataset_name = 'training_dataset_2_9.txt'

'''************   FUNCTION TO CONVERT TELEMETRY FILES (with and without anomalies) TO A (part of a) DATASET  ************'''
def telemetry_files_to_dataset(N, filenames, out_file_name, directory, normal_min, normal_max):
    # N is the length of each panel time series
    filename_1, filename_2, filename_3, filename_4, filename_t = filenames[0], filenames[1], filenames[2], filenames[3], filenames[4]
    # Create a new file for the concatenated sequences
    os.chdir(directory)
    with open(out_file_name, "w") as output_file:
        # Read the values from the telemetry files into lists
        values1 = telemetry_to_str_list(filename_1, Telemetry_dir)
        values2 = telemetry_to_str_list(filename_2, Telemetry_dir)
        values3 = telemetry_to_str_list(filename_3, Telemetry_dir)
        values4 = telemetry_to_str_list(filename_4, Telemetry_dir)
        time_series = telemetry_to_str_list(filename_t, Time_dir)

        #Make all possible series of N consecutive points
        for i in range(len(values1) - (N+1)):

            sequence1 = values1[i:i + N]
            sequence2 = values2[i:i + N]
            sequence3 = values3[i:i + N]
            sequence4 = values4[i:i + N]
            sequencet = time_series[i:i + N]

            # ADD NEXT POINT PREDICTION OUTPUT
            sequence_p1 = [str(values1[i + N + 1])]
            sequence_p2 = [str(values2[i + N + 1])]
            sequence_p3 = [str(values3[i + N + 1])]
            sequence_p4 = [str(values4[i + N + 1])]

            # ADD AMOMALY PROBABILITY OUTPUT
            sequence_a1 = get_current_anomaly_status(sequence1)
            sequence_a2 = get_current_anomaly_status(sequence2)
            sequence_a3 = get_current_anomaly_status(sequence3)
            sequence_a4 = get_current_anomaly_status(sequence4)

            # Remove the 'a' labels from data
            sequence1 = remove_anomaly_labels(sequence1)
            sequence2 = remove_anomaly_labels(sequence2)
            sequence3 = remove_anomaly_labels(sequence3)
            sequence4 = remove_anomaly_labels(sequence4)
            sequence_p1 = remove_anomaly_labels(sequence_p1)
            sequence_p2 = remove_anomaly_labels(sequence_p2)
            sequence_p3 = remove_anomaly_labels(sequence_p3)
            sequence_p4 = remove_anomaly_labels(sequence_p4)

            # Normalize lists that need to be normalized
            sequence1 = normalize_list(sequence1, normal_min, normal_max, None)
            sequence2 = normalize_list(sequence2, normal_min, normal_max, None)
            sequence3 = normalize_list(sequence3, normal_min, normal_max, None)
            sequence4 = normalize_list(sequence4, normal_min, normal_max, None)
            sequence_p1 = normalize_list(sequence_p1, normal_min, normal_max, None)
            sequence_p2 = normalize_list(sequence_p2, normal_min, normal_max, None)
            sequence_p3 = normalize_list(sequence_p3, normal_min, normal_max, None)
            sequence_p4 = normalize_list(sequence_p4, normal_min, normal_max, None)
            sequencet = [normalize_list(sequencet, 0, 100, None)[-1]] #<-Only the last time point is taken

            # ADD SENSOR DATA SLOPE OUTPUT
            sequence_s1 = get_current_sensor_slope(sequence1)
            sequence_s2 = get_current_sensor_slope(sequence2)
            sequence_s3 = get_current_sensor_slope(sequence3)
            sequence_s4 = get_current_sensor_slope(sequence3)

            sequence = sequence_a1 + sequence_a2 + sequence_a3 + sequence_a4 + sequence_p1 + sequence_p2 + sequence_p3 + sequence_p4 + sequence_s1 + sequence_s2 + sequence_s3 + sequence_s4 + sequencet + sequence1 + sequence2 + sequence3 + sequence4
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
        file4 = ''  # -Y
        for fi in matching_files:
            if '+X' in fi:
                file1 = fi
        for fi in matching_files:
            if '-X' in fi:
                file2 = fi
        for fi in matching_files:
            if '+Y' in fi:
                file3 = fi
        for fi in matching_files:
            if '-Y' in fi:
                file4 = fi

        ############## FOR MULTIPLE PANELS ########################################################

        def random_reorder(input_list):
            output_list = list(input_list)  # Create a copy of the input list

            random.shuffle(output_list)  # Shuffle the copy

            return output_list

        def choose_dir():
            dir = random.randint(1, 2)
            if dir == 1:
                a = 1
            else:
                a = -1
            return a
        #Spikes
        #1 random panel
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        k = random.randint(20, len(fil_lst) - 3)
        n = random.randint(1, 2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        list2 = str_to_float_list(telemetry_to_str_list(file2r, Telemetry_dir))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        #2 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        k = random.randint(20, len(fil_lst) - 3)
        n = random.randint(1, 2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        #2 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        k = random.randint(20, len(fil_lst) - 3)
        n = random.randint(1, 2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = fil_lst2[k] + a * random.randint(10, 30)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        #3 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        k = random.randint(20, len(fil_lst) - 3)
        n = random.randint(1, 2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        #3 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        k = random.randint(20, len(fil_lst) - 3)
        n = random.randint(1, 2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = fil_lst2[k] + a * random.randint(10, 30)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        value = fil_lst3[k] + a * random.randint(10, 30)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        k = random.randint(20, len(fil_lst) - 3)
        n = random.randint(1, 2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        list4 = make_const_sensor_anomaly(fil_lst4, k, n, round(value, 2))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        k = random.randint(20, len(fil_lst) - 3)
        n = random.randint(1, 2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = fil_lst2[k] + a * random.randint(10, 30)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        value = fil_lst3[k] + a * random.randint(10, 30)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        a = choose_dir()
        value = fil_lst4[k] + a * random.randint(10, 30)
        list4 = make_const_sensor_anomaly(fil_lst4, k, n, round(value, 2))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)

        # Constant with offset
        # 1 random panel
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = random.randint(20, len(fil_lst) - n)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        list2 = str_to_float_list(telemetry_to_str_list(file2r, Telemetry_dir))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 2 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = random.randint(20, len(fil_lst) - n)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 2 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = random.randint(20, len(fil_lst) - n)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 3 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = random.randint(20, len(fil_lst) - n)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 3 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = random.randint(20, len(fil_lst) - n)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = random.randint(20, len(fil_lst) - n)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        list4 = make_const_sensor_anomaly(fil_lst4, k, n, round(value, 2))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = random.randint(20, len(fil_lst) - n)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, round(value, 2))
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, round(value, 2))
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        a = choose_dir()
        value = fil_lst[k] + a * random.randint(10, 30)
        list4 = make_const_sensor_anomaly(fil_lst4, k, n, round(value, 2))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)

        # Constant no offset, infinite length
        # 1 random panel
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = len(fil_lst) - n
        list1 = make_const_sensor_anomaly(fil_lst, k, n, None)
        list2 = str_to_float_list(telemetry_to_str_list(file2r, Telemetry_dir))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 2 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = len(fil_lst) - n
        list1 = make_const_sensor_anomaly(fil_lst, k, n, None)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, None)
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 3 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = len(fil_lst) - n
        list1 = make_const_sensor_anomaly(fil_lst, k, n, None)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, None)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, None)
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        n = random.randint(10, 30)
        k = len(fil_lst) - n
        list1 = make_const_sensor_anomaly(fil_lst, k, n, None)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = make_const_sensor_anomaly(fil_lst2, k, n, None)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = make_const_sensor_anomaly(fil_lst3, k, n, None)
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        list4 = make_const_sensor_anomaly(fil_lst4, k, n, None)
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)

        # Temperature shift
        # 1 random panel
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        value = random.randint(10, 20)
        list1 = shift_temp(fil_lst, a, value)
        list2 = str_to_float_list(telemetry_to_str_list(file2r, Telemetry_dir))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 2 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        value = random.randint(10, 20)
        list1 = shift_temp(fil_lst, a, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = shift_temp(fil_lst2, a, value)
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 2 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        value = random.randint(10, 20)
        list1 = shift_temp(fil_lst, a, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = random.randint(10, 20)
        list2 = shift_temp(fil_lst2, a, value)
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 3 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        value = random.randint(10, 20)
        list1 = shift_temp(fil_lst, a, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = shift_temp(fil_lst2, a, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = shift_temp(fil_lst3, a, value)
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 3 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        value = random.randint(10, 20)
        list1 = shift_temp(fil_lst, a, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = random.randint(10, 20)
        list2 = shift_temp(fil_lst2, a, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        value = random.randint(10, 20)
        list3 = shift_temp(fil_lst3, a, value)
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        value = random.randint(10, 20)
        list1 = shift_temp(fil_lst, a, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = shift_temp(fil_lst2, a, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = shift_temp(fil_lst3, a, value)
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        list4 = shift_temp(fil_lst4, a, value)
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        value = random.randint(10, 20)
        list1 = shift_temp(fil_lst, a, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        value = random.randint(10, 20)
        list2 = shift_temp(fil_lst2, a, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        value = random.randint(10, 20)
        list3 = shift_temp(fil_lst3, a, value)
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        a = choose_dir()
        value = random.randint(10, 20)
        list4 = shift_temp(fil_lst4, a, value)
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)

        # Temperature bump
        # 1 random panel
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        k = random.randint(10, len(fil_lst)-17)
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list1 = bump_temp(fil_lst, a, k, n, value)
        list2 = str_to_float_list(telemetry_to_str_list(file2r, Telemetry_dir))
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 2 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        k = random.randint(10, len(fil_lst) - 17)
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list1 = bump_temp(fil_lst, a, k, n, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = bump_temp(fil_lst2, a, k, n, value)
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 2 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        k = random.randint(10, len(fil_lst) - 17)
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list1 = bump_temp(fil_lst, a, k, n, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list2 = bump_temp(fil_lst2, a, k, n, value)
        list3 = str_to_float_list(telemetry_to_str_list(file3r, Telemetry_dir))
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 3 random panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        k = random.randint(10, len(fil_lst) - 17)
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list1 = bump_temp(fil_lst, a, k, n, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = bump_temp(fil_lst2, a, k, n, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = bump_temp(fil_lst3, a, k, n, value)
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 3 random panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        k = random.randint(10, len(fil_lst) - 17)
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list1 = bump_temp(fil_lst, a, k, n, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list2 = bump_temp(fil_lst2, a, k, n, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list3 = bump_temp(fil_lst3, a, k, n, value)
        list4 = str_to_float_list(telemetry_to_str_list(file4r, Telemetry_dir))
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together same height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        k = random.randint(10, len(fil_lst) - 17)
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list1 = bump_temp(fil_lst, a, k, n, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        list2 = bump_temp(fil_lst2, a, k, n, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        list3 = bump_temp(fil_lst3, a, k, n, value)
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        list4 = bump_temp(fil_lst4, a, k, n, value)
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        # 4 panels together different height
        file1r, file2r, file3r, file4r = random_reorder([file1, file2, file3, file4])
        ind += 1
        fil_lst = telemetry_to_str_list(file1r, Telemetry_dir)
        fil_lst = str_to_float_list(fil_lst)
        a = choose_dir()
        k = random.randint(10, len(fil_lst) - 17)
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list1 = bump_temp(fil_lst, a, k, n, value)
        ######
        fil_lst2 = telemetry_to_str_list(file2r, Telemetry_dir)
        fil_lst2 = str_to_float_list(fil_lst2)
        a = choose_dir()
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list2 = bump_temp(fil_lst2, a, k, n, value)
        ######
        fil_lst3 = telemetry_to_str_list(file3r, Telemetry_dir)
        fil_lst3 = str_to_float_list(fil_lst3)
        a = choose_dir()
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list3 = bump_temp(fil_lst3, a, k, n, value)
        ######
        fil_lst4 = telemetry_to_str_list(file4r, Telemetry_dir)
        fil_lst4 = str_to_float_list(fil_lst4)
        a = choose_dir()
        n = random.randint(9, 17)
        value = random.randint(80, 120)
        list4 = bump_temp(fil_lst4, a, k, n, value)
        spike_file1 = list_to_telemetry_file(list1, file1r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file2 = list_to_telemetry_file(list2, file2r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file3 = list_to_telemetry_file(list3, file3r[:-4] + f'_a_{ind}.txt', Telemetry_dir)
        spike_file4 = list_to_telemetry_file(list4, file4r[:-4] + f'_a_{ind}.txt', Telemetry_dir)

        ############## FOR A SINGLE PANEL ########################################################
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

if make_tel:
    make_telemetry_files_with_anomalies(ind)



'''************   FUNCTION TO MAKE A TIME SERIES LIST FOR AN INPUT TELEMETRY DATA LIST  ************'''
def time_series_from_telemetry(telemetry_list): #INPUT LIST IS ANY TYPE
    t_lst = [float(l) for l in telemetry_list]
    c_list = [0.0 for t in t_lst]

    #find where T0 is (where satellite leaves the shadow and starts heating up)
    lowest_value_index = t_lst.index(min(t_lst))

    #measure orbital period
    T_orb = 98 #min, int

    #Extrapolate time into the future until the end of the list
    current_ref_point = lowest_value_index
    while int(round(len(c_list)-current_ref_point)) > T_orb:
        for i in range(1, T_orb):
            c_list[current_ref_point+i] = float(i)
        current_ref_point += T_orb
    if int(round(len(c_list) - current_ref_point)) > 2:
        for i in range(1, int(round(len(c_list) - current_ref_point))):
            c_list[current_ref_point + i] = float(i)
    elif int(round(len(c_list) - current_ref_point)) == 2:
        c_list[current_ref_point + 1] = 1.0

    # Extrapolate time into the past until the beginning of the list
    current_ref_point = lowest_value_index
    while current_ref_point > T_orb:
        for i in range(1, T_orb):
            c_list[current_ref_point - i] = T_orb - float(i)
        current_ref_point -= T_orb
    if current_ref_point > 1:
        for i in range(1, current_ref_point + 1):
            c_list[current_ref_point - i] = T_orb - float(i)
    elif current_ref_point == 1:
        c_list[0] = T_orb - 1.0

    return c_list

'''************   FUNCTION TO MAKE UNPERTURBED TIME SERIES FOR EACH TELEMETRY PART  ************'''
def make_time_series(Telemetry_dir, time_dir):
    t_parts = ['44', '163', '286', '529', '775', '1042', '1187']
    ref_panel = '+Y'
    for t_part in t_parts:
        for filename in os.listdir(Telemetry_dir):
            if (ref_panel in filename) and (t_part in filename) and (not 'a' in filename):
                telemetry_file = filename
        values = telemetry_to_str_list(telemetry_file, Telemetry_dir)
        time_series = time_series_from_telemetry(values)
        time_file = list_to_telemetry_file(time_series, f'clock_{t_part}.txt', time_dir)

if make_time:
    make_time_series(Telemetry_dir, Time_dir)

'''************   FUNCTION TO MAKE INDIVIDUAL DATASETS FROM INDIVIDUAL TELEMETRY PARTS  ************'''
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
        file4 = ''  # -Y
        for fi in matching_files:
            if '+X' in fi:
                file1 = fi
        for fi in matching_files:
            if '-X' in fi:
                file2 = fi
        for fi in matching_files:
            if '+Y' in fi:
                file3 = fi
        for fi in matching_files:
            if '-Y' in fi:
                file4 = fi

        # make ANOMALY-FREE datasets
        ind = 0
        filet = f'clock_{t_part}.txt'
        filenames = [file1, file2, file3, file4, filet]
        telemetry_files_to_dataset(N_series, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

        # make datasets WITH ANOMALIES
        if single_panel:
            for i in range(n_anomaly_files):
                ind += 1
                file1_a = file1[:-4] + f'_a_{ind}.txt'
                filenames = [file1_a, file2, file3, file4, filet]
                telemetry_files_to_dataset(N_series, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)
        else:
            for i in range(n_anomaly_files):
                ind += 1
                file1_a = file1[:-4] + f'_a_{ind}.txt'
                file2_a = file2[:-4] + f'_a_{ind}.txt'
                file3_a = file3[:-4] + f'_a_{ind}.txt'
                file4_a = file4[:-4] + f'_a_{ind}.txt'
                filenames = [file1_a, file2_a, file3_a, file4_a, filet]
                telemetry_files_to_dataset(N_series, filenames, f'dataset_{t_part}_{ind}', Dataset_dir, normal_min, normal_max)

if make_sets:
    make_datasets(normal_min, normal_max)


'''************   FUNCTION TO COMBINE ALL DATASETS INTO ONE TRAINING DATASET  ************'''
def produce_dataset(training_dataset_name):
    os.chdir(Output_dir)
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

if produce:
    produce_dataset(training_dataset_name)


#test_anomaly_functions = True

if test_anomaly_functions:
    for telemetry_file_name in os.listdir(Telemetry_dir):
        for i in range(5):
            if (telemetry_file_name == 'output_+Y_1187.txt'): # main_panel in telemetry_file_name and (telemetry_file_name == f'output_+X_163_a_{21+i}.txt'):
                list1 = telemetry_to_str_list(telemetry_file_name, Telemetry_dir)
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
                list1 = remove_anomaly_labels(list1)
                list1 = str_to_float_list(list1)

                time = telemetry_to_str_list('clock_1187.txt', Time_dir)
                time = str_to_float_list(time)

                plt.title(f'+Y panel temperature starting 04/02/2016 19:44')
                plt.plot(range(len(time)), list1, label='Modified', c="b")

                # Set the x-axis tick locations and labels
                plt.xticks(range(len(time)), [int(t) for t in time])
                plt.locator_params(axis='x', nbins=20)

                plt.xlabel('time [min after leaving Earth\'s shadow]')#, fontsize=15)
                plt.ylabel('Temperature [deg C]')
                plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
                plt.minorticks_on()
                plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
                #plt.legend()
                plt.show()



def balance_dataset(dataset_name, dataset_dir):
    unique_lines = set()
    os.chdir(dataset_dir)
    out_dataset = dataset_name[:-4] + '_b.txt'
    with open(dataset_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line not in unique_lines:
                unique_lines.add(line)

    with open(out_dataset, 'w') as file:
        for line in unique_lines:
            file.write(line + '\n')


if balance:
    balance_dataset(training_dataset_name, Output_dir)

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