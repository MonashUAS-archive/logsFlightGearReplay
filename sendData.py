'''
Created on 9 Aug 2016

@author: bcub3d-build-ubuntu
'''

import socket
import time
from pymavlink import fgFDM
import readLog
import packFDM
from ctypes import *

# Setup
filename = '45.BIN'
overwrite = False # Overwrite csv file

# Flight Gear UDP Connection
UDP_IP = '127.0.0.1'
UDP_PORT = 5503

# Load csv file
csvfile = readLog.convert2CSV(filename,overwrite=overwrite)
data = readLog.readCsv(csvfile)
print '------------------------------------------------------------------'

# Create socket to flight gear
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
sock.connect((UDP_IP,UDP_PORT))

# Create Flight Data Structure
fdm = fgFDM.fgFDM()

while True:
	currTime = 0
	offset=0
	startTime = time.time()
	while time.time()-startTime < data.timeVec[-1]:
		# Get current time
		currTime = time.time()-startTime+offset
		index, timeVal = packFDM.findClosestTime(currTime,data.timeVec)
		
		# Pack Data Into Structure
		fdm = packFDM.fillFDM(fdm, data, index)
		#print fdm.get('altitude', units='meters')
		print fdm.get('longitude',units='degrees')
		print fdm.get('latitude',units='degrees')
		
		
		
		
		time.sleep(0.01)
		
		# Send a message
		sock.send(fdm.pack())

# Close Socket
sock.close()

