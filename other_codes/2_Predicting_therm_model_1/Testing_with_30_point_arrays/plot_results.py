import matplotlib.pyplot as plt
import numpy as np
y_act = [-4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41,  -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.41, -4.77, -5.47, -6.43, -7.03, -7.46, -8.23, -8.78, -9.33, -9.88, -10.27, -10.58, -11.2, -11.13, -10.08,
-10.56, -7.89, -6.33, -7.39, -5.68, -3.21, -4.7, -4.44, -0.74, -2.3, -3.12, 0.82, 0.41, -0.81, 1.97, 3.15, 1.68, 2.64,
4.95, 3.84, 3.99, 6.8, 7.52, 6.89, 8.43, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69,
11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 11.69, 23.96, 22.9, 20.16, 22.66,
23.09, 20, 20.19, 22.59, 19.68, 18.6, 21.1, 19.32, 17.24, 19.42, 18.6, 17.04, 15.44, 13.85, 12.48, 10.56, 8.64, 7.71,
6.15, 4.56, 3.75, 2.67, 01.04, 0.29, -0.5, -1.82, -2.59, -2.66, -3.96, -4.7, -4.82, -5.76, -6.62, -6.96, -7.6, -8.35,
-8.73, -9.24, -9.84, -10.27, -10.56, -11.18, -9.76, -9.98, -9.93, -6.14, -6.52, -7.22, -3.93]

y_pred = [-4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -4.9297108, -5.4067796, -5.8838488, -6.8379856, -7.4740772, -8.1101704, -8.5872384, -9.2233288, -9.7003968, -10.3364912, -10.8135592, -11.1316056, -11.4496496, -10.9725808,
-11.7676976, -10.8135592, -7.951146, -6.6789628, -7.633102, -6.2018944, -3.498504, -4.7706876, -4.6116644, -0.79511465, -2.3853438, -3.0214358, 0.63609165, 0.318045825, -1.1131602, 1.5902293,
3.1804586, 1.5902293, 2.7033898, 5.2477556, 3.975573, 3.975573, 6.2018944, 7.4740772, 6.5199416, 8.4282136, 11.4496496, 10.8135592, 11.2906272, 14.9481544, 13.6759712, 12.2447656, 11.608672,
12.0857432, 11.608672, 11.1316056, 11.608672, 12.2447656, 12.2447656, 11.7676976, 12.2447656, 11.7676976, 11.9267176, 12.2447656, 12.4037888, 12.2447656, 12.2447656, 12.0857432, 11.9267176, 12.0857432, 12.0857432,
11.608672, 16.8564272, 17.651544, 27.1929248, 25.4436688, 19.8778624, 19.0827504, 21.9451616, 18.9237264, 15.7432696, 20.8320016, 18.2876384, 17.3334992, 19.8778624, 17.1744768, 15.584248, 18.4466576, 17.1744768,
14.3120632, 9.0643072, 7.1560316, 5.7248248, 3.975573, 3.1804586, 2.7033898, 1.1131602, -0.318045825, 0.1590229125, -0.477068875, -1.749252, -3.498504, -3.816551, -4.4526408, -5.2477556, -5.5658028, -6.2018944, -6.997008, -7.4740772,
-8.1101704, -8.9052816, -9.2233288, -9.5413752, -10.3364912, -10.8135592, -11.1316056, -11.4496496, -10.6545368, -10.3364912, -9.382352, -6.3609172, -6.8379856, -7.4740772, -3.3394814]
x_time = []
t = 0
for i in range(30):
    x_time.append(t)
for i in range(len(y_act)-30):
    x_time.append(t)
    t+=1

#print(len(y_act), len(y_pred), len(x_time))
show_animation = True
if show_animation:
    import matplotlib; matplotlib.use("TkAgg")
    from matplotlib import animation

    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 1.05*(len(x_time)-30)), ylim=(-15, 34))
    line, = ax.plot([], [], lw=1, label="Sensor readings")
    points = ax.scatter([], [], s=3)
    line2, = ax.plot([], [], lw=1, label="Predicted by NN")
    points2 = ax.scatter([], [], s=3)

    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        line.set_color("blue")
        points.set_offsets(np.column_stack([[], []]))
        points.set_color("blue")
        line2.set_data([], [])
        line2.set_color("red")
        points2.set_offsets(np.column_stack([[], []]))
        points2.set_color("red")
        return line, points, line2, points2

    xdata, ydata, ydata2 = [], [], []
    def animate(i):
        # x, y values to be plotted
        x = x_time[i]
        y = y_act[i]
        y2 = y_pred[i]
        # appending new points to x, y axes points list
        xdata.append(x)
        ydata.append(y)
        line.set_data(xdata, ydata)
        points.set_offsets(np.column_stack([xdata, ydata]))

        ydata2.append(y2)
        line2.set_data(xdata, ydata2)
        points2.set_offsets(np.column_stack([xdata, ydata2]))
        if i == 146:
            xdata.clear()
            ydata.clear()
            ydata2.clear()

        return line, points, line2, points2

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=147, interval=200, blit=True, repeat=True)
    #plt.title("this is title \n", fontsize=14)
    plt.legend(loc="upper right", fontsize=10)
    plt.xlabel('time [min]')
    plt.ylabel('T [deg C]')
    plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.3)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='grey', linestyle='-', alpha=0.1)
    # Get the figure manager
    plt.show()
    manager = plt.get_current_fig_manager()
    # Set the initial position of the window
    manager.window.setGeometry = (1450, 1450, 640, 480)