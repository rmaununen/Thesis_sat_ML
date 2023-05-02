import os
Working_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1'
Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/3_Anomaly_detect_mod_1/Dataset'
main_panel = '+X'

def make_const_sensor_anomaly(list, k, n, value=None):
    # k is the starting index where the constant values should begin
    # n is the number of elements to make constant
    if value != None:
        constant_value = value
    else:
        constant_value = list[k]
    # Update the list to make the elements constant
    list[k:k + n] = [constant_value] * n


def shift_temp(list, dir, magniude):
    list_out = []
    if dir == 1:
        for v in list:
            list_out.append(v+magniude)
    else:
        for v in list:
            list_out.append(v-magniude)
    return list_out


def list_to_file(list, file):
    with open(file, 'w') as f:
        for val in list:
            f.write(str(val) + '\n')


def make_series(N, file_name):
    # Create a new file for the concatenated sequences
    with open("new_dataset_{}.txt".format(N), "w") as output_file:
        # Read the values from the output file into a list
        values = []
        with open(file_name, "r") as f:
            for line in f:
                values.append(float(line.strip()))
        for i in range(len(values) - N):
            sequence = values[i:i + N]
            output_file.write(" ".join(str(v) for v in sequence) + "\n")

'''
lengths = [[44, 103], [163, 103], [286, 207], [529, 207], [775, 206], [1042, 103], [1187, 208]]
os.chdir(Dataset_dir)
for l in lengths:
    with open(f'output_time_{l[0]}.txt', "w") as f:
        for i in range(l[1]):
            f.write(str(i+1) + '\n')
'''


os.chdir(Working_dir)
for output_file_name in os.listdir(Dataset_dir):
    if main_panel in output_file_name:
        break

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