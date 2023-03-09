import numpy as np
import matplotlib.pyplot as plt

# Define variables

c = 7


# Define x values
x = np.linspace(0, 2*np.pi, 1000)

# Define y values for the growing exponential line
y1 = -10 + c*(6 - np.exp(-1 * (0.9*x-1.79)))

# Define y values for the decaying exponential line

y2 = -10 + c * (-1 + np.exp(-0.6 * (x - 2*np.pi)))

y3 = np.concatenate((y1[:500], y2[-500:]))
# Combine the two lines into one plot
plt.plot(x, y3, 'r-', label='Growing')
#plt.plot(x, y2, 'b-', label='Decaying')

# Set the plot limits and labels
plt.xlim([0, 2*np.pi])
plt.ylim([-11, 33])
plt.xlabel('theta rad')
plt.ylabel('temp deg C')
plt.title('S/C Temp')

# Add a legend and show the plot
plt.legend()
plt.show()
