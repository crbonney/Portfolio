
%% Bang-Bang Throttle
%load in data
load('systemID_data_zip/bang_bang_T/motor_speed_dataT.mat');
load('systemID_data_zip/bang_bang_T/sensor_dataT.mat');
load('systemID_data_zip/bang_bang_T/sensor_state_dataT.mat');
load('systemID_data_zip/bang_bang_T/state_est_dataT.mat');

dT = 0.005;
MotorMix = [...%T  E  A  R
                1  1  1 -1 ;... %n1  T+ E+ A+ R-
                1  1 -1  1 ;... %n2  T+ E+ A- R+
                1 -1 -1 -1 ;... %n3  T+ E- A- R-
                1 -1  1  1 ;... %n4  T+ E- A+ R+
]';

%correct negative motor speeds
motor_correction = diag([1 -1 1 -1]);
motor_speed_data = motor_speed_data*motor_correction;

% get Throttle
TEAR = motor_speed_data/MotorMix;
T = TEAR(:,1);

% T = motor_speed_data*[ 1; -1;  1; -1]/4;
% E = motor_speed_data*[ 1; -1; -1;  1]/4;
% A = motor_speed_data*[ 1;  1; -1; -1]/4;
% R = motor_speed_data*[-1; -1; -1; -1]/4;

%get states
z  = state_est_data(:,4);
w  = state_est_data(:,10);
az = sensor_data(:,3);
time = state_est_data(:,1);

%correct data
bang_bang_start_t = 200;  %start of bang bang
bang_bang_end_t = 400;    %end of bang bang
T_trim = 303;           %trim offset
delay = 7;              %time delay from actuator
w = detrend(w);         %correct for w offset from pre bang bang dynamics


%create system to solve using backwards euler
% wdot = b*w + c*T
% w(i+1) = wdot*dT + w(i)
% w(i+1) = [w(i) T(i)]*[(1+b*dT); c*dT];
phi = [w(bang_bang_start_t+delay:bang_bang_end_t-1+delay), (T(bang_bang_start_t:bang_bang_end_t-1)-T_trim)];
W   = [w(bang_bang_start_t+1+delay:bang_bang_end_t+delay)];
%solve for system parameters
C = phi\W;
bt = (C(1)-1)/dT; %damping term on w
ct = C(2)/dT;     %more accurate coefficient for Throttle

ct = T\az;
bt = 0;
%%%% check that delay correction is accurate
% figure;
% plotyy(1:length(W),phi(:,1),1:length(W),phi(:,2));


%% Elevator Bang Bang

% Load in data
load('systemID_data_zip\bang_bang_E\state_est_dataE.mat')
load('systemID_data_zip\bang_bang_E\motor_speed_dataE.mat')
load('systemID_data_zip\bang_bang_E\sensor_dataE.mat')

%correct data
bang_bang_start_e = 200;  %start of bang bang
bang_bang_end_e = 330;    %end of bang bang
q = state_est_data(:,12);
q = q - q(bang_bang_start_e);         %correct for qw offset from pre bang bang dynamics

%correct negative motor speeds
motor_correction = diag([1 -1 1 -1]);
motor_speed_data = motor_speed_data*motor_correction;

% get Elevator
TEAR = motor_speed_data/MotorMix;
E = TEAR(:,2);
E_trim = 7.5;
%qdot = b*q + c*E
%q(i+1) = [q(i) E(i)]*[(1+b*dT) c*dT];
phi = [q(bang_bang_start_e+delay:bang_bang_end_e-1+delay), (E(bang_bang_start_e:bang_bang_end_e-1)-E_trim)];
Q   = [q(bang_bang_start_e+1+delay:bang_bang_end_e+delay)];
%solve for system parameters
% C = phi\Q;
% be = (C(1)-1)/dT; %damping term on w
% ce = C(2)/dT;     %more accurate coefficient for Throttle
%q(i+1)-q(i) = c*E*dT
Q = [q(bang_bang_start_e+1+delay:bang_bang_end_e+delay)-q(bang_bang_start_e+delay:bang_bang_end_e-1+delay)]/dT;
ce = (E(bang_bang_start_e:bang_bang_end_e-1)-E_trim)\Q;
be = 0;

%% Aileron Bang Bang

% Load in data
load('systemID_data_zip\bang_bang_A\state_est_dataA.mat')
load('systemID_data_zip\bang_bang_A\motor_speed_dataA.mat')
load('systemID_data_zip\bang_bang_A\sensor_dataA.mat')

%correct data
bang_bang_start_a = 200;  %start of bang bang
bang_bang_end_a = 320;    %end of bang bang
p = state_est_data(:,11);
p = p - p(bang_bang_start_a);         %correct for p offset from pre bang bang dynamics

