filename = 'terminal.txt'

x_values = []
y_values = []

with open(filename) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        x, y = line.split(',')
        x_multiplier, x_exponent = x.strip().split(':')[1].strip().split('*')
        x_value = float(x_multiplier) * pow(2, float(x_exponent.split('^')[1]))
        y_multiplier, y_exponent = y.strip().split(':')[1].strip().split('*')
        y_value = float(y_multiplier) * pow(2, float(y_exponent.split('^')[1]))
        x_values.append(x_value)
        y_values.append(y_value)

print("\nX-values:\n")
for x_val in x_values:
    print(str(x_val).replace('.', ','))

print("\nY-values:\n")
for y_val in y_values:
    print(str(y_val).replace('.', ','))