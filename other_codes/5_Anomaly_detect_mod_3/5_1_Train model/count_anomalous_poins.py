def is_anomalous_line(values):
    return any(val == 1.0 for val in values[:4])

def count_anomalous_lines(file_path):
    anomalous_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            try:
                values = [float(val) for val in line.strip().split()]
                if is_anomalous_line(values):
                    anomalous_count += 1
            except ValueError:
                # If there's any error converting the values to floats, skip the line
                continue

    return anomalous_count

print(count_anomalous_lines('training_dataset_3_0.txt'))