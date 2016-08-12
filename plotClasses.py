'''
Created on 12 Aug 2016

@author: bcub3d-build-ubuntu
'''

from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import cutData

class plottingFrame(Frame):
    
    def __init__(self,master,mainHeaders,data,id,simThread):
        Frame.__init__(self,master,width=800,height=1000)
        
        # Store Info
        self.master = master
        self.mainHeaders = mainHeaders
        self.data = data
        self.id = id
        self.simThread = simThread
        
        # Create Variables
        self.mainOpt = StringVar(self)
        self.smallOpt = StringVar(self)
        
        # Add Fig Buttons
        self.addFigureButtons()
        
        # Add Plot Buttons
        self.addPlotButtons()
        
        # Create Option Menus
        self.createOptionMenus()
        
        # Create Empty Figure
        self.createFigure()
        
        # Create Plotting Canvas
        self.createPlottingCanvas()
    
    def createOptionMenus(self):
        # Create Option Menus
        self.m1 = apply(OptionMenu,(self,self.mainOpt)+tuple(self.mainHeaders))
        self.mainOpt.set(self.mainHeaders[0])
        self.m2 = apply(OptionMenu,(self,self.smallOpt)+tuple(self.data.headersDict[self.mainOpt.get()]))
        self.smallOpt.set(self.data.headersDict[self.mainOpt.get()][0])
        
        # Add Trace
        self.mainOpt.trace('w',self.updateVar)
          
        # Layout Menus
        self.m1.grid(row=0,column=42)
        self.m2.grid(row=0,column=43)
    
    def updateVar(self,*args):
        # Update Variable
        smallHeaders = self.data.headersDict[self.mainOpt.get()]
        self.smallOpt.set(smallHeaders[0])
         
        # Delete Old Entries
        menu = self.m2['menu']
        menu.delete(0,'end')
        
        # Add New Entries
        for head in smallHeaders:
            menu.add_command(label=head, command=lambda myHead=head: self.smallOpt.set(myHead))
            
    def addFigureButtons(self):
        # Add Fig Label
        self.addFigLabel = Label(self,text='Figure: ')
        self.addFigLabel.grid(row=0,column=0)
        
        # Add Fig '+' Button
        self.addFigButton1 = Button(self,text='+',command=lambda: addNewFigure(self.id+1,self.master,self.mainHeaders,self.data,self.simThread))
        self.addFigButton1.grid(row=0,column=1)
        
        # Add Fig '-' Button
        if self.id != 1:
            self.addFigButton2 = Button(self,text='-',command=lambda: removeFigure(self.id,self.master))
            self.addFigButton2.grid(row=0,column=2)  
            
    def updatePlot(self):
        # Get Period
        period = float((self.master.plotFrame[0]).timeSelect.get())
        # Get new data
        currTime = self.simThread.currTime
        timeData, fieldData = cutData.getSection(self.data, self.smallOpt.get(), currTime-period, currTime)
        # Plot Data 
        cutData.addDataToPlot(self.axes,self.plotHandles[0],timeData,fieldData)
        
    def addPlotButtons(self):
        
        # Add Fig Label
        self.addPlotLabel = Label(self,text='Plot: ')
        self.addPlotLabel.grid(row=0,column=46)
        
        # Add Fig '+' Button
        self.addPlotButton1 = Button(self,text='+',command=lambda: self.updatePlot())
        self.addPlotButton1.grid(row=0,column=47)
        
        # Add Fig '-' Button
        self.addPlotButton2 = Button(self,text='-')
        self.addPlotButton2.grid(row=0,column=48)
        
        
    def createFigure(self):
        # Create Figure
        self.fig = Figure(figsize=(12.5,3))
        # Add Subplot
        self.axes = self.fig.add_subplot(111)
        # Adjustments
        self.axes.set_xlabel('Time (s)')
        self.fig.subplots_adjust(bottom=0.18)
        self.plotHandles = []
        self.plotHandles.append((self.axes.plot([],[]))[0])
        
    def createPlottingCanvas(self):
        # Create Canvas, add plot to it.
        self.canvas = FigureCanvasTkAgg(self.fig,master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=1,columnspan=49,sticky=NSEW)
        
def addTimeSelector(frame):
    # Entry Bar
    frame.timeSelect = Entry(frame,width=8)
    frame.timeSelect.grid(row=0,column=5)
    frame.timeSelect.insert(0,"20")
    # Seconds Label
    frame.timeLabel = Label(frame,text='s')
    frame.timeLabel.grid(row=0,column=6,sticky=W)
    # Period Label
    frame.timeLabel2 = Label(frame,text='Period:')
    frame.timeLabel2.grid(row=0,column=4)
    
    return frame
    
def addNewFigure(plotID,masterFrame,mainHeaders,data,simThread):
    masterFrame.plotFrame.append(plottingFrame(masterFrame,mainHeaders,data,plotID,simThread))
    masterFrame.plotFrame[plotID-1].grid(row=plotID+2,columnspan=49)
    
    return masterFrame

def removeFigure(plotID,masterFrame):
    masterFrame.plotFrame[plotID-1].grid_forget()

    
    
    