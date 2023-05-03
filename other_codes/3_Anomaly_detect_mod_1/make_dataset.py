import os
import matplotlib.pyplot as plt
Working_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1'
Telemetry_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/Telemetry'
Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/Dataset'
main_panel = '+X'

'''*********************   FUNCTIONS TO MAKE ANOMALIES   **************************'''
def make_const_sensor_anomaly(list, k, n, value=None):
    # k is the starting index where the constant values should begin
    # n is the number of elements to make constant
    if value != None:
        constant_value = value
    else:
        constant_value = list[k]
    # Update the list to make the elements constant
    list1 = []
    for l in list:
        list1.append(str(l))
    list1[k:k + n] = [str(constant_value) + 'a'] * n
    return list1


def shift_temp(list, dir, magnitude):
    list_out = []
    if dir == 1: #dir 1 i up, 0 is down
        for v in list:
            list_out.append(v+magnitude)
    else:
        for v in list:
            list_out.append(v-magnitude)
    return list_out


def bump_temp(lst, dir, k, n, peak_magn):
    # Define the bell-shaped bump as a Gaussian distribution
    bump = [peak_magn * (1 / (n * 0.4 * (2 * 3.1415) ** 0.5)) * 2.71828 ** (-(i - n / 2) ** 2 / (2 * (n * 0.4) ** 2))
            for i in range(n)]
    # Modify the values in the list starting at index k
    for i in range(k, min(k + n, len(lst))):
        if dir == 1:
            lst[i] += bump[i - k]
        else:
            lst[i] -= bump[i - k]
    return lst

def corrupt_clock(list, factor):
    list_out = []
    for l in list:
        list_out.append(factor*l)
    return list_out

'''***************************************************************************************'''

def file_to_list(file_name):
    os.chdir(Telemetry_dir)
    # Read the values from the file into a list
    values = []
    with open(file_name, "r") as f:
        for line in f:
            values.append(float(line.strip()))
    return values

def file_to_list_str(file_name):
    os.chdir(Telemetry_dir)
    # Read the values from the file into a list
    values = []
    with open(file_name, "r") as f:
        for line in f:
            values.append(line.strip())
    return values

def list_to_file(list, file):
    os.chdir(Telemetry_dir)
    with open(file, 'w') as f:
        for val in list:
            f.write(str(val) + '\n')
    return file


def make_series(N, filenames, out_file_name):
    filename_1, filename_2, filename_3 = filenames[0], filenames[1], filenames[2]
    # Create a new file for the concatenated sequences
    os.chdir(Dataset_dir)
    with open(out_file_name, "w") as output_file:
        # Read the values from the file into a list
        values1 = file_to_list_str(filename_1)
        values2 = file_to_list(filename_2)
        values3 = file_to_list(filename_3)
        os.chdir(Working_dir)
        for i in range(len(values1) - N):
            sequence1 = values1[i:i + N]
            sequence11 = []
            if 'a' in sequence1[-1]:
                sequence0 = [1.0]
            else:
                sequence0 = [0.0]
            for s in sequence1:
                x = s.replace('a', '')
                sequence11.append(x)
            sequence2 = values2[i:i + N]
            sequence3 = values3[i:i + N]
            sequence = sequence0 + sequence11 + sequence2 + sequence3
            output_file.write(" ".join(str(v) for v in sequence) + "\n")

