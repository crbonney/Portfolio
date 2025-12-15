function [Self] = design_metrics(Plant,Controller,Self)
%% Purpose 
% Given a system and controller, analyze the robustness characteristics and
% produce a set of metrics and plots to describe the response.
%
% This script 
% - creates open-loop transfer functions at the input and output
% - closed loop transfer function
% - noise characteristic transfer function (U/V)
% - Return Difference and Stability Robustness min singular value plots
% - Sensitivity and Comp Sensitivity plots
% - classical stability margins (Gain/Phase Margins and crossover freqs)
% - Step response analysis (rise time, settle time, overshoot, undershoot)
%% Inputs
% Plant - A state-space model of the plant including modeled uncertainties
% Controller - A state-space model of the controller to be analyzed
% Self - A structure that stores information on the controller and plant
%% Outputs
% Self - Returns a structure containing what it stored previously, plus all
% the metrics tested

Self.Controller = Controller;
%% Create Constants for analysis

% create time vector
dt = 0.001;
t = 0:dt:2;
Self.t = t;

% create vector of frequnecies for frequency domain analysis
w = logspace(-3,3,500);
Self.w = w;
Self.metric = zeros(1,12);

%% Build Transfer Functions in state-space form
Self.sys_u = input_system(Plant,Controller);
Self.sys_y = output_system(Plant,Controller);
Self.sys_cl = cl_system(Plant,Controller);
Self.sys_v = noise_system(Plant,Controller,Self.sys_cl);

%% Build Frequency Responses
Self.Lu = squeeze(freqresp(Self.sys_u,Self.w));
Self.Ly = squeeze(freqresp(Self.sys_u,Self.w));
Self.Lv = squeeze(freqresp(Self.sys_v,Self.w));
Self.T  = squeeze(freqresp(Self.sys_cl,Self.w));
Self.S  = 1 - Self.T;


%% Actuator Response (Unused)
% Self.dele_Az    = 20*log10(abs(squeeze(Self.Lv(1,1,:))));
% Self.dele_q     = 20*log10(abs(squeeze(Self.Lv(1,3,:))));
% Self.deledot_Az = 20*log10(abs(squeeze(Self.Lv(2,1,:))));
% Self.deledot_q  = 20*log10(abs(squeeze(Self.Lv(2,3,:))));

%% Eigenvalues/vectors of closed-loop system
[Self.eig_vectors,Self.eig_values] = eig(Self.sys_cl.A);
Self.eig_values = diag(Self.eig_values);

%% Return Difference min singular values
##OCTAVE CHANGE
##Self.rd = sigma(Self.sys_u,Self.w,2);
Self.rd = sigma(1+Self.sys_u,Self.w);
Self.rd_min = min(min(abs(Self.rd)));
Self.metric(2) = Self.rd_min;

%% Stability Robustness min singular values
##OCTAVE CHANGE
##Self.sr = sigma(Self.sys_u,w,3);
Self.sr = sigma(1+inv(Self.sys_u),Self.w);
Self.sr_min = min(min(abs(Self.sr)));
Self.metric(3) = Self.sr_min;

%% Max Comp Sensitivity
Self.Tmax = 20*log10(abs(max(Self.T,[],2)));
Self.metric(11) = Self.Tmax(1);

%% Max Sensitivity 
Self.Smax = 20*log10(abs(max(Self.S,[],2)));
Self.metric(12) = Self.Smax(1);

%% Classical Stability (gain/phase margins)
##Self.classical_margins = allmargin(Self.sys_u);
##Self.LGCF = Self.classical_margins.PMFrequency(1);

% OCTAVE CHANGES
[Self.GM, Self.PM, Self.PCF, Self.LGCF] = margin(Self.sys_u);

Self.metric(4) = Self.LGCF;

%% Step response characteristics
[Self.y,~] = step(Self.sys_cl,Self.t); % step simulation of best system
% plot(t,Self.y(:,1),'r','LineWidth',1.5);

az = Self.y(:,1);
aze = abs(ones(size(az))-az);  % error for az
taur = 0.; taus= 0.; % rise time and settling time
fv = aze(numel(aze)); % final value of the error
e_n = aze - fv*ones(size(aze)) - 0.36*ones(size(aze)); %calculate time to reach 63% of final value
e_n1 = abs(e_n) + e_n;
taur = crosst(e_n1,t); % rise time 
Self.risetime = taur;
Self.metric(5) = taur;

e_n = aze - fv*ones(size(aze)) - 0.05*ones(size(aze));
e_n1 = abs(e_n) + e_n;
taus = crosst(e_n1,t); % settling time
Self.settletime = taus;
Self.metric(6) = taus;


%% Output Analysis (unused), code from Kevin Wise
% for i=1:numel(Self.w)
%     s = sqrt(-1)*Self.w(i);
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

end

