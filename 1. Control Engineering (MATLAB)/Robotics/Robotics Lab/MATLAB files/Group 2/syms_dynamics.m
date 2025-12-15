J1 = 0.0012;
m2 = 0.127;
L12 = 0.2;
L2 = 0.3;
Lc2 = L2/2;
beta1 = 0.015;
beta2 = 0.002;
Ra = 2.6;
kt = 0.00768;
kr = 70;
% g = 9.81;

syms theta_1 theta_2 theta_3 theta_4 theta_5 theta_6

% theta_1 = (J1+m2*L12^2)*Ra/(kr*kt);
% theta_2 = 1/3*m2*L2^2*Ra/(kr*kt);
% theta_3 = 1/2*m2*L12*L2*Ra/(kr*kt);
% theta_4 = m2*Lc2*Ra/(kr*kt);
% theta_5 = beta1*Ra/(kr*kt)+kr*kt;
% theta_6 = beta2*Ra/(kr*kt);

syms q_1 q_1dot q_2 q_2dot v g
% q_1 = x(1);
% q_2 = x(2);
% q_1dot = x(3);
% q_2dot = x(4);
% v = [u; 0];

m =    [...
        (theta_1+theta_2*sin(q_2)^2) (theta_3*cos(q_2));...
            (theta_3*cos(q_2)) (theta_2);...
];


c =    [...
             (2*theta_2*cos(q_2)*q_2dot) (-theta_3*sin(q_2)*q_2dot);...
         (-theta_2*sin(q_2)*cos(q_2)*q_1dot) (0);...
];


f =    [...
         theta_5*q_1dot;...
         theta_6*q_2dot;...
];

g =    [...
                  0;...
        -theta_4*g*sin(q_2);...
];


acceleration = -m\(c*[q_1dot;q_2dot]+f+g-v);

xdot = [q_1dot;q_2dot;acceleration];