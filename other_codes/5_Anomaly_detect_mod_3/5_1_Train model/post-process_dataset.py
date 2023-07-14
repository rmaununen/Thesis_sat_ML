remove_columns = True

if remove_columns:
    # Open the input file
    with open('dataset_44_0_x3', 'r') as file: #training_dataset_3_0_12.txt
        lines = file.readlines()

    # Process each line in the file
    processed_lines = []
    for line in lines:
        # Split the line into columns
        columns = line.split()

        # Remove columns 3 to 7
        #processed_columns = columns[:4] + columns[8:]
        processed_columns = columns[:9] + columns[19+7:]

        # Join the columns back into a line
        processed_line = ' '.join(processed_columns) + '\n'

        # Add the processed line to the list
        processed_lines.append(processed_line)

    # Write the processed lines to a new file
    with open('dataset_44_0_x', 'w') as file:
        file.writelines(processed_lines)

