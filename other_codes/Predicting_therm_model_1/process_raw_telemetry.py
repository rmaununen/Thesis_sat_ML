# Define the filename of the input file
input_file = "Black_chassis_raw.txt"

# Define the minimum number of consecutive identical values to be considered an invalid region
min_consecutive_values = 5

# Initialize variables for tracking the current value and the number of consecutive identical values
current_value = None
num_consecutive_values = 0

# Initialize a variable for tracking the current output file
current_output_file = None
last_valid_value = None
last_valid_line_num = 0

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
                current_output_file = open(f"output_{last_valid_value}.txt", "w")
                # Write the valid values to the output file
                with open(input_file, "r") as f2:
                    for i in range(last_valid_line_num):
                        f2.readline()
                    for j in range(i, i+num_consecutive_values):
                        f2.readline()
                    line = f2.readline()
                    while line and float(line.strip()) == last_valid_value:
                        line = f2.readline()
                    while line:
                        current_output_file.write(line)
                        line = f2.readline()
                current_output_file.close()
                current_output_file = None
            # Skip the invalid values
            line = f.readline()
            last_valid_line_num += num_consecutive_values
            num_consecutive_values = 0
        else:
            # If we're not already in a valid region, create a new output file
            if current_output_file is None:
                current_output_file = open(f"output_{value}.txt", "w")
                last_valid_value = value
                last_valid_line_num = 0
            # Write the value to the output file
            current_output_file.write(str(value) + "\n")
            # Read the next line
            line = f.readline()

# Close the current output file, if it is open
if current_output_file is not None:
    current_output_file.close()
