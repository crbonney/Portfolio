
%% Declare Symbolics
syms q1 q2 q3 real
syms q1dot q2dot q3dot real
syms L1 L2 L3 real 
syms m1 m2 m3 real
syms Ixx1 Ixx2 Ixx3 real
syms Iyy1 Iyy2 Iyy3 real
syms Izz1 Izz2 Izz3 real
% syms m1 m2 m3 real

q = [q1; q2; q3];
qdot = [q1dot; q2dot; q3dot];
mm = [m1 m2 m3];
LL = [L1 L2 L3];

mm_actual = [20 15 10]; %kg
LL_actual = [4 3 2]; %meters
Ic1 = diag([Ixx1,Iyy1,Izz1]);
Ic2 = diag([Ixx2,Iyy2,Izz2]);
Ic3 = diag([Ixx3,Iyy3,Izz3]);
Izz_all = [Izz1 Izz2 Izz3];
Izz_actual = [0.5 0.2 0.1];

T12 = [...
       [cos(q2)  -sin(q2)  0  L1];...
       [sin(q2)   cos(q2)  0  0 ];...
       [  0         0      1  0 ];...
       [  0         0      0  1 ];...
];