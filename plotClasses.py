'''
Created on 12 Aug 2016

@author: bcub3d-build-ubuntu
'''

from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class plottingFrame(Frame):
    
    def __init__(self,master,mainHeaders,data,id):
        Frame.__init__(self,master,width=800,height=1000)
        
        # Store Info
        self.master = master
        self.mainHeaders = mainHeaders
        self.data = data
        self.id = id
        
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
        self.addFigButton1 = Button(self,text='+')
        self.addFigButton1.grid(row=0,column=1)
        
        # Add Fig '-' Button
        if self.id != 1:
            self.addFigButton2 = Button(self,text='-')
            self.addFigButton2.grid(row=0,column=2)        
        
    def addPlotButtons(self):
        # Add Fig Label
        self.addPlotLabel = Label(self,text='Plot: ')
        self.addPlotLabel.grid(row=0,column=46)
        
        # Add Fig '+' Button
        self.addPlotButton1 = Button(self,text='+')
        self.addPlotButton1.grid(row=0,column=47)
        
        # Add Fig '-' Button
        self.addPlotButton2 = Button(self,text='-')
        self.addPlotButton2.grid(row=0,column=48)
        
    def createFigure(self):
        # Create Figure
        self.fig = Figure(figsize=(12.5,3))
        # Add Subplot
        self.subplot = self.fig.add_subplot(111)
        # Adjustments
        self.subplot.set_xlabel('Time (s)')
        self.fig.subplots_adjust(bottom=0.18)
        self.plotHandles = []
        self.plotHandles.append(self.subplot.plot([],[]))
        
    def createPlottingCanvas(self):
        # Create Canvas, add plot to it.
        self.canvas = FigureCanvasTkAgg(self.fig,master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=1,columnspan=49,sticky=NSEW)