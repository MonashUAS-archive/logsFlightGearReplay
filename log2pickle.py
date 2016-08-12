'''
Created on 9 Aug 2016

@author: bcub3d-build-ubuntu

Converts a tlog into a Python loadable pickle file.
'''

import struct
from pymavlink import mavutil


def test():
    filename = 'mav.tlog'
    
    class mavmsg():
        def __init__(self,name):
            self.name = name
    
    # Get log information
    mlog = mavutil.mavlink_connection(filename,zero_time_base=True)
    
    # Create Message Store
    msgTypes = []
    msgFields = []
    lats = []
    
    # Get messages
    msg = mlog.recv_match()
    startTime = msg._timestamp
    
    print 'Recieving Messages.'
    i=0
    while msg is not None:
        currtime = msg._timestamp # Message time
        msgType = msg.get_type() # Message Type, e.g. Heartbeat
        if msgType not in  ['BAD_DATA','FMT','PARM']:  
            fields = msg.fieldnames  # Fields
            
            if msgType not in msgTypes:
                msgTypes.append(msgType)
                
            for field in fields:
                if field not in msgFields:
                    msgFields.append(field)
                if field == 'lat':
                    lats.append([currtime - startTime, getattr(msg,field)])
    
            # Display Progress
            i=i+1
            if i % 25000 == 0:
                print 'Read %i messages.' % i
                
        # Get next messgae
        msg = mlog.recv_match()
        
    
    print 'Completed recieving messages.'
    
    print '\nAvaliable Messages.'
    for type in msgTypes:
        print type
    
    print '\nAvaliable Fields.'
    for fields in msgFields:
        print fields
    print len(msgFields)
    
    return lats
    
    
    
