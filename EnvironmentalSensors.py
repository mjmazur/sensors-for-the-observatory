import serial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from time import gmtime, strftime, time
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)

def getvalues():

	line = ser.readline()
	line = line.decode('utf-8')

	values = np.fromstring(line, sep=' ')

	return line, values

port = '/dev/ttyACM0' # put the correct serial port in here
baud = 9600

# print(os.listdir('/home/emccd/enclosure-logs/' + thedate))

ser = serial.Serial(port, baud)

line = ser.readline() # Throw away the first line as it may be incomplete

nline = np.zeros(8)
narray = np.zeros(8)
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
		narray = np.delete(narray, np.s_[1:], axis=0)
		f.close()
		f = open(write_path, 'w+')

	line, values = getvalues()

	if values[0] == 99.0 or values[1] == 99.0 or values[2] == 99.0 or values[4] == 99.0:
		line, values = getvalues()

	tnow = np.fromstring(strftime('%H %M %S', gmtime()), sep=' ')
	hours = tnow[0] + tnow[1]/60.0 + tnow[2]/3600.0

	nline[0] = time()
	nline[1] = hours

	for i in range(2,8):
		nline[i] = values[i-2]

	if hours > hoursold:
		narray = np.vstack((narray, nline))
		# f.write(str(time()) + ' ' + str(hours) + ' ' + str(line))
		np.savetxt(write_path, narray, fmt='%d %.5f %.2f %.2f %.2f %.2f %.2f %.2f', header='Unix Time - Secs from 00 - Tfluid - Tshed - TF - HF - TG - HG')
		#f.write(str(nline))
		print(str(nline))
		print('wrote line')

	hoursold = hours

	# print(narray)
	if narray.shape[0] % 5 == 0:
		# print(narray[1:,0])
		x = narray[1:,1]
		y = narray[1:,2]

		fig, ax = plt.subplots(3, figsize=(12,20))
		
		# plt.suptitle('Elginfield EMCCD Conditions', size=25)

		ax[0].plot(x,narray[1:,2], color='green', label='Fluid Temperature')
		ax[0].set_title('Fluid & Shed Temperatures', size=20)
		ax[0].set_ylabel('Fluid Temperature (C)', size=15)
		ax[0].set_xlabel('UTC (h)', size=15)
		ax[0].set_ylim([np.amin(narray[1:,2])-5,np.amax(narray[1:,2])+5])
		ax[0].set_xlim([0,24])
		ax[0].xaxis.set_tick_params(labelbottom=True)
		ax[0].xaxis.set_major_locator(MultipleLocator(1))
		ax[0].xaxis.set_major_formatter(FormatStrFormatter('%d'))
		axst = ax[0].twinx()
		axst.plot(x,narray[1:,3], color='red', label='Shed Temperature')
		axst.set_ylabel('Shed Temperature (C)', size=15)
		axst.set_ylim([np.amin(narray[1:,3])-5,np.amax(narray[1:,3])+5])
		ax[1].plot(x,narray[1:,4], color='blue', label='F-Camera Temperature')
		ax[1].set_title('F-Camera Temperature & Humidity', size=20)
		ax[1].set_ylabel('Fcam Temperature (C)', size=15)
		ax[1].set_xlabel('UTC (h)', size=15)
		ax[1].set_ylim([np.amin(narray[1:,4])-5,np.amax(narray[1:,4])+5])
		ax[1].set_xlim([0,24])
		#ax[1].set_xticklabels()
		axfh = ax[1].twinx()
		axfh.plot(x,narray[1:,5], color='orange', label='F-Camera Humidity')
		axfh.set_ylabel('Fcam Humidity (%)', size=15)
		axfh.set_ylim([0,100])
		ax[2].plot(x,narray[1:,6], color='blue', label='G-Camera Temperature')
		ax[2].set_title('G-Camera Temperature & Humidity', size=20)
		ax[2].set_ylabel('Gcam Temperature (C)', size=15)
		ax[2].set_xlabel('UTC (h)')
		ax[2].set_ylim([np.amin(narray[1:,6])-5,np.amax(narray[1:,6])+5])
		ax[2].set_xlim([0,24])
		#ax[2].set_xticklabels()
		axgh = ax[2].twinx()
		axgh.plot(x,narray[1:,7], color='orange', label='G-Camera Humidity')
		axgh.set_ylabel('Gcam Humidity (%)', size=15)
		axgh.set_ylim([0,100])
		
		ax[0].legend(loc='lower left', frameon=False)
		ax[1].legend(loc='lower left', frameon=False)
		ax[2].legend(loc='lower left', frameon=False)
		axst.legend(loc='lower right', frameon=False)
		axfh.legend(loc='lower right', frameon=False)
		axgh.legend(loc='lower right', frameon=False)

		plt.tight_layout()
		plt.savefig('envplot_' + thedate + '.png')
		plt.close()

	# print(str(time()) + ' ' + strftime('%H:%M:%S', gmtime()) + ' ' + line)

	# print(strftime('%H:%M:%S', gmtime()))
	# print(time())
	# print(hours)