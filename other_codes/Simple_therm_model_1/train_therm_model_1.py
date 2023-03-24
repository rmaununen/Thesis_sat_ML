import os
import math
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers
os.chdir('/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/other_codes/Simple_therm_model_1')

plot_ds = True

def read_lists_from_txt(filename):
    list1 = []
    list2 = []
    with open(filename, 'r') as f:
        for line in f:
            item1, item2 = line.strip().split('\t')
            list1.append(float(item1))
            list2.append(float(item2))
    return list1, list2
x_values, y_values = read_lists_from_txt('mod1_data.txt')
x_values = np.array(x_values)
y_values = np.array(y_values)

if plot_ds:
    # Plot
    plt.scatter(x_values, y_values, c='r', s=1, label='Growing')
    plt.xlim([0, 2*np.pi])
    plt.ylim([-11, 58])
    plt.xlabel('theta rad')
    plt.ylabel('temp deg C')
    plt.title('S/C Temp')
    plt.legend()
    plt.show()

# Print versions
print('Numpy ' + np.__version__)
print('TensorFlow ' + tf.__version__)
print('Keras ' + tf.keras.__version__)

# Settings
nsamples = 5000     # Number of samples to use as a dataset
val_ratio = 0.2     # Fraction of samples that should be held for validation set
test_ratio = 0.2    # Fraction of samples that should be held for test set
tflite_model_name = 'therm_model_1'  # Will be given .tflite suffix
c_model_name = 'therm_model_1'       # Will be given .h suffi

# Split the dataset into training, validation, and test sets
val_split = int(val_ratio * nsamples)
test_split = int(val_split + (test_ratio * nsamples))
x_val, x_test, x_train = np.split(x_values, [val_split, test_split])
y_val, y_test, y_train = np.split(y_values, [val_split, test_split])

# Check that our splits add up correctly
assert(x_train.size + x_val.size + x_test.size) == nsamples

if plot_ds:
    # Plot the data in each partition in different colors:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x_train, y_train, 'b.', label="Train")
    plt.plot(x_test, y_test, 'r.', label="Test")
    plt.plot(x_val, y_val, 'y.', label="Validate")
    plt.legend()
    plt.show()

# Create a model
model = tf.keras.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(1,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1))
# View model
model.summary()

# Add optimizer, loss function, and metrics to model and compile it
model.compile(optimizer='rmsprop', loss='mae', metrics=['mae'])
# Train model
history = model.fit(x_train,
                    y_train,
                    epochs=1200,
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

predictions = model.predict(x_test)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.clf()
plt.title("Comparison of predictions to actual values")
plt.plot(x_test, y_test, 'b.', label='Actual')
plt.plot(x_test, predictions, 'r.', label='Prediction')
plt.legend()
plt.show()

#SAVE MODEL
model.save(tflite_model_name+'.h5')