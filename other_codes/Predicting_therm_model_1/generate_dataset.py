import os

# Set the value of N
N = 30

# Create a new file for the concatenated sequences
with open("new_dataset_{}.txt".format(N), "w") as output_file:
    # Iterate over the output files in the "output_files" directory
    for output_file_name in os.listdir("telemetry_FUNCUBE"):
        if output_file_name.startswith("output_"):# and (output_file_name == "output_bp_286.txt"):
            # Read the values from the output file into a list
            values = []
            with open(os.path.join("telemetry_FUNCUBE", output_file_name), "r") as f:
                #a_var = 1
                for line in f:
                    #if a_var%2==0:
                    values.append(float(line.strip()))
                    #a_var+=1
            #introducing anomalies
            # Starting index where the constant values should begin
            k = 60#118
            # Number of elements to make constant
            n = 24
            # Value to assign to the constant elements
            constant_value = values[k]
            # Update the list to make the elements constant
            values[k:k + n] = [constant_value] * n
            # Write each sequence of N+1 consecutive values into the output file
            for i in range(len(values) - N):
                sequence = values[i:i+N+1]
                output_file.write(" ".join(str(v) for v in sequence) + "\n")
