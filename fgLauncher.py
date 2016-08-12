'''
Created on 11 Aug 2016

@author: bcub3d-build-ubuntu

Launches Flight Gear with the correct settings to connect over udp.
'''

import os

# Options
updateRate = 60 # Hz
port = 5503
aircraft = 'Rascal110-JSBSim'
aircraftDir = os.getcwd()+'/Aircraft'
lat = -37.954639
lon = 145.237940

# Launching
launch = 'nice fgfs '
sock = '--native-fdm=socket,in,%i,,%i,udp ' % (updateRate,port)
fdm = '--fdm=external '
aircraftStr = '--aircraft=%s ' % aircraft
fgAircraft = '--fg-aircraft="%s" ' % aircraftDir
latStr = '--lat=%f ' % lat
lonStr = '--lon=%f ' % lon
geom = '--geometry=650x550 '
other = ('--bpp=32 --disable-anti-alias-hud --disable-horizon-effect --timeofday=noon'
            ' --disable-sound --disable-fullscreen --disable-ai-models --fog-disable --disable-specular-highlight --wind=0@0')

fullString = launch+sock+fdm+aircraftStr+fgAircraft+latStr+lonStr+geom+other
os.system(fullString)
