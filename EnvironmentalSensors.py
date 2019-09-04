import serial
import matplotlib.pyplot as plt
import numpy as np
import os
from time import gmtime, strftime, time

port = '/dev/ttyACM0' # put the correct serial port in here
baud = 9600

thedate = strftime('%Y%m%d', gmtime())
write_path = '/home/emccd/enclosure-logs/' + thedate +'/output.txt'

# print(os.listdir('/home/emccd/enclosure-logs/' + thedate))

f = open(write_path, 'w+')
ser = serial.Serial(port, baud)

line = ser.readline()
line = line.decode('utf-8')

# print('Unix Time     ' + line)

while True:
	line = ser.readline()
	line = line.decode('utf-8')
	print(str(time()) + ' ' + strftime('%H:%M:%S', gmtime()) + ' ' + line)
	test = np.fromstring(line, sep=' ')
	print(test[0])
	# print(strftime('%H:%M:%S', gmtime()))
	# f.write(str(time()) + ' ' + line) + ' '