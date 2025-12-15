

%% run simulation
% simulation = sim('hamiltonian_data_collector');
simout = PhysicalData;
%% extract data from simout structure
t     = simout.time;
q1    = simout.signals.values(:,1);
q2    = simout.signals.values(:,2);
q1dot = simout.signals.values(:,3);
q2dot = simout.signals.values(:,4);
v     = simout.signals.values(:,5);

%% get init states
t_init     = t(1);
q1_init    = q1(1);
q2_init    = q2(1);
q1dot_init = q1dot(1);
q2dot_init = q1dot(1);
v_init     = v(1);

%% constants
% Ts = 0.001;
% Ra = 2.6;
% kt = 0.00768;
% kr = 70;
g = 9.80665;

%% integral from (t0,tn) v*q1dot
d = cumtrapz(t,v.*q1dot);
d = d(2:end);

%% get init conditions
h1_init = 1/2*q1dot_init.^2;
h2_init = 1/2*sin(q2_init).^2.*q1dot_init.^2 + 1/2*q2dot_init.^2;
h3_init = cos(q2_init).*q1dot_init.*q2dot_init;
h4_init = g*cos(q2_init);

%% hbar equations to integrate
h1 = 1/2*q1dot.^2 - h1_init;
h2 = 1/2*sin(q2).^2.*q1dot.^2 + 1/2*q2dot.^2 - h2_init;
h3 = cos(q2).*q1dot.*q2dot - h3_init;
h4 = g*cos(q2) - h4_init;

Hbar = [h1 h2 h3 h4];
Hbar = Hbar(2:end,:);

%% get Fbar equations
Fbar = [cumtrapz(t,q1dot.^2) cumtrapz(t,q2dot.^2)];
Fbar = Fbar(2:end,:);

%% concatenate to get A
A = [Hbar Fbar];

%% pseudo-inverse A to solve
Ainv = pinv(A);
theta = Ainv*d;

%% multiply theta1,...,theta4 to get form of originals
% K = Ra/(kt*kr);
% Kdiag = diag([K K K K 1 1]);
% 
% % final output
% theta = Kdiag*theta;

