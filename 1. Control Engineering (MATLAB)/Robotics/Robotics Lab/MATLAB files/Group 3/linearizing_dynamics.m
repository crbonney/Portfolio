
%% define syms
syms q1 q2 q1dot q2dot u 
states = [q1;q2;q1dot;q2dot];
inputs = [u];

linear_state = [0;0;0;0];
linear_input = [0];
%% constants

theta1 = 0.030372023809524;
theta2 = 0.018426339285714;
theta3 = 0.018426339285714;
theta4 = 0.092131696428571;
theta5 = 0.610144642857143;
theta6 = 0.009672619047619;
g = 9.81;
% syms theta1 theta2 theta3 theta4 theta5 theta6

%% make matrices
m =    [...
        (theta1+theta2*sin(q2)^2)   (theta3*cos(q2)) ;...
            (theta3*cos(q2))            (theta2)     ;...
];


c =    [...
        (2*theta2*sin(q2)*cos(q2)*q2dot)     (-theta3*sin(q2)*q2dot) ;...
         (-theta2*sin(q2)*cos(q2)*q1dot)               (0)           ;...
];


f =    [...
         theta5*q1dot;...
         theta6*q2dot;...
];

g =    [...
                0         ;...
        -theta4*g*sin(q2) ;...
];

v = [u; 0];

%% get accleration
acceleration = -m\(c*[q1dot;q2dot]+f+g-v);

%% get state derivative
qdot = [q1dot;q2dot;acceleration];

%% get jacobian of system for inputs
J_A = jacobian(qdot, states);
J_B = jacobian(qdot, inputs);

%% get linear system
A = double(round(subs(J_A, [states; inputs], [linear_state; linear_input])*1000)/1000);
B = double(round(subs(J_B, [states; inputs], [linear_state; linear_input])*1000)/1000);
% A = subs(J_A, [states; inputs], [linear_state; linear_input])
% B = subs(J_B, [states; inputs], [linear_state; linear_input])

%% confirm controllability

Ctrb = ctrb(A,B);

rank(Ctrb) % rank 4

%% make controller
n = -6;
desired_poles = [n:-1:n-3];

K = place(A,B,desired_poles);

eig(A-B*K) %[-5;-6;-7;-8]