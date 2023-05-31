import numpy as np

Dataset_file = 'training_dataset_1_2_n.txt'
out_dataset = 'training_dataset_1_2_n_d.txt'

def add_derivative(Dataset_file, out_dataset):
    # Open the file in write mode and truncate its content
    with open(out_dataset, "w") as file:
        file.truncate(0)
    print("Output file contents have been cleared\n")

    print("Adding derivative for sensor 1\n")
    with open(Dataset_file, 'r') as f:
        with open(out_dataset, 'w') as out_f:
            for line in f:
                values = line.strip().split()
                output_values = []
                values_float = [float(v) for v in values]
                slope_inp = [values_float[19], values_float[20], values_float[21]]
                der = np.gradient(slope_inp, 0.3)[-1]
                slope_val = min(1.0, abs(der))
                output_values.append(str(round(abs(slope_val), 4)) + ' ')
                for v in values_float:
                    output_values.append(str(v) + ' ')
                output_values.append('\n')
                out_f.writelines(output_values)
                output_values = []
    print("Output file with derivatives has been made")

add_derivative(Dataset_file, out_dataset)