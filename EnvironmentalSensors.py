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

nline = np.empty(8)

while True:
	line = ser.readline()
	line = line.decode('utf-8')

	tnow = np.fromstring(strftime('%H %M %S', gmtime()), sep=' ')
	secs = tnow[0] + tnow[1]/60.0 + tnow[2]/3600.0

	values = np.fromstring(line, sep=' ')
	nline[0] = time()
	nline[1] = secs

	for i in range(2,8):
		nline[i] = values[i-2]

	print(nline)

	# print(str(time()) + ' ' + strftime('%H:%M:%S', gmtime()) + ' ' + line)

	# print(strftime('%H:%M:%S', gmtime()))
	# f.write(str(time()) + ' ' + line) + ' '