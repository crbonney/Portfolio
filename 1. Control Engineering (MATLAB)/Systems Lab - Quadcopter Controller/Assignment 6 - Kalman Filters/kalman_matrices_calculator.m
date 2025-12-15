load('In_out_data')
syms t
Ts = 0.005;

% Single Integrator state-space model
A_single = [0];
B_single = [1];
C_single = [1];
D_single = [0];

% Double Integrator state-space model
A_double = [0 1; 0 0];
B_double = [0; 1]; 
C_double = [1 0];
D_double = [0];

% Calculating Discrete Dynamics
Ad_single = expm(A_single*t);
Bd_single = int(Ad_single)*B_single;
Ad_double = expm(A_double*t);
Bd_double = int(Ad_double)*B_double;

% Evalute Discrete Dynamics for t = Ts (sampling time)
A_s_single = eval(subs(Ad_single,Ts));
B_s_single = eval(subs(Bd_single,Ts));
A_s_double = eval(subs(Ad_double,Ts));
B_s_double = eval(subs(Bd_double,Ts));

% Calculate Covariances 
q_single = cov(out.In_Out_Data{1}.Values.Data); % input data
r_single = cov(out.In_Out_Data{2}.Values.Data); % output data

% don't worry about size of Q, the lqe function handle it
q_double = q_single;
r_double = r_single;

% Wiener Filter code
G_single = B_single; % noise input is same as process input
G_double = B_double;

% Gain for the Wiener filter
L_single = lqe(A_single, G_single, C_single, q_single, r_single, 0);
L_double = lqe(A_double, G_double, C_double, q_double, r_double, 0);
