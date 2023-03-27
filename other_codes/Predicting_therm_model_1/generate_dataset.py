import os

# Set the value of N
N = 30

# Create a new file for the concatenated sequences
with open("dataset_{}.txt".format(N), "w") as output_file:
    # Iterate over the output files in the "output_files" directory
    for output_file_name in os.listdir("telemetry_FUNCUBE"):
        if output_file_name.startswith("output_"):# and (output_file_name == "output_bc_286.txt"):
            # Read the values from the output file into a list
            values = []
            with open(os.path.join("telemetry_FUNCUBE", output_file_name), "r") as f:
                for line in f:
                    values.append(float(line.strip()))
            # Write each sequence of N+1 consecutive values into the output file
            for i in range(len(values) - N):
                sequence = values[i:i+N+1]
                output_file.write(" ".join(str(v) for v in sequence) + "\n")
