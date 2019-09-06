import serial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from time import gmtime, strftime, time

port = '/dev/ttyACM0' # put the correct serial port in here
baud = 9600

# print(os.listdir('/home/emccd/enclosure-logs/' + thedate))

ser = serial.Serial(port, baud)

line = ser.readline() # Throw away the first line as it may be incomplete
# line = line.decode('utf-8')

# print('Unix Time     ' + line)

nline = np.empty(8)
narray = np.empty(8)

thedate = strftime('%Y%m%d', gmtime())

# write_path = '/home/emccd/enclosure-logs/' + thedate + '_02.log'
write_path = './' + thedate + '_02.log'

f = open(write_path, 'w+')

while True:

	if strftime('%Y%m%d', gmtime()) != thedate:
		thedate = strftime('%Y%m%d', gmtime())
		# write_path = '/home/emccd/enclosure-logs/' + thedate + '_02.log'
		write_path = './' + thedate + '_02.log'
		f.close()
		f = open(write_path, 'w+')

	line = ser.readline()
	line = line.decode('utf-8')

	tnow = np.fromstring(strftime('%H %M %S', gmtime()), sep=' ')
	secs = tnow[0] + tnow[1]/60.0 + tnow[2]/3600.0

	values = np.fromstring(line, sep=' ')

	# print(values[0])

	nline[0] = time()
	nline[1] = secs

	for i in range(2,8):
		nline[i] = values[i-2]

	narray = np.vstack((narray, nline))

	# print(narray)
	if narray.shape[0] % 2 == 0:
		print(narray[1:,0])
		x = narray[1:,1]
		y = narray[1:,2]

		plt.plot(x,y)
		plt.savefig('test.png')

	# print(str(time()) + ' ' + strftime('%H:%M:%S', gmtime()) + ' ' + line)

	# print(strftime('%H:%M:%S', gmtime()))
	# f.write(str(time()) + ' ' + line) + ' '