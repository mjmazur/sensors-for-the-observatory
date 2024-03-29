import serial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from time import gmtime, strftime, time, sleep
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)

def getvalues():

	line = ser.readline()
	line = line.decode('utf-8')

	values = np.fromstring(line, sep=' ')

	return values

thedate = strftime('%Y%m%d', gmtime())

port = '/dev/ttyACM0' # put the correct serial port in here
baud = 9600

ser = serial.Serial(port, baud)

#line = ser.readline() # Throw away the first line as it may be incomplete
getvalues() # Throw away the first line as it may be incomplete

write_file = 'env_' + thedate + '_02'

write_path = '/home/emccd/enclosure-logs/' + thedate + '/'
# write_path = './'

# If the log file exists, open it and append new data to it.
# Otherwise, create a new array for values.
if os.path.isfile(write_path + write_file + '.log') == True:
	narray = np.loadtxt(write_path + write_file + '.log', skiprows=1)
else:
	narray = np.full(8,-999.0)

nline = np.zeros(8)

hoursold = 0.0

while True:
	# If the date has rolled over to a new day, start a new log and plot
	if strftime('%Y%m%d', gmtime()) != thedate:
		thedate = strftime('%Y%m%d', gmtime())
		write_path = '/home/emccd/enclosure-logs/' + thedate + '/'
		write_file = 'env_' + thedate + '_02'
		narray = np.delete(narray, np.s_[1:], axis=0)

	# print(narray.shape[0])

	values = getvalues()

	# If the list of values is incomplete (less than 6 elements), read again
	while len(values) != 6:
		values = getvalues()

	# Sometimes we see a spike in the one-wire temperature probe. Catch it and re-read if it happens
	if values[0] == 99.0 or values[1] == 99.0 or values[2] == 99.0 or values[4] == 99.0:
		values = getvalues()
		while len(values) < 6:
			values = getvalues()
	elif len(narray) > 2 and abs(values[0] - narray[len(narray)-1,2]) > 5:
		print('rapid rise in T')
		values = getvalues()
		while len(values) < 6:
			values = getvalues()

	tnow = np.fromstring(strftime('%H %M %S', gmtime()), sep=' ') # Get current UTC
	hours = tnow[0] + tnow[1]/60.0 + tnow[2]/3600.0 # Number of hours from 00 UTC

	# Set the first two array elements to unix time and fractional UTC hours respectively
	nline[0] = time()
	nline[1] = hours

	# Fill the rest of the line with the values retrieved from the sensors
	for i in range(2,8):
		nline[i] = values[i-2]

	if hours > hoursold: # Fixes an issue when not using GMT. Can probably be removed.
		narray = np.vstack((narray, nline))
		np.savetxt(write_path + write_file + '.log', narray[1:,:], fmt='%d %.5f %.2f %.2f %.2f %.2f %.2f %.2f', header='Unix Time - Hours from 00 - Tfluid - Tshed - TF - HF - TG - HG')

	hoursold = hours

	### Plotting section ###

	# Check size of the array and make a plot if divisible by modulo argument
	# This allows for the plot to be updated at a different rate than the saved file

	if (len(narray) > 2) and (narray.shape[0] % 1 == 0):
		x = narray[1:,1]
		y = narray[1:,2]

		fig, ax = plt.subplots(3, figsize=(12,20))

		ax[0].plot(x,narray[1:,2], color='green', label='Fluid Temperature')
		ax[0].set_title('Fluid & Shed Temperatures', size=20)
		ax[0].set_ylabel('Fluid Temperature (C)', size=15)
		ax[0].set_xlabel('UTC (h)', size=15)
		ax[0].set_ylim([np.amin(narray[1:,2])-5,np.amax(narray[1:,2])+5])
		ax[0].set_xlim([0,24])
		ax[0].xaxis.set_tick_params(labelbottom=True)
		ax[0].xaxis.set_major_locator(MultipleLocator(1))
		ax[0].xaxis.set_major_formatter(FormatStrFormatter('%d'))
		ax[0].xaxis.set_minor_locator(MultipleLocator(0.25))
		ax[0].yaxis.set_major_locator(MultipleLocator(1))
		ax[0].yaxis.set_major_formatter(FormatStrFormatter('%d'))
		ax[0].yaxis.set_minor_locator(MultipleLocator(0.5))

		axst = ax[0].twinx()
		axst.plot(x,narray[1:,3], color='red', label='Shed Temperature')
		axst.set_ylabel('Shed Temperature (C)', size=15)
		axst.set_ylim([np.amin(narray[1:,3])-5,np.amax(narray[1:,3])+5])
		axst.yaxis.set_major_locator(MultipleLocator(1))
		axst.yaxis.set_major_formatter(FormatStrFormatter('%d'))
		axst.yaxis.set_minor_locator(MultipleLocator(0.5))

		ax[1].plot(x,narray[1:,4], color='blue', label='F-Camera Temperature')
		ax[1].set_title('F-Camera Temperature & Humidity', size=20)
		ax[1].set_ylabel('Fcam Temperature (C)', size=15)
		ax[1].set_xlabel('UTC (h)', size=15)
		ax[1].set_ylim([np.amin(narray[1:,4])-5,np.amax(narray[1:,4])+5])
		ax[1].set_xlim([0,24])
		ax[1].xaxis.set_major_locator(MultipleLocator(1))
		ax[1].xaxis.set_major_formatter(FormatStrFormatter('%d'))
		ax[1].xaxis.set_minor_locator(MultipleLocator(0.25))
		ax[1].yaxis.set_major_locator(MultipleLocator(1))
		ax[1].yaxis.set_major_formatter(FormatStrFormatter('%d'))
		ax[1].yaxis.set_minor_locator(MultipleLocator(0.5))

		axfh = ax[1].twinx()
		axfh.plot(x,narray[1:,5], color='orange', label='F-Camera Humidity')
		axfh.set_ylabel('Fcam Humidity (%)', size=15)
		axfh.set_ylim([0,100])
		axfh.yaxis.set_major_locator(MultipleLocator(10))
		axfh.yaxis.set_major_formatter(FormatStrFormatter('%d'))
		axfh.yaxis.set_minor_locator(MultipleLocator(2))

		ax[2].plot(x,narray[1:,6], color='blue', label='G-Camera Temperature')
		ax[2].set_title('G-Camera Temperature & Humidity', size=20)
		ax[2].set_ylabel('Gcam Temperature (C)', size=15)
		ax[2].set_xlabel('UTC (h)')
		ax[2].set_ylim([np.amin(narray[1:,6])-5,np.amax(narray[1:,6])+5])
		ax[2].set_xlim([0,24])
		ax[2].xaxis.set_major_locator(MultipleLocator(1))
		ax[2].xaxis.set_major_formatter(FormatStrFormatter('%d'))
		ax[2].xaxis.set_minor_locator(MultipleLocator(0.25))
		ax[2].yaxis.set_major_locator(MultipleLocator(1))
		ax[2].yaxis.set_major_formatter(FormatStrFormatter('%d'))
		ax[2].yaxis.set_minor_locator(MultipleLocator(0.5))

		axgh = ax[2].twinx()
		axgh.plot(x,narray[1:,7], color='orange', label='G-Camera Humidity')
		axgh.set_ylabel('Gcam Humidity (%)', size=15)
		axgh.set_ylim([0,100])
		axgh.yaxis.set_major_locator(MultipleLocator(10))
		axgh.yaxis.set_major_formatter(FormatStrFormatter('%d'))
		axgh.yaxis.set_minor_locator(MultipleLocator(2))
		
		ax[0].legend(loc='lower left', frameon=False)
		ax[1].legend(loc='lower left', frameon=False)
		ax[2].legend(loc='lower left', frameon=False)
		axst.legend(loc='lower right', frameon=False)
		axfh.legend(loc='lower right', frameon=False)
		axgh.legend(loc='lower right', frameon=False)

		plt.tight_layout()
		plt.savefig(write_path + write_file + '.png', dpi=300)
		plt.savefig(write_path + '../current/environment_02.png', dpi=300)
		plt.close()

	sleep(120)