'''
Created on 11 Aug 2016

@author: bcub3d-build-ubuntu
'''

from Tkinter import *
import ttk
from threading import Thread
import readLog
import socket
import sendDataGUI
import math
import tkinterFunctions
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import cutData
import plotClasses

# Setup
filename = '45.BIN'
overwrite = False # Overwrite csv file
updateRate = 10 # Hz
mainHeaders = sorted(['GPS','IMU','RCIN','RCOU','BARO','POWER','CMD','ARSP','CURR','ATT','MAG','MODE','IMU2','AHR2','POS','MAG2','RATE','CTUN','STAT']) # The main headers to select to plot

# Flight Gear UDP Connection
UDP_IP = '127.0.0.1'
UDP_PORT = 5503

# ============================= Load Data ============================= #
# Load csv file
csvfile = readLog.convert2CSV(filename,overwrite=overwrite)
data = readLog.readCsv(csvfile)
print '------------------------------------------------------------------'

# Create socket to flight gear
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
sock.connect((UDP_IP,UDP_PORT))

# ======================== Simulation Thread ========================= #
# Start Time Thread
simThread = sendDataGUI.outDataThread(data,sock,updateRate)
simThread.start()

# ========================= Tkinter Control ========================== #
# Create Tkinter Window
master = Tk()
master.wm_title('Pixhawk Log Playback Controls')

# Create scale bar
tickinterval = math.floor((data.timeVec[-1]/20.0)/100.0)*100
maxTime = data.timeVec[-1]
timeScale = Scale(master, from_=0, to=maxTime,tickinterval=tickinterval, orient=HORIZONTAL,length=1000,command=lambda x: simThread.updatePosition(bypass=True,bypassTime=float(timeScale.get())))
timeScale.grid(row=0,columnspan=49)

# Create Start/Pause Buttons
Button(master,text='Start Replay', command=lambda: simThread.startSim(timeScale.get())).grid(row=1,column=38)
Button(master,text='Pause Replay', command=simThread.pauseSim).grid(row=1,column=39)

# "Go To" Buttons and Boxes
# Go to Entry Box
e = Entry(master,width=6)
e.grid(row=1,column=1)
e.insert(0,"0")
# Create Go To Button
Button(master,text='Go to:', command=lambda: tkinterFunctions.goToButton(e, timeScale, simThread)).grid(row=1,column=0)
# Seconds Label
l = Label(master,text='s')
l.grid(row=1,column=2,sticky=W)

# Time Marking
# Label
l2 = Label(master,text="Mark [Set,Jump]:")
l2.grid(row=1,column=42,sticky=E)
# Button Set 1
c1 = tkinterFunctions.createMark(master,'green',10,990)
s1 = Button(master,text='S1',bg='green',command=lambda: tkinterFunctions.set1(timeScale, c1, master, maxTime, simThread)).grid(row=1,column=43)
j1 = Button(master,text="J1",bg='green',command=lambda: simThread.jump1(timeScale)).grid(row=1,column=44)
# Button Set 2
c2 = tkinterFunctions.createMark(master,'red',10,990)
s2 = Button(master,text='S2',bg='red',command=lambda: tkinterFunctions.set2(timeScale, c2, master, maxTime, simThread)).grid(row=1,column=45)
j2 = Button(master,text="J2",bg='red',command=lambda: simThread.jump2(timeScale)).grid(row=1,column=46)
# Button Set 3
c3 = tkinterFunctions.createMark(master,'cyan',10,990)
s3 = Button(master,text='S3',bg='cyan',command=lambda: tkinterFunctions.set3(timeScale, c3, master, maxTime, simThread)).grid(row=1,column=47)
j3 = Button(master,text="J3",bg='cyan',command=lambda: simThread.jump3(timeScale)).grid(row=1,column=48)

# Separator
ttk.Separator(master,orient=HORIZONTAL).grid(row=2,columnspan=49,sticky='ew')

# ======================== Tkinter Plotting ========================= #
# Create Plotting Frame
plotFrame = plotClasses.plottingFrame(master,mainHeaders,data,1)
plotFrame.grid(row=3,columnspan=49)

# Add time selector (First Plot Only
plotFrame.timeSelect = Entry(plotFrame,width=8)
plotFrame.timeSelect.grid(row=0,column=5)
plotFrame.timeSelect.insert(0,"20")
plotFrame.timeLabel = Label(plotFrame,text='s')
plotFrame.timeLabel.grid(row=0,column=6,sticky=W)
plotFrame.timeLabel2 = Label(plotFrame,text='Period:')
plotFrame.timeLabel2.grid(row=0,column=4)

plotFrame2 = plotClasses.plottingFrame(master,mainHeaders,data,2)
plotFrame2.grid(row=4,columnspan=49)

# ========================= Tkinter Loop ============================ #
while True:
    if simThread.running:
        timeScale.set(simThread.currTime)
        
        #timeVec, fieldData = cutData.getSection(data, 'ARSP_Airspeed', startTime=max(0,simThread.currTime-20), endTime=simThread.currTime)
        #cutData.addDataToPlot(a,h1,timeVec,fieldData)
        #canvas.draw()
        
    master.update_idletasks()
    master.update()

# Close Socket
sock.close()
