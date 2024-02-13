%IR1 sensor model
clear
clc
close all

% data = csvread('calibration.csv', 1, 0);
data = [csvread('training1.csv', 1, 0); csvread('training2.csv', 1, 0)];
data = sortrows(data,3);  %sorting by range

%Extracting columns
index = data(:, 1);
time = data(:, 2);
range = data(:, 3);
v_command = data(:, 4);
raw_ir1 = data(:, 5);

%% clip data to suitable sensor range
clipI = find(range<0.3);
range = range(clipI);
raw_ir1 = raw_ir1(clipI);

%% Initial Fit

close all
invRange = 1./range;

%Fitting Hyperbolic Models to Infra red Sensors
%Model form: v = k1 + k2/r
A = [ones(length(invRange),1), invRange];  %Coefficients matrix for linear least squares

%IR1
theta = A\raw_ir1;
v = theta(1) + theta(2)*invRange;    %voltage model[V]

%range = k2/(v-k1)
ir1 = theta(2)./(raw_ir1 - theta(1));  %model distances[m]

figure
plot(range, raw_ir1,'.')
ylabel('Sensor Measurement [V]')
hold on
plot(range, v)
xlabel('Distance [m]')

%Error
error = range - ir1;

tol = 1.5;
I = find(abs(error)<tol);

rangeFilt = range(I);
errorFilt = error(I);
ir1Filt = ir1(I);
raw_ir1Filt  = raw_ir1(I);


%% mean and var
winSize = 30;
numWindows = 200;
dataLength = length(rangeFilt);
meanError = zeros(numWindows,1);
varError = zeros(numWindows,1);

% figure(4)
% hold on
j = 1;
windowI = winSize/2 : floor(dataLength/numWindows) :dataLength - winSize/2;

% i is the index of the centre of the window
for i = windowI
    
    windowRange = rangeFilt(i-winSize/2+1:i+winSize/2);
    windowError = errorFilt(i-winSize/2+1:i+winSize/2);
    
    meanError(j) = mean(windowError);
    varError(j) = var(windowError);
    
%     plot(windowRange,windowError,'.')
%     plot(rangeFilt(i),meanError(j),'+');
    
    j = j + 1;
end

%Fit Mean of Noise
p1_mean = polyfit(rangeFilt(windowI), meanError, 4);
mu_fit1 = polyval(p1_mean, rangeFilt);     %polynmial fit vector

%Fit Variance of Noise
p1_var = polyfit(rangeFilt(windowI), varError, 4);
var_fit1 = polyval(p1_var, rangeFilt);

figure
subplot(211)
hold on
plot(rangeFilt(windowI),meanError,'.')
plot(rangeFilt,mu_fit1)
ylabel('Error Mean')
hold off
subplot(212)
hold on
plot(rangeFilt(windowI),varError,'.')
plot(rangeFilt,var_fit1)
ylabel('Error Variance')
hold off
xlabel('Distance [m]')