#!/usr/bin/env python
import sys
import serial
import time
import scipy
import pylab

port = '/dev/ttyUSB0'
baudrate = 115200 
stream_dt = 0.001
ain2phys = 5.0/(2.0**10.0)

# Get input arguments
sample_t = float(sys.argv[1])
length = float(sys.argv[2])
output_file = sys.argv[3]

# Open serial connection to photogate device 
ser = serial.Serial(port,baudrate)
ser.open()

# Wait for device to reset
print 'waiting for device reset ... ',
sys.stdout.flush()
time.sleep(2.0)
print 'done'
time.sleep(0.5)

print 'acquiring data'
time.sleep(0.5)

# Empty any residual samples in serial buffer
ser.flush()

# Start streaming
ser.write('E')

# Read in data from device
cnt = 0
num_samples = scipy.floor(sample_t/stream_dt)
data = scipy.zeros((num_samples,))
t = scipy.arange(0.0,num_samples)*stream_dt

while cnt < num_samples:
    line = ser.readline()
    line = line.split()
    if line:
        value_list = [float(x) for x in line]
        for value in value_list:
            data[cnt] = ain2phys*value 
            print 't: %1.3f, v: %1.2f'%(t[cnt], data[cnt])
            cnt += 1

# Stop streaming
ser.write('D')
ser.flush()

# Write data to file
with open(output_file,'w') as fid:
    fid.write('%f\n'%(length,))
    for i in range(0,num_samples):
        fid.write('%f %f\n'%(t[i], data[i]))

# Plot data
pylab.plot(t, data)
pylab.xlabel('time (sec)')
pylab.ylabel('photogate (V)')
pylab.show()

