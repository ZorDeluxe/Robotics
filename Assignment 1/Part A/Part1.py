import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

# Load data
filename = 'training2.csv'
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

# Apply a moving average filter to determine the velocity
avgSpeed = []
for n in range(len(estimatedSpeed)-6):
    total = sum(estimatedSpeed[n:n+5])
    avg_speed = total/len(estimatedSpeed[n:n+5])
    avgSpeed.append(avg_speed)
print(len(avgSpeed))


# Apply a moving median filter to determine the velocity
medianSpeed = []
for n in range(0,len(estimatedSpeed)-6):
    median_speed = signal.medfilt(estimatedSpeed[n:n+5],5)
    medianSpeed.append(median_speed)
    print(len(medianSpeed))
    
    
""" Calculating Motion Model Displacement """
# Calculating Displacement with respect to Command speed
commandDisplacement = []
for n in range(len(timeDiff)):
    commandDisp = velocity_command[n] * timeDiff[n]
    if (n == 0):
        currentDisp = 0
    else:
        currentDisp = previousDisp + commandDisp
        
    commandDisplacement.append(currentDisp)
    previousDisp = currentDisp

# Calculating Displacement with respect Estimated Speed
estimatedDisplacement = []
for n in range(len(timeDiff)):
    estimatedDisp = estimatedSpeed[n] * timeDiff[n]
    if (n == 0):
        currentDisp = 0
    else:
        currentDisp = previousDisp + estimatedDisp
        
    estimatedDisplacement.append(currentDisp)
    previousDisp = currentDisp

# Calculating Displacement with respect Estimated Speed using moving average filter
modelledDisplacement = []
for n in range(len(avgSpeed)):
    modelledDisp = avgSpeed[n] * timeDiff[n]
    if (n == 0):
        currentDisp = 0
    else:
        currentDisp = previousDisp + modelledDisp
        
    modelledDisplacement.append(currentDisp)
    previousDisp = currentDisp
    
# Calculating Displacement with respect Estimated Speed using moving median filter
modelledDisplacement1 = []
for n in range(len(medianSpeed)):
    modelledDisp1 = medianSpeed[n] * timeDiff[n]
    if (n == 0):
        currentDisp = 0
    else:
        currentDisp = previousDisp + modelledDisp1
        
    modelledDisplacement1.append(currentDisp)
    previousDisp = currentDisp

""" Plotting Motion Model Figures """
fig = plt.figure(figsize=(12, 4))
ax1 = plt.subplot(121)
ax1.plot(time[0:len(time)-2], estimatedSpeed, label='Estimated Speed')
ax1.plot(time[0:len(time)], velocity_command, label='Command Speed')
ax1.plot(time[0:len(time)-8], avgSpeed, label='Modelled Speed')
#ax1.plot(time[0:len(time)-8], medianSpeed, label='Modelled Speed Median')

ax1.set(title="Speed Motion Model", xlabel="Time", ylabel="Velocity")
ax1.legend()

ax2 = plt.subplot(122)
ax2.plot(time, range_, 'r', label='Measured Distance')        
ax2.plot(time[0:len(commandDisplacement)], commandDisplacement, 'b', label='Commanded Distance') 
ax2.plot(time[0:len(estimatedDisplacement)], estimatedDisplacement, 'y', label='Estimated Distance') 
ax2.plot(time[0:len(modelledDisplacement)], modelledDisplacement, 'g', label='Modelled Distance') 
ax2.set(title="Displacement Motion Model", xlabel="Time", ylabel="Displacement")
ax2.legend()

plt.show()
