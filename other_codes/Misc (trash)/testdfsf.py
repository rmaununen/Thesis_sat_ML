import tkinter as tk
import numpy as np

# Define the MLP network architecture (in this example, 3 input neurons, 4 hidden neurons, and 2 output neurons)
input_size = 3
hidden_size = 4
output_size = 2

# Define the weights and biases for each layer
W1 = np.random.randn(input_size, hidden_size)
b1 = np.random.randn(hidden_size)
W2 = np.random.randn(hidden_size, output_size)
b2 = np.random.randn(output_size)

# Create a Tkinter window
window = tk.Tk()

# Define the canvas size and create a canvas object
canvas_width = 500
canvas_height = 300
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
canvas.pack()

# Define the size of the circles and lines
circle_radius = 20
line_width = 2

# Create the circles for the input neurons
x_start = 50
y_start = 100
circles_input = []
for i in range(input_size):
    x = x_start + i * 50
    y = y_start
    circle = canvas.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, fill="blue")
    circles_input.append(circle)

# Create the circles for the hidden neurons
x_start = 200
y_start = 50
circles_hidden = []
for i in range(hidden_size):
    x = x_start + i * 50
    y = y_start
    circle = canvas.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, fill="green")
    circles_hidden.append(circle)

# Create the circles for the output neurons
x_start = 350
y_start = 100
circles_output = []
for i in range(output_size):
    x = x_start + i * 50
    y = y_start
    circle = canvas.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, fill="red")
    circles_output.append(circle)

# Create the lines and text for the connections between input and hidden neurons
lines_input_hidden = []
text_input_hidden = []
for i in range(input_size):
    for j in range(hidden_size):
        x1 = canvas.coords(circles_input[i])[2]
        y1 = canvas.coords(circles_input[i])[3]
        x2 = canvas.coords(circles_hidden[j])[0]
        y2 = canvas.coords(circles_hidden[j])[1]
        line = canvas.create_line(x1, y1, x2, y2, width=line_width)
        weight = round(W1[i][j], 2)
        text = canvas.create_text((x1+x2)/2, (y1+y2)/2-line_width, text=str(weight))
        lines_input_hidden.append(line)
        text_input_hidden.append(text)

# Create the lines and text for the connections between hidden and output neurons
lines_hidden_output = []
text_hidden_output = []
for i in range(hidden_size):
    for j in range(output_size):
        x1 = canvas.coords(circles_hidden[i])[2]
        y1 = canvas.coords(circles_hidden[i])[3]
        x2 = canvas.coords(circles_output[j])[0]
        y2 = canvas.coords(circles_output[j])[1]
        line = canvas.create_line(x1, y1, x2, y2, width=line_width)
        weight = round(W2[i][j], 2)
        text = canvas.create_text((x1+x2)/2, (y1+y2)/2-line_width, text=str(weight))
        lines_hidden_output.append(line)
        text_hidden_output.append(text)

text_bias_input = []
for i in range(input_size):
    x = canvas.coords(circles_input[i])[0]
    y = canvas.coords(circles_input[i])[1] - 20
    text = canvas.create_text(x, y, text="b" + str(i+1) + "=" + str(round(b1[i], 2)))
    text_bias_input.append(text)

text_bias_hidden = []
for i in range(hidden_size):
    x = canvas.coords(circles_hidden[i])[0]
    y = canvas.coords(circles_hidden[i])[1] - 20
    text = canvas.create_text(x, y, text="b" + str(i+1) + "=" + str(round(b2[0], 2)))
    text_bias_hidden.append(text)

text_bias_output = []
for i in range(output_size):
    x = canvas.coords(circles_output[i])[0]
    y = canvas.coords(circles_output[i])[1] - 20
    text = canvas.create_text(x, y, text="b" + str(i+1) + "=" + str(round(b2[i], 2)))
    text_bias_output.append(text)

window.mainloop()