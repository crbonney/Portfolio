function [Self] = design_scp(DesignPlant, cmd_state, feedback_states, AnalysisPlant, qq, Self)
%DESIGN_SCP Summary of this function goes here
%   Detailed explanation goes here

Self.DesignPlant = DesignPlant;
Self.AnalysisPlant = AnalysisPlant;

%% build RSLQR controller
Self.RSLQR = design_lqr(AnalysisPlant, cmd_state, feedback_states, AnalysisPlant, qq, Self);


%% pick eig vectors to keep
disp('RSLQR eig values/vectors')

to_keep = [3,4,5];
F = Self.RSLQR.Aw - Self.RSLQR.Bw*Self.RSLQR.Kx;
Self.Lmda_cl = eig(F);
[Self.X_cl,~] = eig(F);
Lmda_r = Self.Lmda_cl(to_keep);
X_r = Self.X_cl(:,to_keep);
C = [eye(3) zeros(3,2)];

Ky = Self.RSLQR.Kx*X_r*inv(C*X_r);
Ky = real(Ky);

Self.Lmda_r = Lmda_r;
Self.X_r = X_r;
Self.Ky = Ky;

Self.Controller.Ac = 0;
Self.Controller.Bc1 = [1 0 0 0];
Self.Controller.Bc2 = [-1];
Self.Controller.Cc = -Ky(1);
Self.Controller.Dc1 = [-Ky(2:3) 0 0];
Self.Controller.Dc2 = 0;

Self = design_metrics(AnalysisPlant,Self.Controller,Self);
end

