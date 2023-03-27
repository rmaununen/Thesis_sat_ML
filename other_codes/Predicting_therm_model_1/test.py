import numpy as np
a = np.array([[0, 0, 1, 0], [1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 1, 0]])
c = np.array([[0, 0, 1, 0], [1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0]])
b = [[0, 0, 1], [1, 0, 0], [1, 1, 0], [0, 1, 1]]
d = [0, 1, 1, 0]
print(np.shape(a))
print(np.shape(c))
print(np.shape(b))
print(np.shape(d))


my_list = [1.0, 2.5, 3.2, 4.8, 5.1, 6.7, 7.2, 8.9, 9.0, 10.5]

# Starting index where the constant values should begin
k = 3

# Number of elements to make constant
N = 4

# Value to assign to the constant elements
constant_value = my_list[k]

# Update the list to make the elements constant
my_list[k:k+N] = [constant_value] * N

print(my_list)