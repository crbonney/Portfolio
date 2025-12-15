close all;

TEAR = [100;0;0;0]; 
Run_model('Thrust', [1 1 0 0], [1 0 0 1]);

TEAR = [0;0.3;0;0]; 
Run_model('Elevator', [1 1 1 1], [1 1 1 1]);

TEAR = [0;0;0.2;0]; 
Run_model('Aileron', [1 1 1 1], [1 1 1 1]);

TEAR = [0;0;0;20]; 
Run_model('Rudder', [1 1 1 1], [1 0 0 1]);

% not used in report
% TEAR = [0;0.3;0.2;0]; 
% Run_model('Elevator and Aileron', [1 1 1 1], [1 1 1 1]);
