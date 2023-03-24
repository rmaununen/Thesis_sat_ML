import numpy as np
import matplotlib.pyplot as plt
from random import randrange

# Define variables
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
x = np.linspace(0, 2*np.pi, 1000)

# Define y values for the growing exponential line
y1 = -10*n5 + c*(6*n4 - np.exp(-1*n3 * (n1*0.9*x-(1.79*n2))))

# Define y values for the decaying exponential line

y2 = -10*n10 + c * (-1*n9 + np.exp(-0.6*n8 * (x*n7 - 2*np.pi*n6)))

y3 = np.concatenate((y1[:500], y2[-500:]))
# Combine the two lines into one plot
plt.plot(x, y3, 'r-', label='Growing')
#plt.plot(x, y2, 'b-', label='Decaying')

# Set the plot limits and labels
plt.xlim([0, 2*np.pi])
plt.ylim([-11, 58])
plt.xlabel('theta rad')
plt.ylabel('temp deg C')
plt.title('S/C Temp')

# Add a legend and show the plot
plt.legend()
plt.show()
