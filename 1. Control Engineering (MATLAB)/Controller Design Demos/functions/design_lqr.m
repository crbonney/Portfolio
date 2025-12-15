function [Self] = design_lqr(DesignPlant, cmd_state, feedback_states, AnalysisPlant, qq, Self)
%% Purpose:
% to pick gains of and build a control law in common-controller form of a
% robust servo LQR controller. It tests different Q matrices by scaling by
% a factor of qq, and picks the best by selecting the one with the minimum
% difference between Return Difference and Stability Robustness min
% singular values (which give the best gain/phase margins)
% it also analyzes the system's robustness using the design_metrics
% function
%% Inputs:
% DesignPlant - state-space model of the system used to design a
% controller
% 
% cmd_state - the state that is being commanded
% feedback_states - states that can be used for feedback
% AnalysisPlant - state-space model of the system used for analysis of the
% control design
%
% qq - an array of values to sweep to scale the Q matrix when optimizing
% the gain margins
% Self - a structure containing information about the system, controller
% design, and stability/robustness metrics
%% Outputs: 
% Self - same as above

% make sure DesignPlant and AnalysisPlant are included in the output
Self.DesignPlant = DesignPlant;
Self.AnalysisPlant = AnalysisPlant;
Self.qq = qq;

%% Build system matrix that includes the robust servo integrator
Ccmd = DesignPlant.C(cmd_state,:);
Dcmd = DesignPlant.D(cmd_state,:);
Self.Aw = [zeros(1,1)      Ccmd      ; 
           zeros(size(DesignPlant.A,1),1)  DesignPlant.A];
Self.Bw = [Dcmd;   DesignPlant.B];


  %% Make LQR Controllers and analyze
Q = zeros(size(Self.Aw)); %shape of Aw
R = 1;
% qq = logspace(-0,8,50); %only penalize first element (error)
Kx_lqr = zeros([length(qq),size(Self.Aw,1)]);

Q(1,1) = 1e-4;
H = [Self.Aw, -Self.Bw*Self.Bw'; Q, -Self.Aw']

% empty arrays to store metrics of different LQR designs
rd_min_ii = zeros(1,length(qq)); % min return difference singular value
sr_min_ii = zeros(1,length(qq)); % min stability robustness singular value
wc_ii = zeros(1,length(qq)); % phase crossover frequnecy

% solve for the gains of all the LQR controllers
for i=1:length(qq)
    Q(1,1) = qq(i);
    Kx_lqr(i,:) = lqr(Self.Aw,Self.Bw,Q,R);
end

ny_analysis = size(AnalysisPlant.C,1);
ny_design = size(DesignPlant.C,1);

%% Iterate through each controller and analyze metrics
for itr=1:length(qq)
    Kx = Kx_lqr(itr,:);

    % Build Controller in Classical Form
    Ctrl.Ac = 0;
%     Ctrl.Bc1 = [1 0 0 0 0];
    Ctrl.Bc1 = zeros(1,ny_analysis);
    Ctrl.Bc1(cmd_state) = 1;
    Ctrl.Bc2 = [-1];
    Ctrl.Cc = -Kx(1);
%     Ctrl.Dc1 = [0 -Kx(2:3) 0 0];
    Ctrl.Dc1 = zeros(1,ny_analysis);
    Ctrl.Dc1(feedback_states) = -Kx(2:size(Self.Aw,1));
    Ctrl.Dc2 = 0;

    % build closed-loop system
    sys_cl = cl_system(AnalysisPlant,Ctrl);

    % confirm closed-loop system is stable
    if (max(real(eig(sys_cl.A))) > 0) %unstable controller
        disp("unstable: ");
        fdisp (stdout, qq(itr));
        disp(eig(sys_cl.A));
      continue;
    end
    
    % analyze design
    Design = design_metrics(AnalysisPlant,Ctrl);
    design_ii(itr) = Design;
    rd_min_ii(itr) = Design.rd_min;
    sr_min_ii(itr) = Design.sr_min;
    wc_ii(itr) = Design.LGCF;

end

assert(exist('design_ii','var') == true,'Could not find a stable controller design.');


% pick design that has the smallest difference between RD and SR min
% singular values
[~,best_ii] = min(abs(rd_min_ii-sr_min_ii));

Kx = Kx_lqr(best_ii,:);

% Build Controller in Classical Form
    Ctrl.Ac = 0;
%     Ctrl.Bc1 = [1 0 0 0 0];
    Ctrl.Bc1 = zeros(1,ny_analysis);
    Ctrl.Bc1(1) = 1;
    Ctrl.Bc2 = [-1];
    Ctrl.Cc = -Kx(1);
%     Ctrl.Dc1 = [0 -Kx(2:3) 0 0];
    Ctrl.Dc1 = zeros(1,ny_analysis);
%     Ctrl.Dc1(1:ny_design) = -Kx(2:size(Self.Aw,1));
    Ctrl.Dc1(feedback_states) = -Kx(2:size(Self.Aw,1));
    Ctrl.Dc2 = 0;

%% Return design analsis, and all the controllers tested
Self.Controller = Ctrl; % classical controller form of picked design
Self.Design_data = design_ii; % analysis of all controllers
Self = design_metrics(AnalysisPlant,Self.Controller,Self); %metrics
Self.best_ii = best_ii;
Self.best_qq = qq(best_ii);
Q(1,1) = Self.best_qq;
Self.Q = Q; % picked Q matrix
Self.R = R; % picked R matrix
Self.Kx = Kx; %picked state-feedback gains



end

