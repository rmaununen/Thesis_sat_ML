import os
import sys
import math
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes')
from other_codes.tfl_converter_tools import *
sys.path.append('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/4_0_Produce_dataset')
#from dataset_functions import *

Dataset_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/Dataset'
Working_dir = '/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/4_Anomaly_detect_mod_2/4_1_Train model'

training_dataset = 'training_dataset_2_9_b.txt'

# Print versions
print('Numpy ' + np.__version__)
print('TensorFlow ' + tf.__version__)
print('Keras ' + tf.keras.__version__)

# Settings
#plot_ds = True
nsamples = 10718     # Number of samples to use as a dataset
val_ratio = 0.3     # Fraction of samples that should be held for validation set
model_name = 'adm_2_9_b'  # Will be given .h5 suffix
N_i = 85 # number of input neurons
H1 = 32 # number of neurons on the hidden layers
H2 = 32 # number of neurons on the hidden layers
H3 = 32 # number of neurons on the hidden layers
N_o = 8 # number of output neurons
nepochs = 400
sbatch = 100
normal_min, normal_max = -40, 50

#Get dataset
os.chdir(Working_dir)
x_values, y_values = read_ptm_dataset(N_i, N_o, training_dataset)
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
    tf.keras.layers.Dense(N_o)#, activation='relu')
])
# View model
model.summary()

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01), loss='mae', metrics=['mae'])

# 4_1_Train model
history = model.fit(x_train,
                    y_train,
                    epochs=nepochs,
                    batch_size=sbatch,
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



#SAVE MODEL
os.chdir(Working_dir)
model.save(model_name+'.h5')

''' *******************   TESTING   ********************** '''
x_test_rows = []
y_test_rows = []
os.chdir(Dataset_dir)
with open("dataset_1187_1.txt", "r") as f:
    for line in f:
        # Split the line into values
        values_nn = line.strip().split()
        values = values_nn #normalize_list(values_nn, normal_min, normal_max, already_normalised_indx)
        if len(values) == N_i + N_o:
            # Extract the input and output values
            x = [float(v) for v in values[N_o:]]
            y = [float(v) for v in values[0:N_o]]
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
plt.title("Comparison of predictions to actual values output 1")
plt.plot(x_time, np.array(y_test_rows)[:, 1+1], 'b', label='Actual values')
plt.plot(x_time, predictions[:, 1], 'r', label='Model predictions')
plt.legend()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.clf()
plt.title("Comparison of predictions to actual values output 2")
plt.plot(x_time, np.array(y_test_rows)[:, 0], 'b', label='Actual values')
plt.plot(x_time, denormalise_array(predictions[:, 0+1], normal_min, normal_max, None), 'r', label='Model predictions')
plt.legend()
plt.show()