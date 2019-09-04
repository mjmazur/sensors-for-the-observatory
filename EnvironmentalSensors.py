import serial
import matplotlib.pyplot as plt
import numpy as np
import os
from time import gmtime, strftime, time

port = '/dev/ttyACM0' # put the correct serial port in here
baud = 9600
write_path = 'output.txt'

thedate = strftime('%Y%m%d', gmtime())

print(os.listdir('/home/emccd/enclosure_logs/' + thedate))

f = open(write_path, 'w+')
ser = serial.Serial(port, baud)

line = ser.readline()
line = line.decode('utf-8')

# print('Unix Time     ' + line)

while True:
	line = ser.readline()
	line = line.decode('utf-8')
	print(str(time()) + ' ' + strftime('%H:%M:%S', gmtime()) + ' ' + line)
	# print(strftime('%H:%M:%S', gmtime()))
	# f.write(str(time()) + ' ' + line) + ' '