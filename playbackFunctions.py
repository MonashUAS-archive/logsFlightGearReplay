'''
Created on 11 Aug 2016

@author: bcub3d-build-ubuntu
'''
import time
from Tkinter import *

def goToButton(entryBox,timeScale,simThread):
    # Pause Simulation
    simThread.pauseSim()
    # Value of entry box
    mytime = float(entryBox.get())
    # Update time scale
    timeScale.set(mytime)
    time.sleep(0.2)
    # Start Sime
    simThread.startSim(mytime)
    
def createMark(master,colorString,width,xpos):
    # Create canvas with bordless window
    c = Canvas(master,width=width,height=10,bd=0)
    c.create_rectangle(0,0,15,15, fill=colorString,width=0)
    c.place(x=xpos,y=19)
    
    return c
           
def set1(timeScale,c,master,maxTime,simThread):
    # Reposition Canvas
    xPx = (float(timeScale.get())/(1.0*maxTime))*1000.0
    c.place(x=xPx,y=19)
    # Update mark time
    simThread.mark1 = float(timeScale.get())

def set2(timeScale,c,master,maxTime,simThread):
    # Reposition Canvas
    xPx = (float(timeScale.get())/(1.0*maxTime))*1000.0 - 5
    c.place(x=xPx,y=19)
    # Update mark time
    simThread.mark2 = float(timeScale.get())

def set3(timeScale,c,master,maxTime,simThread):
    # Reposition Canvas
    xPx = ((float(timeScale.get())/(1.0*maxTime))*968.0) + 12
    c.place(x=xPx,y=19)
    # Update mark time
    simThread.mark3 = float(timeScale.get())

def createModeRadioButton(master,row,column):
    # Create Variable
    v = IntVar()
    v.set(1)
    rb2 = Radiobutton(master,text='Skim Mode',variable=v,value=2,command=v.set(2)).grid(row=row,column=column+1)
    rb1 = Radiobutton(master,text='Play Mode',variable=v,value=1,command=v.set(1)).grid(row=row,column=column)
    
    return v, [rb1,rb2]
    
    