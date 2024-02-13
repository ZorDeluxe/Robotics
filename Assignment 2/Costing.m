% ENMT482 Time and Motion Study
% Author: Zoren Dela Cruz

clc, clear all, close all;

%------------------------------- Constants -------------------------------%
xArray = linspace(0,1,13);
months = [0:1:12];

%----------------------------- Robot Costing -----------------------------%
robotCost = 40000;                      % Cost of UR5
robotTools = 5000;                      % Cost of Tools
robotMaintenance = 400;                 % Annual maitenance 

% Fixed Cost
robotFC = robotCost + robotTools;

% Variable Cost 
robotVC = robotMaintenance;

% Total Cost 
robotTC = robotVC*xArray + robotFC;

%----------------------------- Robot Profit ------------------------------%
secondsInADay = 8 * 60 * 60;            % Seconds
costOfCoffee = 4.50;                    % Profit cost

% Coffee Speeds
cupOfCoffee0 = secondsInADay / 600;
cupOfCoffee1 = secondsInADay / 540;
cupOfCoffee2 = secondsInADay / 480;
cupOfCoffee3 = secondsInADay / 420;

% Total Revenue with change of speeds
TR0 = cupOfCoffee0 * costOfCoffee * 365 * xArray;
TR1 = cupOfCoffee1 * costOfCoffee * 365 * xArray;
TR2 = cupOfCoffee2 * costOfCoffee * 365 * xArray;
TR3 = cupOfCoffee3 * costOfCoffee * 365 * xArray;



%------------------------------- Plotting --------------------------------%
figure(1)
plot(months, TR0 /1000, 'linewidth', 2);
hold on 
plot(months, TR1 /1000, 'linewidth', 2);
plot(months, TR2 /1000, 'linewidth', 2);
plot(months, TR3 /1000, 'linewidth', 2);
plot(months, robotTC / 1000, 'linewidth', 2, 'color', 'k');
hold off

% Text
txt = {'Total Cost'};
text(1,60,txt)
txt = {'Total Revenues'};
text(9,125,txt)
annotation('arrow', [0.6 0.5], [0.17 0.23])
txt = {'Breakevens (Intersection Points)'};
text(6,15,txt);


% Legends
[leg,att] = legendflex(gca, {'10 mins', '9 mins', '8 mins', '7 mins'}, 'anchor', {'nw', 'nw'}, ...
    'buffer', [10, -10], 'title', 'Coffee Time');
set(findall(leg, 'string', 'Coffee Time'), 'fontweight', 'bold');
leg.Title.Visible = 'on';

% Limits
ylim([0, 300]);
xlim([0, 12]);

% Labels
title('Cost Volume Profit Graph')
xlabel('Months')
ylabel('Dollars in Thousands')

% Grids 
grid on
grid minor









