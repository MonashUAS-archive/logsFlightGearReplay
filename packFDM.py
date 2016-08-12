'''
Created on 10 Aug 2016

@author: bcub3d-build-ubuntu

Fills the fdm structure with data from the csv file
'''

import numpy as np

currTime = 10

def findClosestTime(currTime,timeVec):
    '''Finds the time and index in the time vector
    of a given current time.'''
    # Get index
    index = (np.abs(timeVec-currTime)).argmin()
    
    # Get closest time
    timeVal = timeVec[index]
    
    return index, timeVal

def fillFDM(fdm,data,index):
    '''Fills the FDM structure with data for
    the given index of the time in the timeVec.'''
    #fdm.set('timestamp_us', data.timeVec[index]*10e6)
    currData = data.fields[index]
    # Position
    fdm.set('longitude',    float(currData[data.headers['GPS_Lng']]),units='degrees')
    fdm.set('latitude',     float(currData[data.headers['GPS_Lat']]),units='degrees')
    fdm.set('altitude',     float(currData[data.headers['GPS_Alt']]),units='meters')
    # Attitude
    fdm.set('phi',          float(currData[data.headers['ATT_Roll']]),units='degrees')
    fdm.set('theta',        float(currData[data.headers['ATT_Pitch']]),units='degrees')
    fdm.set('psi',          float(currData[data.headers['ATT_Yaw']]),units='degrees')
    # Velocities
    fdm.set('phidot',       float(currData[data.headers['IMU2_GyrX']]),units='dps')
    fdm.set('thetadot',     float(currData[data.headers['IMU2_GyrY']]),units='dps')
    fdm.set('psidot',       float(currData[data.headers['IMU2_GyrZ']]),units='dps')
    fdm.set('vcas',         float(currData[data.headers['ARSP_Airspeed']]),units='mps')
    #Accelerations
    fdm.set('A_X_pilot',    float(currData[data.headers['IMU2_AccX']]),units='mpss')
    fdm.set('A_Y_pilot',    float(currData[data.headers['IMU2_AccY']]),units='mpss')
    fdm.set('A_Z_pilot',    float(currData[data.headers['IMU2_AccZ']]),units='mpss')
    return fdm