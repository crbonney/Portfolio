% Chris Bonney (March 2021)


 
%% Program Start

clear all
close all
clc

format short e

% add my set of functions to path
addpath('functions')

SCP.name = 'SCP';

%% Plant Data
Za_V = -1.3046;
Ma   = 47.711; % Positve Ma = unstable aircraft
Zd_V = -.2142;
Md   = -104.83;
V    = 886.78; % (fps)
Za   = V*Za_V;
Zd   = V*Zd_V;
w_act = 2.*pi*11; % actuator natural frequency rps
z_act = 0.707;    % actuator damping

grav = 32.174; % (fps2)

% Size of the plant model
% [nx,~]=size(Ap);

Plant.Ap = [Za/V   Za       0            Zd     ;
            Ma/Za  0  (Md-Ma*Zd/Za)      0      ;
              0    0        0            1      ;
              0    0    -w_act^2  -2*z_act*w_act];

% Input is delcmd (rad)
Plant.Bp = [0.; 0.; 0.; w_act*w_act ];

% Outputs are Az (fps2), AOA (rad), pitch rate (rps), dele (rad), deledot (rps)
Plant.Cp = eye(4);
Plant.Dp = 0.*Plant.Cp*Plant.Bp;
% Plant.Cp = [Za 0 Zd 0;
%             1  0 0  0;
%             0  1 0  0];
Plant.Dp = 0*(Plant.Cp*Plant.Bp);
Ap = Plant.Ap;
Bp = Plant.Bp;
Cp = Plant.Cp;
Dp = Plant.Dp;

SCP.AnalysisPlant = ss(Ap,Bp,Cp,Dp);

SCP = design_scp(SCP.AnalysisPlant,1,[1,2,3,4],SCP.AnalysisPlant,logspace(-6,-3,50),SCP);

% AZ TIME HISTORIES OF LQR CONTROLLERS
figure('Name','LQR Time Histories')
hold on
% for itr = 1:length(SCP.Design_data)
%     plot(SCP.t,SCP.Design_data(itr).y(:,1))
% end
best_plot = plot(SCP.t,SCP.y(:,1),'r','LineWidth',2);
xlabel('time (sec)');
ylabel('Az (fps2)');
legend(best_plot,'SCP Az','Location','best');
title('LQR Time Histories');

% rd_min_ii = [SCP.Design_data(:).rd_min];
% sr_min_ii = [SCP.Design_data(:).sr_min];
% wc_ii = [SCP.Design_data(:).LGCF];
% 
% figure('Name','LQR Controllers Min RD, Min SR');
% hold on
% plot(wc_ii,rd_min_ii,'r','LineWidth',2)
% plot(wc_ii,sr_min_ii,'b','LineWidth',2)
% plot(SCP.LGCF,SCP.rd_min,'ko','MarkerSize',10,'LineWidth',2)
% 
% grid on
% xlabel('wc (rps)');
% ylabel('min RD, min SR');
% legend(['Min RD SV'],['Min SR SV'],['Cross Point']);
% 
% figure('Name','LQR design LGCFs')
% semilogy(wc_ii,SCP.qq,'LineWidth',2);
% grid on
% xlabel('wc (rps)');
% ylabel('qq');
% title('LQR design LGCFs');

%% Output Analysis
% for i=1:numel(RSLQR.w)
%     s = sqrt(-1)*RSLQR.w(i);
%     Lout = Cout*inv(s*eye(size(Aout))-Aout)*Bout+Dout;
%     % This loops computes SISO freq response at plant output one loop open,
%     % rest closed
%     for jj = 1:nCp
%         Fyjj = eye(nCp);
%         Fyjj(jj,jj) = 0.;
%         Tyjj = inv(eye(nCp) + Lout*Fyjj)*Lout;
%         Tyj(jj,i) = Tyjj(jj,jj);
%     end
% end
% for jj=1:nCp
%     v_min(jj) = min(min(abs(1.+Tyj(jj,:))));
% end

%% print analysis

print_analysis(SCP);

%%
save('SCP_design.mat','SCP');