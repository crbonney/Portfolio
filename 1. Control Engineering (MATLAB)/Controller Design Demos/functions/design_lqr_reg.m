function [Self] = design_lqr_reg(DesignPlant, cmd_state, feedback_states, AnalysisPlant, qq, Self)
%% Purpose:
% to pick gains of and build a control law in common-controller form of a
% LQR controller. It tests different Q matrices by scaling by
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

Self.DesignPlant = DesignPlant;
Self.AnalysisPlant = AnalysisPlant;

Ccmd = DesignPlant.C(cmd_state,:);
Dcmd = DesignPlant.D(cmd_state,:);
Self.Aw = [zeros(1,1)      Ccmd      ; 
           zeros(size(DesignPlant.A,1),1)  DesignPlant.A];
Self.Bw = [Dcmd;   DesignPlant.B];
Self.Aw = DesignPlant.A;
Self.Bw = DesignPlant.B;


%% Make LQR Controllers and analyze
Q = zeros(size(Self.Aw)); %shape of Aw
R = 1;
% qq = logspace(-0,8,50); %only penalize first element (error)
Kx_lqr = zeros([length(qq),size(Self.Aw,1)]);

rd_min_ii = zeros(1,length(qq));
sr_min_ii = zeros(1,length(qq));
wc_ii = zeros(1,length(qq));

% figure('Name','LQR Step Sim');
% hold on
% grid on


for i=1:length(qq)
    Q(1,1) = qq(i);
    Kx_lqr(i,:) = lqr(Self.Aw,Self.Bw,Q,R);
end

ny_analysis = size(AnalysisPlant.C,1);
ny_design = size(DesignPlant.C,1);
%% Iterate through each controller and perform step function
for itr=1:length(qq)
    Kx = Kx_lqr(itr,:);

    % Build Controller in Classical Form
    Ctrl.Ac = 0;
%     Ctrl.Bc1 = [1 0 0 0 0];
    Ctrl.Bc1 = zeros(1,ny_analysis);
    Ctrl.Bc2 = [0];
    Ctrl.Cc = [0];
%     Ctrl.Dc1 = [0 -Kx(2:3) 0 0];
    Ctrl.Dc1 = zeros(1,ny_analysis);
    Ctrl.Dc1(feedback_states) = -Kx(1:size(Self.Aw,1));
    Ctrl.Dc2 = 0;

    sys_cl = cl_system(AnalysisPlant,Ctrl);

    if (max(real(eig(sys_cl.A))) > 0) %unstable controller
      continue;
    end
    
    
    Design = design_metrics(AnalysisPlant,Ctrl);
    design_ii(itr) = Design;
    rd_min_ii(itr) = Design.rd_min;
    sr_min_ii(itr) = Design.sr_min;
    wc_ii(itr) = Design.LGCF;

%     [y,~] = step(Design.sys_cl,Design.t);
%     plot(Design.t,y(:,cmd_state))
%     hold on
end

[~,best_ii] = min(abs(rd_min_ii-sr_min_ii));

Kx = Kx_lqr(best_ii,:);


% Build Controller in Classical Form
    Ctrl.Ac = 0;
%     Ctrl.Bc1 = [1 0 0 0 0];
    Ctrl.Bc1 = zeros(1,ny_analysis);
    Ctrl.Bc2 = [0];
    Ctrl.Cc = [0];
%     Ctrl.Dc1 = [0 -Kx(2:3) 0 0];
    Ctrl.Dc1 = zeros(1,ny_analysis);
    %     Ctrl.Dc1(1:ny_design) = -Kx(2:size(Self.Aw,1));
    Ctrl.Dc1(feedback_states) = -Kx(1:size(Self.Aw,1));
    Ctrl.Dc2 = 0;


Self.Controller = Ctrl;
Self.Design_data = design_ii;
Self = design_metrics(AnalysisPlant,Self.Controller,Self);
Self.qq = qq;
Self.best_ii = best_ii;
Self.best_qq = qq(best_ii);
Q(1,1) = Self.best_qq;
Self.Q = Q;
Self.R = R;
Self.Kx = Kx;



end