def create_datasets():
    os.chdir(Telemetry_dir)
    steps = ['44', '163', '286', '529', '775', '1042', '1187']
    import fnmatch
    import random

    for filename in os.listdir(Telemetry_dir):
        if '_a_' in filename:
            os.remove(os.path.join(Telemetry_dir, filename))

    for step in steps:
        # Define the pattern to match against
        pattern = f'*{step}*'
        # Use the os module to get a list of all files in the directory
        all_files = os.listdir(Telemetry_dir)
        # Use the fnmatch module to filter the list of files based on the pattern
        matching_files = [filename for filename in all_files if fnmatch.fnmatch(filename, pattern)]
        file1 = '' #+X
        file2 = '' #-X
        file3 = '' #+Y
        for fi in matching_files:
            if '+X' in fi:
                file1 = fi
        for fi in matching_files:
            if '-X' in fi:
                file2 = fi
        for fi in matching_files:
            if '+Y' in fi:
                file3 = fi
        ind = 0
        filenames = [file1, file2, file3]
        make_series(20, filenames, f'dataset_{step}_{ind}')
        for i in range(7): #spikes
            ind+=1
            fil_lst = file_to_list(file1)
            k = random.randint(20, len(fil_lst)-3)
            n = random.randint(1, 2)
            dir = random.randint(1, 2)
            if dir ==1:
                a = 1
            else:
                a = -1
            value = fil_lst[k] + a*random.randint(10, 30)
            list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
            spike_file = list_to_file(list1, file1[:-4]+f'_a_{ind}.txt')
            filenames = [spike_file, file2, file3]
            make_series(20, filenames, f'dataset_{step}_{ind}')
        for i in range(3): #None const
            ind+=1
            fil_lst = file_to_list(file1)
            n = random.randint(10, 30)
            k = random.randint(20, len(fil_lst)-n)
            list1 = make_const_sensor_anomaly(fil_lst, k, n, None)
            const_file = list_to_file(list1, file1[:-4]+f'_a_{ind}.txt')
            filenames = [const_file, file2, file3]
            make_series(20, filenames, f'dataset_{step}_{ind}')

        for i in range(3): #value const
            ind += 1
            fil_lst = file_to_list(file1)
            n = random.randint(10, 30)
            k = random.randint(20, len(fil_lst) - n)
            dir = random.randint(1, 2)
            if dir == 1:
                a = 1
            else:
                a = -1
            value = fil_lst[k] + a * random.randint(10, 30)
            list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
            const_file = list_to_file(list1, file1[:-4] + f'_a_{ind}.txt')
            filenames = [const_file, file2, file3]
            make_series(20, filenames, f'dataset_{step}_{ind}')
        for i in range(3): #value const
            ind += 1
            fil_lst = file_to_list(file1)
            k = random.randint(20, len(fil_lst)-30)
            n = len(fil_lst)-k
            dir = random.randint(1, 2)
            if dir == 1:
                a = 1
            else:
                a = -1
            value = fil_lst[k] + a * random.randint(10, 30)
            list1 = make_const_sensor_anomaly(fil_lst, k, n, round(value, 2))
            const_file = list_to_file(list1, file1[:-4] + f'_a_{ind}.txt')
            filenames = [const_file, file2, file3]
            make_series(20, filenames, f'dataset_{step}_{ind}')

#COMBINE DATASETS
def produce_dataset():
    # specify the output file path and name
    os.chdir(Working_dir)

    # open the output file in append mode
    with open('training_dataset.txt', 'a') as output_file:

        # loop through all files in the directory
        for filename in os.listdir(Dataset_dir):

            # get the full path of the file
            file_path = os.path.join(Dataset_dir, filename)

            # open the file in read mode
            with open(file_path, 'r') as input_file:

                # read all lines from the file
                lines = input_file.readlines()

                # write the lines to the output file
                output_file.writelines(lines)

create_datasets()
produce_dataset()
'''
    if main_panel in output_file_name and (output_file_name == 'output_+X_44.txt'):
            list = file_to_list(output_file_name)
            #list1 = make_const_sensor_anomaly(list, 30, len(list)-30, value=35)
            #list1 = shift_temp(list, -1, 10)
            #list1 = bump_temp(list, -1, 10, 10, 80)
            list1 = [i for i in range(len(list))]
            list1 = corrupt_clock(list1, 2)
            plt.plot(list1, list, label='Modified', c="g")
            plt.xlabel('faster time', fontsize=15)
            #y = [0 for i in range(len(list))]
            #plt.plot(list1, y, c="black")
            plt.legend()
            plt.show()
'''
'''
lengths = [[44, 103], [163, 103], [286, 207], [529, 207], [775, 206], [1042, 103], [1187, 208]]
os.chdir(Dataset_dir)
for l in lengths:
    with open(f'output_time_{l[0]}.txt', "w") as f:
        for i in range(l[1]):
            f.write(str(i+1) + '\n')
'''



'''
# TEST
lst = [0.5 + i * 0.5 for i in range(50)]
lst1 = [0.5 + i * 0.5 for i in range(50)]
lst20 = [0.5 for i in range(50)]
lst2 = [0.5 for i in range(50)]
# Apply the function to the list
new_lst = incr_temp(lst2, dir=1, k=20, n=20, peak_magn=50)

# Plot the original and modified lists
plt.plot(lst20, label='Original')
plt.plot(new_lst, label='Modified')
plt.legend()
plt.show()
'''

#get files
#
#
#
#
#
#
#testing data set: normal p1, normal p2, normal p3, normal time
#                  anomaly a-z p1, normal p2, normal p3, normal time

#training data set [20 p1 , 20 p2, 20 p3, 20 t, ANOMALY:0/1]