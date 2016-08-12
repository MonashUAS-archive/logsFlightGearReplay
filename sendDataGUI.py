'''
Created on 9 Aug 2016

@author: bcub3d-build-ubuntu
'''

import time
from pymavlink import fgFDM
import packFDM
import threading

class outDataThread(threading.Thread):
	'''Creates a thread to grab the data and send it
	to the socket to flight gear.'''
	def __init__(self,data,sock,updateRate):
		threading.Thread.__init__(self)
		self.data = data
		self.sock = sock
		self.running = False
		self.updateRate = updateRate
		self.currTime = 0
		self.blockStartTime = 0
		self.blockStartSimTime = 0
		self.stop = False
		
		# Mark Values
		self.mark1 = 0
		self.mark2 = 0
		self.mark3 = 0
		
		# Create Flight Data Structure
		self.fdm = fgFDM.fgFDM()
		
	def updatePosition(self,bypass=False,bypassTime=0,mode=1):
		# Get current time
		if not bypass:
			self.currTime = time.time()-self.blockStartTime + self.blockStartSimTime
		elif mode.get()==2:
			self.currTime = bypassTime
			self.blockStartTime = time.time()
			self.blockStartSimTime = self.currTime
			pass
			
		# Get Relevant Index
		index, _ = packFDM.findClosestTime(self.currTime,self.data.timeVec)
	
		# Pack Data Into Structure
		self.fdm = packFDM.fillFDM(self.fdm, self.data, index)
			
		# Wait time	
		time.sleep(1.0/self.updateRate)
		
		# Send a message
		self.sock.send(self.fdm.pack())
	
	def run(self):
		while not self.stop:
			self.blockStartSimTime = self.currTime
			self.blockStartTime = time.time()
			while self.running:
				self.updatePosition()
			
			# Wait to recheck if sim is running
			time.sleep(1)
			
	def startSim(self,time):
		self.running=True
		self.currTime = time
		print 'Sim starting at %.2f s.' % time
	
	def pauseSim(self):
		self.running=False
		print 'Sim paused at %.2f s.' % self.currTime
			
	def jump1(self,timeScale):
		# Update sim
		self.startSim(self.mark1)
		# Update scale
		timeScale.set(self.currTime)
		time.sleep(1)
		# Pause Sim
		self.pauseSim()
		
	def jump2(self,timeScale):
		# Update sim
		self.startSim(self.mark2)
		# Update scale
		timeScale.set(self.currTime)
		time.sleep(1)
		# Pause Sim
		self.pauseSim()
		
	def jump3(self,timeScale):
		# Update sim
		self.startSim(self.mark3)
		# Update scale
		timeScale.set(self.currTime)
		time.sleep(1)
		# Pause Sim
		self.pauseSim()
				
