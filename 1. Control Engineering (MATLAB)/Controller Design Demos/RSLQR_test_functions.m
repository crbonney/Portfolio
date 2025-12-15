% Chris Bonney (March 2021)


 
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
Plant.Dp = 0*(Plant.Cp*Plant.Bp);


Ap = Plant.Ap;
Bp = Plant.Bp;
Cp = Plant.Cp;
Dp = Plant.Dp;
RSLQR.AnalysisPlant = ss(Ap,Bp,Cp,Dp);

%% Design RSLQR controller
% paramaters: 
% controller model, cmd state, feedback states, analysis model, ...
% vector of values for qq, and the system structure
RSLQR = design_lqr(RSLQR.DesignPlant,1,[2,3],RSLQR.AnalysisPlant,logspace(-6,-3,50),RSLQR);

figure
bode(RSLQR.sys_u,RSLQR.w);

% AZ TIME HISTORIES OF LQR CONTROLLERS
figure('Name','LQR Time Histories')
hold on
for itr = 1:length(RSLQR.Design_data)
    plot(RSLQR.t,RSLQR.Design_data(itr).y(:,1))
end
best_plot = plot(RSLQR.t,RSLQR.y(:,1),'r','LineWidth',2);
xlabel('time (sec)');
ylabel('Az (fps2)');
legend(best_plot,'Best RSLQR','Location','best');
title('LQR Time Histories');

rd_min_ii = [RSLQR.Design_data(:).rd_min];
sr_min_ii = [RSLQR.Design_data(:).sr_min];
wc_ii = [RSLQR.Design_data(:).LGCF];

figure('Name','LQR Controllers Min RD, Min SR');
hold on
plot(wc_ii,rd_min_ii,'r','LineWidth',2)
plot(wc_ii,sr_min_ii,'b','LineWidth',2)
plot(RSLQR.LGCF,RSLQR.rd_min,'ko','MarkerSize',10,'LineWidth',2)

grid on
xlabel('wc (rps)');
ylabel('min RD, min SR');
legend(['Min RD SV'],['Min SR SV'],['Cross Point']);

figure('Name','LQR design LGCFs')
semilogy(wc_ii,RSLQR.qq,'LineWidth',2);
hold on
semilogy(RSLQR.LGCF,RSLQR.best_qq,'ko','MarkerSize',10,'LineWidth',2)

grid on
xlabel('wc (rps)');
ylabel('qq');
title('LQR design LGCFs');

%% print analysis
% paramaters: any number of plant+controller structures
% makes plots and prints controller + system properties
print_analysis(RSLQR);

%% small gain thrm

M = -RSLQR.Lu./(1+RSLQR.Lu);
RSLQR.M = M;
w = RSLQR.w;
figure('Name', 'small gain thrm')
semilogx(w,20*log10(abs(squeeze(1./M))),'k','LineWidth',2)
hold on

delta = omega^2./(omega^2+2*zeta.*omega.*w*1i+(w*1i).^2) - 1;
semilogx(w,20*log10(abs(delta)),'r','LineWidth',2)
legend('sgm(1/M)','\Delta = actuator - 1','Location','best')

%% list controller matrices

Q = RSLQR.Q
R = RSLQR.R

Aw = RSLQR.Aw
Bw = RSLQR.Bw

Ac  = RSLQR.Controller.Ac
Bc1 = RSLQR.Controller.Bc1
Bc2 = RSLQR.Controller.Bc2
Cc  = RSLQR.Controller.Cc
Dc1 = RSLQR.Controller.Dc1
Dc2 = RSLQR.Controller.Dc2


%%
save('RSLQR_design.mat','RSLQR');