
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np 
import copy


# In[2]:


def SplitMatrix(t,v,depth = 0):
    i = 0
    if len(t) != 0:
        while i < (len(t)-1):
            i += 1

            if t[i] == 0 and v[i] == 0:
                time,amp = SplitMatrix(t[i+1:],v[i+1:],(depth + 1))
                time[depth] = t[0:i-1]
                amp[depth] = v[0:i-1]
                break
    else:
        time = np.array([None]*depth)
        amp = np.array([None]*depth)
        
            
    return time,amp


# In[3]:


def ConvertObjectArrayToFloat(obj):
    temp = copy.deepcopy(obj)
    for i in range(0,len(obj)):
        temp[i] = temp[i].astype('float64')
        
    return temp


# In[4]:


def GetPhysicalValuesFromDigitizedReadings(amp,VoltageQuantizedStep,AccelerationQuantizedStep):
    #Voltage in units of V
    voltage = copy.deepcopy(amp)
    for j in range(0,len(voltage)):
        for i in range(0,len(voltage[j])):
            voltage[j][i] = voltage[j][i]*VoltageQuantizedStep      

    #Acceleration in units of g
    accel = copy.deepcopy(voltage)
    for j in range(0,len(accel)):
        for i in range(0,len(accel[j])):
            accel[j][i] = accel[j][i]*AccelerationQuantizedStep - 50
            
    return voltage, accel


# In[5]:


def ImportData(filename):
    
    dataset = pd.read_csv(filename, header = None, index_col = False)
    dataset.rename(columns={0: "Time", 1: "Value"}, inplace = True)
    alltimes = np.array(dataset["Time"].values)
    allvalues = np.array(dataset["Value"].values)

    time, amp = SplitMatrix(alltimes,allvalues)
    time = ConvertObjectArrayToFloat(time)
    amp = ConvertObjectArrayToFloat(amp)
    
    return time, amp


# In[6]:


def ExtractData(filename,VoltageQuantizedStep,AccelerationQuantizedStep):
    
    time,amp = ImportData(filename)
    voltage,acceleration = GetPhysicalValuesFromDigitizedReadings(amp,VoltageQuantizedStep,AccelerationQuantizedStep)
    
    return time,amp,voltage,acceleration