%correct negative motor speeds
motor_correction = diag([1 -1 1 -1]);
motor_speed_data = motor_speed_data*motor_correction;

% get Aileron
TEAR = motor_speed_data/MotorMix;
A = TEAR(:,3);
A_trim = -.25;

%p(i+1)-p(i) = c*A*dT
P = [p(bang_bang_start_a+1+delay:bang_bang_end_a+delay)-p(bang_bang_start_a+delay:bang_bang_end_a-1+delay)]/dT;
ca = (A(bang_bang_start_a:bang_bang_end_a-1)-A_trim)\P;
ba = 0;




%% Rudder Bang Bang

% Load in data
load('systemID_data_zip\bang_bang_R\state_est_dataR.mat')
load('systemID_data_zip\bang_bang_R\motor_speed_dataR.mat')
load('systemID_data_zip\bang_bang_R\sensor_dataR.mat')

%correct data
bang_bang_start_r = 200;  %start of bang bang
bang_bang_end_r = 400;    %end of bang bang
r = state_est_data(:,13);
r = r - r(bang_bang_start_r);         %correct for r offset from pre bang bang dynamics

%correct negative motor speeds
motor_correction = diag([1 -1 1 -1]);
motor_speed_data = motor_speed_data*motor_correction;

% get Rudder
TEAR = motor_speed_data/MotorMix;
Rudder = TEAR(:,4);
R_trim = 4.4;

%r(i+1)-r(i) = c*R*dT
R = [r(bang_bang_start_r+1+delay:bang_bang_end_r+delay)-r(bang_bang_start_r+delay:bang_bang_end_r-1+delay)]/dT;
cr = (Rudder(bang_bang_start_r:bang_bang_end_r-1)-R_trim)\R;
br = 0;






%% Throttle Chirp (Actuator Dynamics)
% 
% %load in data
% % load('log_chirp_data/log_chirp_50Hz.mat');
% 
% motor_speed_data = motor_speed_data*motor_correction;
% 
% % get Throttle
% TEAR = motor_speed_data/MotorMix;
% T_trim = 301.5;
% T_cmd = TEAR(:,1)-T_trim;
% 

% T_act = (b*w-az)/c;

%% (2) Finding motor transfer function
load('log_chirp_data\log_chirp_50Hz.mat')

% constants
b = bt;  % b_T
c = -ct; % c_T
deltaT = 0.005;
chirp_start = 2000;
chirp_end = 4000;
delay = 7; %samples

% Detrending w
w = state_est_data(:,10);
w_corrected = detrend(w);
w_transp = w_corrected';
w_iplus1 = w_corrected(chirp_start+1+delay:chirp_end);
w_i = w_corrected(chirp_start+delay:chirp_end-1);


% Equation I'm using is az = b*w + T*c
% Solve for T = (az-b*w)/c
time = state_est_data(:,1);
time_i = time(chirp_start:chirp_end-1-delay);

bcinv = pinv([b c]);
az = sensor_data(:,3);
az_corrected = detrend(az);
az_i = az_corrected(chirp_start+delay:chirp_end-1);

T_i = (az_i-b*w_i)/c;


% az_i_transp = az_i';
% wT_transp = bcinv*az_i_transp;
% %wT_transp = bcinv*(w_iplus1-w_i)/deltaT;
% wT = wT_transp';
% T = wT(:,2);


% Adding EAR to T
zero_row_size = size(T_i);
zero_row_size = zero_row_size(1);
TEAR = [T_i zeros(zero_row_size,3)];

% Converting from TEAR to n1,...,n4
TEAR_tran = TEAR';
motorspeeds_tran = MotorMix*TEAR_tran;
motorspeeds = motorspeeds_tran'; 
n1 = motorspeeds(:,1); % n_a

chirp_transp = chirp_data(chirp_start: chirp_end-1-delay); 
chirp = chirp_transp'; % n_c

% converting to double
n_a = T_i;
n_c = chirp;
n_a = double(n_a);
n_c = double(n_c);

% Obtaining bode plot
obj=iddata(n_a, n_c, deltaT);
sys=tfest(obj,1);
figure
bode(sys);

% figures

figure
plot(time_i, T_i, time_i, chirp);
xlabel('time (s)');
ylabel('Amplitude (Hz)');
title('Commanded motor speed (chirp signal) and actual motor speed over time');
legend('n_a', 'n_c');


% figure
% plot(w_corrected);
% legend('w detrended');

%figure
%plotyy((1:signallength), motorspeed1, (1:signallength), chirp);
%legend('n_a', 'n_c');

%figure
%plot(chirp_data(:,1));
%figure
%plot(time, motor_speed_data);



