import numpy as np
import matplotlib.pyplot as plt
import random
import os
os.chdir('/other_codes/1_Simple_therm_model_1')
#from random import randrange

# Set variations
n1 = 1 #randrange(90, 110)/100
n2 = 1 #randrange(90, 110)/100
n3 = 1 #randrange(90, 110)/100
n4 = 1 #randrange(90, 110)/100
n5 = 1 #randrange(90, 110)/100
n6 = 1 #randrange(95, 105)/100
n7 = 1 #randrange(95, 105)/100
n8 = 1 #randrange(95, 105)/100
n9 = 1 #randrange(95, 105)/100
n10 = 1 #randrange(95, 105)/100
c = 7 #randrange(680, 720)/100

# Define x values
nsamples = 5000
x = np.linspace(0, 2*np.pi, nsamples)

# Define y values for the growing exponential line
y1 = -10*n5 + c*(6*n4 - np.exp(-1*n3 * (n1*0.9*x-(1.79*n2))))
# Define y values for the decaying exponential line
y2 = -10*n10 + c * (-1*n9 + np.exp(-0.6*n8 * (x*n7 - 2*np.pi*n6)))
# Combine the two lines into one
y3 = np.concatenate((y1[:int(nsamples/2)], y2[-int(nsamples/2):]))

x_values = []
y_values = []
var = 2.8 * np.random.randn(x.shape[0])
ind = 0

for i, j in zip(x, y3):
    x_values.append(i)
    y_values.append(j+var[ind])
    ind+=1

#Shuffle
# Combine x and y into a list of tuples
xy_pairs = list(zip(x_values, y_values))
# Shuffle the list of tuples
random.shuffle(xy_pairs)
# Separate the tuples back into two lists
x_values, y_values = zip(*xy_pairs)

# Plot
plt.scatter(x_values, y_values, c='r', s=1, label='Growing')
plt.xlim([0, 2*np.pi])
plt.ylim([-11, 58])
plt.xlabel('theta rad')
plt.ylabel('temp deg C')
plt.title('S/C Temp')
plt.legend()
plt.show()

#Save data
def write_lists_to_txt(list1, list2, filename):
    with open(filename, 'w') as f:
        for item1, item2 in zip(list1, list2):
            f.write(f'{item1}\t{item2}\n')
write_lists_to_txt(x_values, y_values, 'mod1_data.txt')
write_lists_to_txt(x, y3, 'mod1_actual.txt')