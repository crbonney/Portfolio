clear all
close all

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

%% Create Transformation Matrices
T01 = [...
       [cos(q1)  -sin(q1)  0  0 ];...
       [sin(q1)   cos(q1)  0  0 ];...
       [  0         0      1  0 ];...
       [  0         0      0  1 ];...
];


T12 = [...
       [cos(q2)  -sin(q2)  0  L1];...
       [sin(q2)   cos(q2)  0  0 ];...
       [  0         0      1  0 ];...
       [  0         0      0  1 ];...
];

T23 = [...
       [cos(q3)  -sin(q3)  0  L2];...
       [sin(q3)   cos(q3)  0  0 ];...
       [  0         0      1  0 ];...
       [  0         0      0  1 ];...
];

T34 = [...
       [  1         0      0  L3];...
       [  0         1      0  0 ];...
       [  0         0      1  0 ];...
       [  0         0      0  1 ];...
];

T04 = T01*T12*T23*T34;

%% Direct Differentiation Jacobian
% X_direct = [...
%      T04(1:3,4) ;...
%      T04(1:3,1) ;...
%      T04(1:3,2) ;...
%      T04(1:3,3) ;...
% ];

x = L1*cos(q1) + L2*cos(q1+q2) + L3*cos(q1+q2+q3);
y = L1*sin(q1) + L2*sin(q1+q2) + L3*sin(q1+q2+q3);

% r = atan2(y,x);
r = q1+q2+q3;

X_p = jacobian([x y 0],[q]);
X_r = jacobian([0 0 r],[q]);

J = [X_p; X_r];


%% Calculate Mq

Jv1 = [...
       [ -L1*sin(q1)/2 0 0];... 
       [  L1*cos(q1)/2 0 0];...
       [        0      0 0];...
];

Jv2 = [...
       [ -(L2*sin(q1 + q2))/2 - L1*sin(q1), -(L2*sin(q1 + q2))/2, 0];...
       [  (L2*cos(q1 + q2))/2 + L1*cos(q1),  (L2*cos(q1 + q2))/2, 0];...
       [                  0,                          0,          0];...
];

Jv3 = [...
       [ -L2*sin(q1 + q2) - L1*sin(q1) - (L3*sin(q1 + q2 + q3))/2, - L2*sin(q1 + q2) - (L3*sin(q1 + q2 + q3))/2, -(L3*sin(q1 + q2 + q3))/2];...
       [  L2*cos(q1 + q2) + L1*cos(q1) + (L3*cos(q1 + q2 + q3))/2,   L2*cos(q1 + q2) + (L3*cos(q1 + q2 + q3))/2,  (L3*cos(q1 + q2 + q3))/2];...
       [                                                        0,                                            0,                         0];...
];

Jw1 = [0,0,0;0,0,0;1,0,0];
Jw2 = [0,0,0;0,0,0;1,1,0];
Jw3 = [0,0,0;0,0,0;1,1,1];

Mq = (m1*Jv1'*Jv1 + Jw1'*Ic1*Jw1) +...
     (m2*Jv2'*Jv2 + Jw2'*Ic2*Jw2) +...
     (m3*Jv3'*Jv3 + Jw3'*Ic3*Jw3) ;
 
Mq = simplify(subs(Mq, [mm LL Izz_all],[mm_actual, LL_actual, Izz_actual]));

%% Calculate Vqqdot
dMq1 = diff(Mq, q1);
dMq2 = diff(Mq, q2);
dMq3 = diff(Mq, q3);

Mdot = dMq1*q1dot + dMq2*q2dot + dMq3*q3dot;
Vq = Mdot*qdot -1/2*[qdot'*dMq1*qdot; qdot'*dMq2*qdot; qdot'*dMq3*qdot];
Vq = simplify(Vq);

%% Calculate Gq
syms grav real
g = [0;-grav;0];
Gq = -[Jv1' Jv2' Jv3']*[m1*g;m2*g;m3*g];
Gq = simplify(subs(Gq, [mm LL],[mm_actual LL_actual]));

% syms tau1 tau2 tau3 real
% tau = [tau1; tau2; tau3];
accel = inv(Mq)*(- Vq - Gq);
accel = simplify(accel);

%% Position Calculator
syms q1ddot q2ddot q3ddot real
qddot = [q1ddot;q2ddot;q3ddot];
tau = (Vq+Gq)+Mq*qddot;
tau = simplify(tau);