import os
import sys
import math
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
from other_codes.tfl_converter_tools import *

# Print versions
print('Numpy ' + np.__version__)
print('TensorFlow ' + tf.__version__)
print('Keras ' + tf.keras.__version__)

# Settings
plot_ds = True
nsamples = 7406     # Number of samples to use as a dataset
val_ratio = 0.3     # Fraction of samples that should be held for validation set
model_name = 'ptm_1'  # Will be given .tflite suffix
N_i = 30 # number of input neurons
H1 = 16 # number of neurons on the hidden layers
H2 = 16 # number of neurons on the hidden layers
H3 = 16 # number of neurons on the hidden layers
N_o = 1 # number of output neurons


#Get dataset
os.chdir('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Predicting_therm_model_1')
x_values, y_values = read_ptm_dataset(N_i)
print('x_rows', np.shape(x_values), 'y rows:', np.shape(y_values))

# Split the dataset into training, validation, and test sets
train_size = int((1-val_ratio) * nsamples)
#val_size = nsamples - train_size

x_train, y_train = x_values[:train_size], y_values[:train_size]
x_val, y_val = x_values[train_size:], y_values[train_size:]

# Printing the shapes of the two arrays
print("Shape of x_train:", x_train.shape)
print("Shape of x_val:", x_val.shape)
print("Shape of y_train:", y_train.shape)
print("Shape of y_val:", y_val.shape)

# Check that our splits add up correctly
assert(x_train.shape[0] + x_val.shape[0]) == nsamples

# Define the model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Dense(H1, activation='relu', input_shape=(N_i,)),
    tf.keras.layers.Dense(H2, activation='relu'),
    tf.keras.layers.Dense(H3, activation='relu'),
    tf.keras.layers.Dense(N_o)
])
# View model
model.summary()

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01), loss='mae', metrics=['mae'])

# Train model
history = model.fit(x_train,
                    y_train,
                    epochs=1000,
                    batch_size=100,
                    validation_data=(x_val, y_val))
# Plot the training history
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()

x_test_rows = []
y_test_rows = []
with open("1test_0.txt", "r") as f:
    for line in f:
        # Split the line into values
        values = line.strip().split()
        if len(values) == N_i + 1:
            # Extract the input and output values
            x = [float(v) for v in values[:-1]]
            y = float(values[-1])
            x_test_rows.append(x)
            y_test_rows.append(y)

predictions = model.predict(np.array(x_test_rows))
x_time = []
t = 0
for i in range(len(y_test_rows)):
    x_time.append(t)
    t+=1
fig = plt.figure()
ax = fig.add_subplot(111)
plt.clf()
plt.title("Comparison of predictions to actual values")
plt.plot(x_time, y_test_rows, 'b', label='Actual values')
plt.plot(x_time, predictions, 'r', label='Model predictions')
plt.legend()
plt.show()

#SAVE MODEL
model.save(model_name+'.h5')