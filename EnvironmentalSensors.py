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
hoursold = 0.0

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
	hours = tnow[0] + tnow[1]/60.0 + tnow[2]/3600.0

	values = np.fromstring(line, sep=' ')

	# print(values[0])

	nline[0] = time()
	nline[1] = hours

	for i in range(2,8):
		nline[i] = values[i-2]

	if hours > hoursold:
		narray = np.vstack((narray, nline))
		f.write(str(time()) + ' ' + str(hours) + ' ' + str(line))

	hoursold = hours

	# print(narray)
	if narray.shape[0] % 5 == 0:
		# print(narray[1:,0])
		x = narray[1:,1]
		y = narray[1:,2]

		fig, ax = plt.subplots(4, figsize=(12,20), sharex=True)

		ax[0].plot(x,narray[1:,2], color='blue')
		ax[0].set_ylabel('Fluid Temperature (C)')
		ax[0].set_xlabel('UTC (h)')
		ax[0].set_ylim([0,50])
		ax[1].plot(x,narray[1:,3], color='blue')
		ax[1].set_ylabel('Shed Temperature (C)')
		ax[1].set_ylim([0,50])
		ax[2].plot(x,narray[1:,4], color='blue')
		ax[2].set_ylabel('Fcam Temperature (C)')
		ax[2].set_ylim([0,50])
		axfh = ax[2].twinx()
		axfh.plot(x,narray[1:,5], color='orange')
		axfh.set_ylabel('Fcam Humidity (%)')
		axfh.set_ylim([0,100])
		ax[3].plot(x,narray[1:,6], color='blue')
		ax[3].set_ylabel('Gcam Temperature (C)')
		ax[3].set_xlabel('UTC (h)')
		ax[3].set_ylim([0,50])
		axgh = ax[3].twinx()
		axgh.plot(x,narray[1:,7], color='orange')
		axgh.set_ylabel('Gcam Humidity (%)')
		axgh.set_ylim([0,100])
		
		plt.tight_layout()
		plt.savefig('envplot_' + thedate + '.png')
		plt.close()

	# print(str(time()) + ' ' + strftime('%H:%M:%S', gmtime()) + ' ' + line)

	# print(strftime('%H:%M:%S', gmtime()))
	# print(time())
	# print(hours)