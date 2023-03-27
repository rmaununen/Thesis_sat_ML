import numpy as np
a = np.array([[0, 0, 1, 0], [1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 1, 0]])
c = np.array([[0, 0, 1, 0], [1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0]])
b = [[0, 0, 1], [1, 0, 0], [1, 1, 0], [0, 1, 1]]
d = [0, 1, 1, 0]
print(np.shape(a))
print(np.shape(c))
print(np.shape(b))
print(np.shape(d))


def read_ptm_dataset(N):
    x_rows = []
    y_rows = []
    with open("dataset_{}.txt".format(N), "r") as f:
        for line in f:
            # Split the line into values
            values = line.strip().split()
            if len(values) == N + 1:
                # Extract the input and output values
                x = [float(v) for v in values[:-1]]
                y = [float(values[-1])]
                x_rows.append(x)
                y_rows.append(y)
            else:
                print('Warning: length of a row is not', N+1, '. Counted is', len(values))

    return x_rows, y_rows
x_rows, y_rows = read_ptm_dataset(30)
print('x_rows', np.shape(x_rows), 'y rows:', np.shape(y_rows))
print(x_rows[-1])
print(y_rows[-1])