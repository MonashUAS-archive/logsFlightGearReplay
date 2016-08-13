'''
Created on 11 Aug 2016

@author: bcub3d-build-ubuntu

Launches Flight Gear with the correct settings to connect over udp.
'''

import os
import subprocess
import sys

# Options
updateRate = 60 # Hz
port = 5503
aircraft = 'Rascal110-JSBSim'
if sys.platform=='win32':
    aircraftDir = os.getcwd()+'\\Aircraft'
else:
    aircraftDir = os.getcwd()+'/Aircraft'
lat = -37.954639
lon = 145.237940

def winFindFlightGear():
    folders =  os.listdir('C:\Program Files')
    # Find first folder with FlightGear
    for folder in folders:
        if folder.find('FlightGear') != -1:
            mypath = 'C:\\Program Files\\' + folder + '\\bin\\fgfs.exe '
            
    return mypath
# Launching
if sys.platform == 'win32':
    launch = winFindFlightGear()
else:
    launch = 'nice fgfs '
    
sock = '--native-fdm=socket,in,%i,,%i,udp ' % (updateRate,port)
fdm = '--fdm=external '
aircraftStr = '--aircraft=%s ' % aircraft
fgAircraft = '--fg-aircraft="%s" ' % aircraftDir
latStr = '--lat=%f ' % lat
lonStr = '--lon=%f ' % lon
geom = '--geometry=650x550 '
other = ('--disable-anti-alias-hud --disable-horizon-effect --timeofday=noon'
            ' --disable-sound --disable-fullscreen --disable-ai-models --fog-disable --disable-specular-highlight')

fullString = launch+sock+fdm+aircraftStr+fgAircraft+latStr+lonStr+geom+other

if sys.platform == 'win32':
    subprocess.Popen(fullString)
else:
    os.system(fullString) 
