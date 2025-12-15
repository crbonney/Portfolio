% Chris Bonney (April 2021)


 
%% Program Start

clear all
close all
clc

format short e

% add my set of functions to path
addpath('functions')

RSLQR.name = 'RSLQR';

%% Plant Data
% Controller Constants

Ka=-0.0015;
Kq=-0.32;
az=2;
aq=6;

% Dynamics Constants

V=886.78;
Za=-1.3046*V;
Zd=-0.2142*V;
Ma=47.7109;
Md=-104.8346;
% Actuator Constants

% omega = sqrt(12769);
% zeta = 0.6;
omega = 2.*pi*11;
zeta = sqrt(1/2);


%% Dynamics without actuator
Ap = [Za/V  1  ;
       Ma   0 ];
Bp = [Zd/V ;
       Md ];

Cp = [Za 0  ;
      0  1 ];
Dp = [Zd ;
      0 ];

RSLQR.DesignPlant = ss(Ap,Bp,Cp,Dp);

% Size of the plant model
[nx,~]=size(Ap);

%% Dynamics with Actuator
A_actuator = [0 1; -omega^2 -2*zeta*omega];
B_actuator = [0; omega^2];
Plant.Ap = [   Ap      Bp zeros(2,1); 
            zeros(2,2)  A_actuator];
Plant.Bp = [zeros(2,1); B_actuator];
Plant.Cp = [Za 0 Zd 0; 
            eye(4)];
% Plant.Cp = [Za 0 Zd 0;
%             1  0 0  0;
%             0  1 0  0];
Plant.Dp = 0*(Plant.Cp*Plant.Bp);
Ap = Plant.Ap;
Bp = Plant.Bp;
Cp = Plant.Cp;
Dp = Plant.Dp;
RSLQR.AnalysisPlant = ss(Ap,Bp,Cp,Dp);


%% Design RSLQR Controllers From HW3
RSLQR = design_lqr(RSLQR.DesignPlant,1,[2,3],RSLQR.AnalysisPlant,logspace(-6,-3,50),RSLQR);


%% Define RSLQG Parameters

Q0 = diag([ 0.001 0.0014 0.005 ]);
R0 = 1000*diag([ 0.025^2 0.001^2]);
c0 = 0.00001;
% c0 = 0.01;

vee = logspace(2,-3,3);
% vee = logspace(5,-5,3);

Aw = RSLQR.Aw;
Bw = RSLQR.Bw;
Kx = RSLQR.Kx;

Cw = [1 0 0; 
      0 0 1];
Dw = [0;0];
  
Aw_lqg = Aw;
Bw_lqg = Bw;
Cw_lqg = Cw;
Dw_lqg = Dw;

sys_1 = ss(Aw_lqg, Bw_lqg, Cw_lqg, Dw_lqg);
zz = [-10];

sys_2 = square_system_inputs_pp(sys_1,zz);
disp(['BbarMatrix z = ' num2str(zz) ])
sys_2.b
tzero(sys_2)

for ii=1:length(vee)
    RSLQG(ii) = RSLQR;
end

%% Design RSLQG Controllers

for ii=1:length(vee)
   
    RSLQG(ii).name = strcat('RSLQG, vee = ', num2str(vee(ii)));
    Qv = Q0 + c0*(vee(ii)+1)/vee(ii)*(sys_2.b*sys_2.b');
    Rv = (vee(ii)/(vee(ii)+1))*R0;
    RSLQG(ii).Qv = Qv;
    RSLQG(ii).Rv = Rv;
    Lvee = lqr(Aw',Cw',Qv,R0)';
    RSLQG(ii).Lvee = Lvee;
    
    RSLQG(ii).Controller.Ac  = [0 zeros(1,3); Lvee(:,1) Aw - Bw*Kx - Lvee*Cw];
    RSLQG(ii).Controller.Bc1 = [ 1 0 0 0 0; zeros(3,2) Lvee(:,2) zeros(3,2)];
    RSLQG(ii).Controller.Bc2 = [-1;-1; 0; 0];
    RSLQG(ii).Controller.Cc  = [0 -Kx];
    RSLQG(ii).Controller.Dc1 = [0 0 0 0 0];
    RSLQG(ii).Controller.Dc2 = [0];
    RSLQG(ii) = design_metrics(RSLQG(ii).AnalysisPlant,RSLQG(ii).Controller,RSLQG(ii));
end


%% Print Results
print_analysis(RSLQR,RSLQG(1),RSLQG(2),RSLQG(3))
% print_analysis(RSLQR,RSLQG)

%% print controller info for vee = 10^-3

Aw = RSLQG(3).Aw
C = RSLQG(3).AnalysisPlant.C
Q = RSLQG(3).Qv
R = RSLQG(3).Rv
Lvee = RSLQG(3).Lvee
Ac  = RSLQG(3).Controller.Ac
Bc1 = RSLQG(3).Controller.Bc1
Bc2 = RSLQG(3).Controller.Bc2
Cc  = RSLQG(3).Controller.Cc
Dc1 = RSLQG(3).Controller.Dc1
Dc2 = RSLQG(3).Controller.Dc2


%%
save('RSLQG_design.mat','RSLQG');