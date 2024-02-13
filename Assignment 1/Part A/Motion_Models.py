import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import statistics

# Load data
filename = 'training1.csv'
data = np.loadtxt(filename, delimiter=',', skiprows=1)

# Split into columns
index, time, range_, velocity_command, raw_ir1, raw_ir2, raw_ir3, raw_ir4, sonar1, sonar2 = data.T

""" Calculating Motion Model Speed """

# Calculate the difference in time steps 
timeDiff = []
for i in range(0,len(time)-2):
    if (i == 0):
        dt = 0.01
    else:
        dt = time[i+1] - time[i]
        
    timeDiff.append(dt)
    
# Calculating the difference in distance for each time step
distDiff = []
for n in range(0, len(range_)-2):
    if (n == 0):
        dx = 0
    else:
        dx = range_[n+1] - range_[n]
        
    distDiff.append(dx) 

# Calculating the estimated speed of the robot
estimatedSpeed = [x/y for x, y in zip(distDiff,timeDiff)]

    
""" Calculating Motion Model Displacement """
# Calculating Displacement with respect to Command speed
commandDisplacement = []
for n in range(len(timeDiff)):
    commandDisp = velocity_command[n] * timeDiff[n]
    if (n == 0):
        currentDisp = range_[0]
    else:
        currentDisp = previousDisp + commandDisp
        
    commandDisplacement.append(currentDisp)
    previousDisp = currentDisp

# Calculating Displacement with respect Estimated Speed
estimatedDisplacement = []
for n in range(len(timeDiff)):
    estimatedDisp = estimatedSpeed[n] * timeDiff[n]
    if (n == 0):
        currentDisp = range_[0]
    else:
        currentDisp = previousDisp + estimatedDisp
        
    estimatedDisplacement.append(currentDisp)
    previousDisp = currentDisp
    
# Calculating Displacement with respect to Command speed
l9 = np.array(velocity_command, dtype=float)*0.75
modelledDisplacement = []
for n in range(len(timeDiff)):
    modelledDisp = l9[n] * timeDiff[n]
    if (n == 0):
        currentDisp = range_[0]
    else:
        currentDisp = previousDisp + modelledDisp
        
    modelledDisplacement.append(currentDisp)
    previousDisp = currentDisp
    

""" Plotting Motion Model Figures """
fig = plt.figure(figsize=(12, 4))
ax1 = plt.subplot(121)
ax1.plot(time[0:len(time)-2], estimatedSpeed, label='Estimated Speed')
ax1.plot(time[0:len(time)], velocity_command, label='Command Speed')
ax1.plot(time[0:len(time)], l9, label='Modelled Speed')

ax1.set(title="Speed Motion Model", xlabel="Time", ylabel="Velocity")
ax1.legend()

ax2 = plt.subplot(122)
ax2.plot(time, range_, 'r', label='Measured Distance')        
ax2.plot(time[0:len(commandDisplacement)], commandDisplacement, 'b', label='Commanded Distance') 
ax2.plot(time[0:len(estimatedDisplacement)], estimatedDisplacement, 'y', label='Estimated Distance') 
ax2.plot(time[0:len(commandDisplacement)], modelledDisplacement, 'g', label='Modelled Distance') 

ax2.set(title="Displacement Motion Model", xlabel="Time", ylabel="Displacement")
ax2.legend()

plt.show()
