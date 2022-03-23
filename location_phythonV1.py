

import numpy as np
import scipy.io
import math
from scipy import signal


# DataFileName = str('2017-12-15-17-57-15(5).mat')
# cut_start = int(4.08e6) #(1.1e6)
# cut_end = int(6.1e6)  # (7.1e6)

## input
DataFileName = input("Enter File Location")

cut_start = int(input("enter starting point(2000000)"))
cut_end = int(input("enter ending point(6000000)"))

step_size = int(1500)
step_gap = int (150)
MinCorr = 0.01
j = 0


baseline = 10
speedLight = int(3e8)
closer_tolerance = 3.5

Azimuth = np.array
Elevation = np.array
sigIndex = np.array


class signal_import:
    def __init__(self):
        mat_data = scipy.io.loadmat(DataFileName)
        data = mat_data.get("data")
        sig_time = data[:,0]
        temp_sig_o = data[:,2]
        temp_sig_x = data[:,3]
        temp_sig_y = data[:,4]
        self.dt = sig_time[2]-sig_time[1]
        self.sig_o = temp_sig_o [cut_start : cut_end]
        self.sig_x = temp_sig_x [cut_start : cut_end]
        self.sig_y = temp_sig_y [cut_start : cut_end]
        
sig= signal_import()

dt = sig.dt
del sig.dt

import matplotlib.pyplot as plt
# plt.plot(sig.sig_o)

numOfStep = math.floor((cut_end - cut_start - step_size)/step_gap)

for i in range(numOfStep):
    validSig = True 
    
    step_start = i*step_gap
    step_end = step_start + step_size -1
    TempSig_o = sig.sig_o[step_start : step_end]
    TempSig_x = sig.sig_x[step_start : step_end]
    TempSig_y = sig.sig_y[step_start : step_end]
    
    corrox = signal.correlate(TempSig_o,TempSig_x,mode='same')
    corroy = signal.correlate(TempSig_o,TempSig_y,mode='same')
    corryx = signal.correlate(TempSig_y,TempSig_x,mode='same')
    
    if max(corrox)<MinCorr or max(corroy)<MinCorr or max(corryx)<MinCorr:
        validSig = False
        
    #OX
    peakat = np.argmax(corrox)
    if peakat > 10 and peakat < step_size - 10:
        tempPoly = corrox[peakat-2 : peakat+3]
        indexPoly = np.arange(peakat-2 , peakat+3)
        polycor = np.polyfit(indexPoly,tempPoly,2)
        poly_a= polycor.item(0)
        poly_b = polycor.item(1)
        
        PeakWithPolyfit = -0.5 * poly_b/ poly_a
        lagPoints= PeakWithPolyfit - step_size/2
        timeLagOX = lagPoints * dt
    else:
        timeLagOX = 1
            
        
    #OY
    peakat = np.argmax(corroy)
    if peakat > 10 and peakat < step_size - 10:
        tempPoly = corroy[peakat-2 : peakat+3]
        indexPoly = np.arange(peakat-2 , peakat+3)
        polycor = np.polyfit(indexPoly,tempPoly,2)
        poly_a= polycor.item(0)
        poly_b = polycor.item(1)
        
        PeakWithPolyfit = -0.5 * poly_b/ poly_a
        lagPoints= PeakWithPolyfit - step_size/2
        timeLagOY = lagPoints * dt
    else:
        timeLagOY = 1
        
    #YX
    peakat = np.argmax(corryx)
    if peakat > 10 and peakat < step_size - 10:
        tempPoly = corryx[peakat-2 : peakat+3]
        
        indexPoly = np.arange(peakat-2 , peakat+3)
        polycor = np.polyfit(indexPoly,tempPoly,2)
        poly_a= polycor.item(0)
        poly_b = polycor.item(1)
        
        PeakWithPolyfit = -0.5 * poly_b/ poly_a
        lagPoints= PeakWithPolyfit - step_size/2
        timeLagYX = lagPoints * dt
    else:
        timeLagYX = 1
        
    max_delay = 1.1 * (baseline/(speedLight));
    
    if abs(timeLagYX) > max_delay or abs(timeLagYX) > max_delay or abs(timeLagYX) > max_delay:
        validSig = False
    
    closer_time = timeLagOY + timeLagYX - timeLagOX;
    
    if closer_time > closer_tolerance*dt :
        validSig = False
    
    ElRatio = np.sqrt( np.square(timeLagOX) + np.square(timeLagOY) ) * speedLight / baseline
    
    if ElRatio > 1:
        validSig = False
    
    
    
    if validSig == True:
        ElevationAng = math.degrees(math.acos(ElRatio))
        AzimuthAng = 180 + math.degrees(math.atan2((timeLagOX-0),(timeLagOY-0)))
        
        Azimuth = np.append(Azimuth, AzimuthAng )
        Elevation = np.append(Elevation,ElevationAng )
        sigIndex = np.append(sigIndex ,i)

tempAzimuth =Azimuth [1:len(Azimuth)]
tempElevation =Elevation [1:len(Azimuth)]

PAzimuth = tempAzimuth.tolist()
PElevation = tempElevation.tolist()

import matplotlib.pyplot as plt
plt.scatter(PAzimuth,PElevation)
plt.ylabel('Azimuth angle ')
plt.ylabel('Elevation angle ')
plt.show()

    
