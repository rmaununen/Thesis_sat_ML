import matplotlib.pyplot as plt

clk = []
with open('clock_1187.txt', "r") as f:
    for line in f:
        clk.append(float(line.strip()))

tea = []
with open('TEA_output_1187.txt', "r") as f:
    for line in f:
        tea.append(float(line.strip()))

fig = plt.figure()
ax = fig.add_subplot(111)
plt.clf()
plt.title(f'Time stamps produced by Python algorithm vs C++ TEA')
plt.plot(clk, 'b', linewidth=3, label='Python algorithm')
plt.plot(tea, 'r', label='C++ TEA')
# for time:
plt.legend()
plt.xlabel('Data point number')
plt.ylabel('Estimated time [min]')
plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
plt.minorticks_on()
plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
plt.show()