import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import myoutliers
import gradientDescent

# Load data
filename = 'calibration.csv'
data = np.loadtxt(filename, delimiter=',', skiprows=1)

# Split into columns
index, time, distance, velocity_command, raw_ir1, raw_ir2, raw_ir3, raw_ir4, \
    sonar1, sonar2 = data.T

""" Removing Sensor Outliers """
Samples = 25

# Infrared Sensor 1
IR1Clean = []
distIRClean = []
for i in range(0, len(raw_ir1)-Samples, Samples):
    IR1Outlier = myoutliers.is_outlier(raw_ir1[i:i+Samples])
    for n in range(len(raw_ir1[i:i+Samples])):
        if (IR1Outlier[n] == False):
            IR1Clean.append(raw_ir1[i+n])
            distIRClean.append(distance[i+n])

# Infrared Sensor 2
IR2Clean = []
distIR2Clean = []
for i in range(0, len(raw_ir2)-Samples, Samples):
    IR2Outlier = myoutliers.is_outlier(raw_ir2[i:i+Samples])
    for n in range(len(raw_ir2[i:i+Samples])):
        if (IR2Outlier[n] == False):
            IR2Clean.append(raw_ir2[i+n])
            distIR2Clean.append(distance[i+n])
                        
# Infrared Sensor 3
IR3Clean = []
distIR3Clean = []
for i in range(0, len(raw_ir3)-Samples, Samples):
    IR3Outlier = myoutliers.is_outlier(raw_ir3[i:i+Samples])
    for n in range(len(raw_ir3[i:i+Samples])):
        if (IR3Outlier[n] == False):
            IR3Clean.append(raw_ir3[i+n])
            distIR3Clean.append(distance[i+n])
                                    
# Infrared Sensor 3
IR4Clean = []
distIR4Clean = []
for i in range(0, len(raw_ir4)-Samples, Samples):
    IR4Outlier = myoutliers.is_outlier(raw_ir4[i:i+Samples])
    for n in range(len(raw_ir4[i:i+Samples])):
        if (IR4Outlier[n] == False):
            IR4Clean.append(raw_ir4[i+n])
            distIR4Clean.append(distance[i+n])    
            
# Sonar1
sonar1Clean = []
distSonarClean = []
for i in range(0, len(sonar1)-Samples, Samples):
    sonar1Outlier = myoutliers.is_outlier(sonar1[i:i+Samples])
    
    for n in range(len(sonar1[i:i+Samples])):
        if (sonar1Outlier[n] == False):
            sonar1Clean.append(sonar1[i+n])
            distSonarClean.append(distance[i+n])    
              
# Sonar2
sonar2Clean = []
distSonar2Clean = []
for i in range(0, len(sonar2)-Samples, Samples):
    sonar2Outlier = myoutliers.is_outlier(sonar2[i:i+Samples])
    for n in range(len(sonar2[i:i+Samples])):
        if (sonar2Outlier[n] == False):
            sonar2Clean.append(sonar2[i+n])
            distSonar2Clean.append(distance[i+n])                

""" Modelling Sensor using OLS """
# Gradient Descent Parameters


# IR 3
IR1Coeff = gradientDescent.IR(distIRClean, IR1Clean, [0, 0, 0.1])
k1 = IR1Coeff[1]
print(IR1Coeff)
l5 = k1/(np.array(distIRClean, dtype=float)) + IR1Coeff[0] + np.array(distIRClean, dtype=float)*IR1Coeff[2]


# IR 3
IR2Coeff = gradientDescent.IR(distIR2Clean, IR2Clean, [0, 0, 0.1])
k1 = IR2Coeff[1]
print(IR2Coeff)
l4 = k1/(np.array(distIR2Clean, dtype=float)) + IR2Coeff[0] + np.array(distIR2Clean, dtype=float)*IR2Coeff[2]


# IR 3
IR3Coeff = gradientDescent.IR(distIR3Clean, IR3Clean, [0, 0, 0.15])
k1 = IR3Coeff[1]
print(IR3Coeff)
l3 = k1/(np.array(distIR3Clean, dtype=float)) + IR3Coeff[0] + np.array(distIR3Clean, dtype=float)*IR3Coeff[2]

# IR 4
IR4Coeff = gradientDescent.IR(distIR4Clean, IR4Clean, [0, 0, 0.15])
k1 = IR4Coeff[1]
print(IR4Coeff)
l6 = k1/(np.array(distIR4Clean, dtype=float)) + IR4Coeff[0] + np.array(distIR4Clean, dtype=float)*IR4Coeff[2]


# Sonar 1
SonarCoeff = gradientDescent.Sonar(distSonarClean, sonar1Clean, [0, 1])
print(SonarCoeff)
l = np.array(distSonarClean, dtype=float)*SonarCoeff[1]+SonarCoeff[0]

# Sonar 2 
SonarCoeff2 = gradientDescent.Sonar(distSonar2Clean, sonar2Clean, [0.2, 1])
print(SonarCoeff2)
l2 = np.array(distSonar2Clean, dtype=float)*SonarCoeff2[1]+SonarCoeff2[0]


""" Plotting Motion Model Figures """

fig, ax = plt.subplots(2,3)


ax[0,0].plot(distance, raw_ir1, 'b.', alpha=0.2)
ax[0,0].plot(distIRClean, IR1Clean, 'r.', alpha=0.2)
ax[0,0].plot(distIRClean, l5, 'g.', alpha=0.2)
ax[0,0].set_title('IR1')

ax[0,1].plot(distance, raw_ir2, 'b.', alpha=0.2)
ax[0,1].plot(distIR2Clean, IR2Clean, 'r.', alpha=0.2)
ax[0,1].plot(distIR2Clean, l4, 'g.', alpha=0.2)
ax[0,1].set_title('IR2')

ax[0,2].plot(distance, raw_ir3, 'b.', alpha=0.2)
ax[0,2].plot(distIR3Clean, IR3Clean, 'r.', alpha=0.2)
ax[0,2].plot(distIR3Clean, l3, 'g.', alpha=0.2)
ax[0,2].set_title('IR3')

ax[1,0].plot(distance, raw_ir4, 'b.', alpha=0.2)
ax[1,0].plot(distIR4Clean, IR4Clean, 'r.', alpha=0.2)
ax[1,0].plot(distIR4Clean, l6, 'g.', alpha=0.2)
ax[1,0].set_title('IR4')

ax[1,1].plot(distance, sonar1, 'b.', alpha=0.2)
ax[1,1].plot(distSonarClean, sonar1Clean, 'r.', alpha=0.2)
ax[1,1].plot(distSonarClean, l, 'g.', alpha=0.2)
ax[1,1].set_title('Sonar 1')

ax[1,2].plot(distance, sonar2, 'b.', alpha=0.2)
ax[1,2].plot(distSonar2Clean, sonar2Clean, 'r.', alpha=0.2)
ax[1,2].plot(distSonar2Clean, l2, 'g.', alpha=0.2)

ax[1,2].set_title('Sonar 2')

plt.show()    