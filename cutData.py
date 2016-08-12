
import numpy as np

def getSection(data,field,startTime,endTime):
    # Find times that are within the range
    ind = np.where((data.timeVec>=startTime) & (data.timeVec<=endTime))[0]
    # Get time values
    timeData = data.timeVec[ind]
    # Get field values
    fieldData = []
    for index in ind:
        fieldData.append(data.fields[index][data.headers[field]])
    
    # Convert field data to floats
    fieldData = np.array(fieldData)
    fieldData = fieldData.astype(np.float)
    
    return timeData, fieldData

def addDataToPlot(axes,subplot,timeData,fieldData):
    # Plot it
    subplot.set_xdata(timeData)
    subplot.set_ydata(fieldData)
    axes.set_xlim(min(timeData),max(timeData))
    axes.set_ylim(min(fieldData),max(fieldData))
    

    