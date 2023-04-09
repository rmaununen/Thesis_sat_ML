#Receive
from matplotlib import pyplot
import serial
import time
import struct
#1410 or 1420

#/dev/cu.usbserial-1420
#/dev/cu.usbmodemM43210051
serialcom = serial.Serial('/dev/cu.usbmodemM43210051', baudrate=115200, timeout=1) #Change port name to the one you are using

while True:
    # Request user input string
    user_input = input("Enter a string to send over serial: ")
    # Initialize variables for reading serial
    user_input += '\n'
    received_lines = []
    time_init = time.time()

    # Send user input string over serial
    serialcom.write(user_input.encode())
    # Read lines from serial for 5 seconds after sending user input string
    while (time.time() - time_init) <= 0.1:
        # Read line from serial (if there is anything to read)
        line = serialcom.readline().decode().rstrip()
        print(line)

# Close serial port
serialcom.close()
print('Done')

'''
receiving = True
time.sleep(2)
received_data = []
#serialcom.write("1\n".encode())
time_init = time.time()
print('start time: ', time_init)
while receiving:
    #bytesToRead = serialcom.inWaiting()
    #data = serialcom.read(bytesToRead).decode('ascii')#[:-2]
    data = serialcom.readline()
    print(data)
    #if not data == '':
    #    received_data.append(data)
    time.sleep(0.01) #must be faster than the board
    time_cur = time.time()
    if (time_cur - time_init) >= 5:
        receiving = False
    #    serialcom.write("0\n".encode())
        time.sleep(0.4)
        print('end time: ', time_cur)

#bytesToRead = serialcom.inWaiting()
#data = serialcom.read(bytesToRead)#.decode('ascii')#[:-2]
data = serialcom.readline()
serialcom.close()
print(data)
'''

'''
received_data.append(data[0])
received_data.append(data[1])
print(data[2])
print(data[3])
'''

#print('\n', received_data)
#print('length of the received array: ', len(received_data))