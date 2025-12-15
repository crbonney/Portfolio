
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
g = 9.81;

theta1 = (J1+m2*L12^2)*Ra/(kr*kt);
theta2 = 1/3*m2*L2^2*Ra/(kr*kt);
theta3 = 1/2*m2*L12*L2*Ra/(kr*kt);
theta4 = m2*Lc2*Ra/(kr*kt);
theta5 = beta1*Ra/(kr*kt)+kr*kt;
theta6 = beta2*Ra/(kr*kt);