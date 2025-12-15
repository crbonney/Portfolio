
%% Input number of joints and type
n = 3; %number of joints
epsilon = [1 1 1]; %1 for revolute, 0 for prismatic

%% Declare Symbolics
q = sym('q',[n,1]);
syms q qdot L m Ixx Iyy Izz [n 1] real
syms Ic [3 3 n] real

for i=1:n
    Ic(:,:,i)=diag([Ixx(i) Iyy(i) Izz(i)]);
end

%% give values for actual
m_actual = [20 15 10]'; %kg
L_actual = [4 3 2]'; %meters
Izz_actual = [0.5 0.2 0.1]';

%% Create Transformation Matrices
syms 'T%d%d_%d%d' [4 4 n+1 n+1] real


% T01
T(:,:,1,2) = [...
       cos(q1)  -sin(q1)  0  0 ;...
       sin(q1)   cos(q1)  0  0 ;...
         0         0      1  0 ;...
         0         0      0  1 ;...
];

% T12
T(:,:,2,3) = [...
       cos(q2)  -sin(q2)  0  L1;...
       sin(q2)   cos(q2)  0  0 ;...
         0         0      1  0 ;...
         0         0      0  1 ;...
];

% T23
T(:,:,3,4) = [...
       cos(q3)  -sin(q3)  0  L2;...
       sin(q3)   cos(q3)  0  0 ;...
         0         0      1  0 ;...
         0         0      0  1 ;...
];

% T34
T(:,:,4,5) = [...
         1         0      0  L3;...
         0         1      0  0 ;...
         0         0      1  0 ;...
         0         0      0  1 ;...
];

%% Calculate all Transformation Matrices
% main diagonal:
% Tii = Identity
for i=1:n+1
    T(:,:,i,i) = eye(4,4);
end

% upper triangle
% T(i)(i+2) = T(i)(i+1)*T(i+1)(i+2)
for i=n-1:-1:1
    for j=i:n-1
        T(:,:,i,j+2) = T(:,:,i,j+1)*T(:,:,j+1,j+2);
    end
end

% lower triangle
% T(i)(j) = inv(T(j)(i))
for i=2:n
    for j=1:i
        T(:,:,i,j)=inv(T(:,:,j,i));
    end
end

T = simplify(T);

%% get center of mass transformations

syms 'T%d%d_%d%dc' [4 4 n+2 n+2] real

for i=1:n
    if (epsilon(i))
        T_c(:,:,i+1,i+2)=subs(T(:,:,i+1,i+2),L(i),L(i)/2);
    else
        T_c(:,:,i+1,i+2)=subs(T(:,:,i+1,i+2),q(i),q(i)-L(i)/2);
    end
end

T_c = simplify(T_c);

%% get Velocities

Zhat = [0;0;1];
syms 'omega%d_%d' [n 3] real

for i=1:n
    omega_(:,i) = T(1:3,1:3,1,i)*Zhat;
end

%% Make Velocity Jacobians

syms Jv [3 n n] real

for i=1:n
    P = T(:,:,1,i+1)*T_c(:,:,i+1,i+2);
    Jv(:,:,i) = jacobian(P(1:3,4),q);
end

Jv = simplify(Jv);
%% Make Angular Velocity Jacobians

syms Jw [3 n n] real

for i=1:n
    Jw(:,:,i) = [omega_(:,1:i) zeros(3,n-i)];
end
    
Jw = simplify(Jw);
%% Make Mass Matrix M(q)

syms Mq [n n] real
Mq = zeros(n,n);

for i=1:n
    Mq = Mq + m(i)*Jv(:,:,i)'*Jv(:,:,i) + Jw(:,:,i)'*Ic(:,:,i)*Jw(:,:,i);
end

Mq = simplify(Mq);
%% Get V(q,qdot)

syms 'dMq%d%d%d' [n n n] real
syms Mdot [n n] real
syms partial_kinetics [n 1] real
Mdot = zeros(n,n);

for i=1:n
    dMq(:,:,i) = diff(Mq, q(i));
    Mdot = Mdot + dMq(:,:,i)*qdot(i);
    partial_kinetics(i) = qdot'*dMq(:,:,i)*qdot;
end

Vq = Mdot*qdot -1/2*partial_kinetics;
Vq = simplify(Vq);
%% Calculate Gq
syms grav real
g = [0;-grav;0];

Gq = zeros(n,1);
for i=1:n
    Gq = Gq - Jv(:,:,i)'*m(i)*g;
end

Gq = simplify(Gq);

%% Cleanup worspace (optional)
% clearvars -except Mq Gq Vq m L Izz m_actual L_actual Izz_actual

%% Subs actual values
Mq = simplify(subs(Mq, [m L Izz],[m_actual, L_actual, Izz_actual]));
Vq = simplify(subs(Vq, [m L Izz],[m_actual, L_actual, Izz_actual]));
Gq = simplify(subs(Gq, [m L Izz],[m_actual, L_actual, Izz_actual]));

%% Acceleration (optional)
% accel = inv(Mq)*(- Vq - Gq);
% accel = simplify(accel);

%% Position Torque Calculations (optional)
% syms q1ddot q2ddot q3ddot real
% qddot = [q1ddot;q2ddot;q3ddot];
% tau = (Vq+Gq)+Mq*qddot;
% tau = simplify(tau);