'''
Created on 9 Aug 2016

@author: bcub3d-build-ubuntu

Converts a tlog into a Python loadable pickle file.
'''

import os
import csv
import time
import numpy as np

filename = '45.BIN'
overwrite = False # Overwrite csv file

def convert2CSV(filename,overwrite=False):
    # First Convert Bin File to .csv
    csvfile = filename.split('.')[0]+'.csv'
    if overwrite or (not os.path.isfile(csvfile)):
        startTime = time.time()
        print 'Converting %s file to %s.' % (filename,csvfile)
        os.system('python sdlog2_dump.py %s -f %s' % (filename,csvfile))
        endTime = time.time()
        print 'Completed conversion in %.2f seconds.' % (endTime-startTime)
    else:
        print '%s already exists, not overwriting.' % csvfile
        
    return csvfile

class logData():
    def __init__(self,name):
        self.name = name
        self.timeVec = []
        self.fields = []
        
    def convertLists2Numpy(self):    
        pass
    
    def appendFields(self):
        pass

def readCsv(csvfile):
    # Open csv file
    f = open(csvfile,'rb')
    reader = csv.reader(f)

    # Create log data class
    data = logData('logs')

    # Get Header Row
    headers = next(reader)
    data.headers = {}
    # Add header lists to class 
    for i in range(3,len(headers)):
        data.headers[headers[i]] = i-3
    # Check if MSG_Message in headers
    if 'MSG_Message' in data.headers.keys():
        msgRm = True
        msgPos = data.headers['MSG_Message']
        data.MSG_Message = []
    else:
        msgRm = False
        
    # Read each row
    rowCount = 0
    for row in reader:
        rowCount += 1
        
        # Store Time
        if not row[data.headers['GPS_TimeUS']+3] == '':
            data.timeVec.append(float(row[data.headers['GPS_TimeUS']+3]))
            
            # Don't store MSG_Message in normal array
            if msgRm:
                rowData = row[3:]
                data.MSG_Message.append(row[msgPos])
                rowData[msgPos] = '0'
            else:
                rowData = row[3:]
                
            # Store Data
            data.fields.append(rowData)
                
            # Display progress
            if rowCount % 1000 == 0:
                print 'Read row %i' % rowCount
            

    # Convert to numpy arrays
    print 'Converting to numpy arrays.'
    data.timeVec = np.array(data.timeVec)
    data.fields = np.array(data.fields)
    
    # Set empty entries to zeros
    print 'Setting empty entries to zero.'
    for entry in data.fields:
        entry[entry==''] = '0'
    
    # Zero intitial time vector, convert to seconds
    print 'Zeroing start time.'
    data.timeVec = (data.timeVec/(1e6)) - (data.timeVec[0]/(1e6))
  
    # Get all main headers
    print 'Sorting Data Headers.'
    data.headersDict = {}
    for header in headers:
        mainHeader = header.split('_')[0]
        if mainHeader not in data.headersDict:
            data.headersDict[mainHeader] = []
        data.headersDict[mainHeader].append(header) 
  
    return data

if __name__ == '__main__':
    csvfile = convert2CSV(filename,overwrite=overwrite)
    data = readCsv(csvfile)