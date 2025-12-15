% Calculating UAV Coefficients and Plotting Thrust, Power, Moment curves
close all; 

%% Prop Data Analysis and Plots of C_T, C_P
% PROP DATA: https://commons.erau.edu/cgi/viewcontent.cgi?article=2057&context=publication
RPMs = [11000 19000 23000 25000 27000 29000];
C_thrust = [0.079 0.083 0.088 0.09 0.092 0.093];
C_power = [0.041 0.041 0.041 0.041 0.041 0.041];
prop_dia = 0.066; %meters

% UAV DATA: parrot.com/global/drones/parrot-mambo-fly
UAV_mass = 0.068; %kg
prop_dist = sqrt(2)*0.09; %meters
prop_mass = 0.001; %kg (1 gram)

% PHYSICAL CONSTANTS 
rho = 1.22495; % kg/m3
ns = RPMs/60; %Hz
g = 9.81; %m/s2

% used for linear regression of prop data
X = [ones(1,length(ns))' ns'];

% coefficients in linear fit of coef thrust/power curves
C_thrust_lin = X\C_thrust';
C_power_lin = X\C_power';

%eq'n for coef of thrust/power
C_thrust_eq = @(C_T, n) [(C_T(1)+C_T(2)*n)];
C_power_eq = @(C_P, n) [(C_P(1)+C_P(2)*n)];

%to plot coefficient of thrust/power curves
n = [0:10:500]; %Hz
C_thrust_curve = C_thrust_eq(C_thrust_lin, n);
C_power_curve = C_power_eq(C_power_lin, n);

figure; %figure 1: C_T and C_P vs Hz
subplot(2,1,1); %sublpot 1.1: C_T vs Hz
plot(ns, C_thrust, 'bo');
hold on;
plot(n, C_thrust_curve);
xlim([0 600]);
ylim([0.05 0.1]);
xlabel('n (Hz)');
ylabel('C_T');
title('C_{Thrust} vs Propeller Speed in Hz');
legend({'Prop Data', 'Linear Fit'},'Location','Best');
grid on;

subplot(2,1,2); %subplot 1.2: C_P vs Hz
plot(ns, C_power, 'bo');
hold on;
plot(n, C_power_curve);
xlim([0 600]);
ylim([0 0.05]);
xlabel('n (Hz)');
ylabel('C_P');
title('C_{Power} vs Propeller Data in Hz');
legend({'Prop Data', 'Linear Fit'},'Location','Best');
grid on;

%% Plotting Thrust and Power equations and Plots

%define eq'ns for prop power and thrust ; from class presentation
prop_power_eq =  @(C_P, n) [C_power_eq(C_P,n).*(n.^3)*rho*(prop_dia^5)];
prop_thrust_eq = @(C_T, n) [C_thrust_eq(C_T,n).*(n.^2)*rho*(prop_dia^4)];

%calculate curve to plot
prop_yaw_moment_n = prop_power_eq(C_power_lin,n)./(n*2*pi);

figure; %figure 2: Yaw and Pitch/Roll moments vs Prop speed
subplot(2,1,1); %subplot 2.1: Yaw moment in N-m vs prop speed in Hz
plot(n,prop_yaw_moment_n);
%xlim([0 500]);
% ylim([0 0.05]);
xlabel('n (Hz)');
ylabel('yaw moment (N-m)');
title('Prop Yaw Moment vs revolutions in Hz');
grid on;
% legend({'Prop Data', 'Linear Fit'},'Location','Best');

%% Thrust Moment Calculations and Plots

%calculate pitch/roll moment as thrust(force)*dist from CM
prop_pitch_moment_n = prop_thrust_eq(C_thrust_lin,n).*prop_dist;

subplot(2,1,2); %subplot 2.2: pitch/roll moments in N-m vs prop speed in Hz
plot(n,prop_pitch_moment_n);
%xlim([0 500]);
% ylim([0 0.05]);
xlabel('n (Hz)');
ylabel('moment (N-m)');
title('Prop Pitch/Roll Moment vs revolutions in Hz');
grid on;
% legend({'Prop Data', 'Linear Fit'},'Location','Best');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%2.1.3%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%I_rod = 1/12*L^2*M ; derived in notes
prop_mass_moment = 1/12*(prop_dia^2)*prop_mass;
% RESULT: 1.2705e-06 N-m

%parallel axis thrm to translate it to UAV CM:
prop_mass_moment_uav = prop_mass_moment + prop_mass*(prop_dist^2);
% RESULT: 5.79705e-05 N-m

%% Calculating Trim Thrust

%total prop thrust = 4*prop_thrust
%assumption: at trim all props are at same speed
%want to set total thrust to be 1g*UAV_mass Newtons
syms x
n_trim_speed = vpa(solve([4*prop_thrust_eq(C_thrust_lin,x)==g*UAV_mass; x>1]))
% RESULT: n = 293 Hz

%ALSO CAN USE fsolve for a function's 0's

%acceleration of UAV from 4 props and gravity at n Hz
% vertical_acceleration_curve = 4*prop_thrust_eq(C_thrust_lin,n)/(UAV_mass)-g;
vertical_acceleration_curve = prop_thrust_eq(C_thrust_lin,n);

figure; %figure 3: UAV acceleration curve (g's) vs prop speed
plot(n,vertical_acceleration_curve);
xlabel('n (Hz)');
ylabel('UAV acceleration (m/s^2)');
title('UAV Vertical Acceleration ((thrust/mass) - g) vs Prop Speed');
grid on;
