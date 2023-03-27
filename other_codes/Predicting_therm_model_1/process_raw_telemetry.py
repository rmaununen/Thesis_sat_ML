import os

# Define the filename of the input file
input_file = "Black_chassis_raw.txt"
short_id = 'bc'

out_id = 1

# Define the minimum number of consecutive identical values to be considered an invalid region
min_consecutive_values = 5

# Initialize variables for tracking the current value and the number of consecutive identical values
current_value = None
num_consecutive_values = 0

# Initialize a variable for tracking the current output file
current_output_file = None

# Open the input file for reading
with open(input_file, "r") as f:
    # Read the first line
    line = f.readline()
    # Loop over the remaining lines
    while line:
        # Convert the line to a float value
        value = float(line.strip())
        # Check if this value is different from the previous value
        if value != current_value:
            # Update the current value and reset the number of consecutive identical values
            current_value = value
            num_consecutive_values = 1
        else:
            # Increment the number of consecutive identical values
            num_consecutive_values += 1
        # Check if the current region of identical values is too long
        if num_consecutive_values >= min_consecutive_values:
            # If we're not already in an invalid region, create a new output file
            if current_output_file is None:
                current_output_file = open("output_" + short_id + f"_{out_id}.txt", "w")
            # Write the value to the output file
            current_output_file.write(str(value) + "\n")
            out_id += 1
            # Read the next line
            line = f.readline()
            # Reset the number of consecutive identical values
            num_consecutive_values = 0

            # Close the current output file
            current_output_file.close()
            current_output_file = None
        else:
            # If we're not already in a valid region, create a new output file
            if current_output_file is None:
                current_output_file = open("output_" + short_id + f"_{out_id}.txt", "w")
            # Write the value to the output file
            current_output_file.write(str(value) + "\n")
            out_id += 1
            # Read the next line
            line = f.readline()

# Close the current output file, if it is open
if current_output_file is not None:
    current_output_file.close()


# Define the filename prefix of the output files
output_file_prefix = "output_"

# Iterate over all output files with the specified prefix
for output_file_name in os.listdir():
    if output_file_name.startswith(output_file_prefix):
        # Read the values from the output file into a list
        values = []
        with open(output_file_name, "r") as f:
            for line in f:
                values.append(float(line.strip()))
        # Check if the list ends with several identical values
        num_identical_values_end = 0
        for i in range(len(values)-1, 0, -1):
            if values[i] == values[i-1]:
                num_identical_values_end += 1
            else:
                break
        # Check if the list starts with several identical values
        num_identical_values_start = 0
        for i in range(len(values)-1):
            if values[i] == values[i+1]:
                num_identical_values_start += 1
            else:
                break
        # If there are several identical values at the beginning or end of the list, remove them
        if num_identical_values_start > 0 or num_identical_values_end > 0:
            values = values[(num_identical_values_start+1):len(values)-(num_identical_values_end+1)]
            # Rewrite the output file with the updated values
            with open(output_file_name, "w") as f:
                for value in values:
                    f.write(str(value) + "\n")


# Define the minimum number of valid values required to keep an output file
min_valid_values = 31

# Iterate over all output files with the specified prefix
for output_file_name in os.listdir():
    if output_file_name.startswith(output_file_prefix):
        # Count the number of valid values in the output file
        num_valid_values = 0
        with open(output_file_name, "r") as f:
            for line in f:
                num_valid_values += 1
        # If the number of valid values is less than the threshold, delete the output file
        if num_valid_values < min_valid_values:
            os.remove(output_file_name)
            print(f"Deleted file {output_file_name} because it had only {num_valid_values} valid values")
