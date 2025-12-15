function Xdot = xdot(Friction,Gravity,tau,X)

%#codegen
SFric1=Friction(1);
DFric1=Friction(2);
SFric2=Friction(3);
DFric2=Friction(4);
SFric3=Friction(5);
DFric3=Friction(6);

grav=Gravity;

q1=X(1);
q1dot=X(2);
q2=X(3);
q2dot=X(4);
q3=X(5);
q3dot=X(6);

tau1 = tau(1);
tau2 = tau(2);
tau3 = tau(3);

MassMatrix=zeros(3);
MassMatrix(1,1)=80*cos(q2 + q3) + 420*cos(q2) + 60*cos(q3) + 12291/20;
MassMatrix(1,2)=40*cos(q2 + q3) + 210*cos(q2) + 60*cos(q3) + 2681/20;
MassMatrix(1,3)=40*cos(q2 + q3) + 30*cos(q3) + 101/10;
MassMatrix(2,1)=40*cos(q2 + q3) + 210*cos(q2) + 60*cos(q3) + 2681/20;
MassMatrix(2,2)=60*cos(q3) + 2681/20;
MassMatrix(2,3)=30*cos(q3) + 101/10;
MassMatrix(3,1)=40*cos(q2 + q3) + 30*cos(q3) + 101/10;
MassMatrix(3,2)=30*cos(q3) + 101/10;
MassMatrix(3,3)=101/10;

CMatrix=zeros(3);
CMatrix(1,2)=-40*sin(q2 + q3) - 210*sin(q2);
CMatrix(1,3)=-40*sin(q2 + q3) - 30*sin(q3);
CMatrix(2,1)=40*sin(q2 +q3) + 210*sin(q2);
CMatrix(2,3)=-30*sin(q3);
CMatrix(3,1)=40*sin(q2 +q3) + 30*sin(q3);
CMatrix(3,2)=30*sin(q3);

BMatrix=zeros(3);
BMatrix(1,1)=-80*sin(q2 + q3) - 420*sin(q2);
BMatrix(1,2)=-80*sin(q2 + q3) - 60*sin(q3);
BMatrix(1,3)=-80*sin(q2 + q3) - 60*sin(q3);
BMatrix(2,2)=-60*sin(q3);
BMatrix(2,3)=-60*sin(q3);
BMatrix(3,1)=60*sin(q3);

GMatrix=[0;0;0];
GMatrix(1)=15*grav*((3*cos(q1 + q2))/2 + 4*cos(q1)) + 10*grav*(cos(q1 + q2 + q3) + 3*cos(q1 +q2) +4*cos(q1)) + 40*grav*cos(q1);
GMatrix(2)=10*grav*(cos(q1 + q2 + q3) + 3*cos(q1 + q2)) + (45*grav*cos(q1 + q2))/2;
GMatrix(3)=10*grav*cos(q1 + q2 + q3);

% SFric1=5;
% DFric1=5;
J1Friction=SFric1*sign(q1dot) + DFric1*q1dot;
% SFric2=0;
% DFric2=0;
J2Friction=SFric2*sign(q2dot) + DFric2*q2dot;
% SFric3=0;
% DFric3=0;
J3Friction=SFric3*sign(q3dot) + DFric3*q3dot;


FMatrix=[J1Friction;J2Friction;J3Friction];


Accel=MassMatrix^(-1)*(tau - CMatrix*[q1dot^2;q2dot^2;q3dot^2] - BMatrix*[q1dot*q2dot;q1dot*q3dot;q2dot*q3dot] - GMatrix - FMatrix);

% 
%     accel1 =  -(320758*tau1 - 320758*tau2 - 180000*tau1*cos(2*q3) + 180000*tau2*cos(2*q3) + 37611180*q1dot^2*sin(q2) + 37611180*q2dot^2*sin(q2) + 5526000*q1dot^2*sin(q2 - q3) - 8052000*q1dot^2*sin(q2 + 2*q3) + 5526000*q2dot^2*sin(q2 - q3) - 8052000*q2dot^2*sin(q2 + 2*q3) + 5526000*q3dot^2*sin(q2 - q3) + 38682000*q1dot^2*sin(2*q2) - 723200*tau3*cos(q2 + q3) + 341020*grav*cos(q1) - 2684000*grav*cos(q1 + 2*q2 + 2*q3) - 10736000*q1dot^2*sin(2*q2 + 2*q3) - 608400*tau2*cos(q2) + 608400*tau3*cos(q2) + 9670500*grav*cos(q1 + 2*q2) - 900000*grav*cos(q1 - 2*q3) - 900000*grav*cos(q1 + 2*q3) + 240000*tau2*cos(q2 + 2*q3) + 1260000*tau3*cos(q2 - q3) - 240000*tau3*cos(q2 + 2*q3) + 104320*q1dot^2*sin(q2 + q3) + 104320*q2dot^2*sin(q2 + q3) + 104320*q3dot^2*sin(q2 + q3) + 75222360*q1dot*q2dot*sin(q2) + 11052000*q1dot*q2dot*sin(q2 - q3) - 16104000*q1dot*q2dot*sin(q2 + 2*q3) + 11052000*q1dot*q3dot*sin(q2 - q3) + 11052000*q2dot*q3dot*sin(q2 - q3) + 208640*q1dot*q2dot*sin(q2 + q3) + 208640*q1dot*q3dot*sin(q2 + q3) + 208640*q2dot*q3dot*sin(q2 + q3))/(38682000*cos(2*q2) + 36090000*cos(2*q3) - 10736000*cos(2*q2 + 2*q3) - 75778219);
%     accel2 = (20*(30*q1dot^2*sin(q3) - tau3 + 30*q2dot^2*sin(q3) + 10*grav*cos(q1 + q2 + q3) + 40*q1dot^2*sin(q2 + q3) + 60*q1dot*q2dot*sin(q3))*(99160*cos(q2 + q3) - 42420*cos(q2) - 288300*cos(q3) + 32000*cos(q2 + q3)^2 - 126000*cos(q2)*cos(q3) + 168000*cos(q2 + q3)*cos(q2) + 24000*cos(q2 + q3)*cos(q3) - 97061))/(38682000*cos(2*q2) + 36090000*cos(2*q3) - 10736000*cos(2*q2 + 2*q3) - 75778219) - (2*(120000*cos(q2 + 2*q3) + 90000*cos(2*q3) - 304200*cos(q2) - 160379)*(tau1 + 210*q2dot^2*sin(q2) + 30*q3dot^2*sin(q3) - (105*grav*cos(q1 + q2))/2 - 60*grav*cos(q1) - 10*grav*cos(q1 + q2 + q3) + 40*q2dot^2*sin(q2 + q3) + 40*q3dot^2*sin(q2 + q3) + 420*q1dot*q2dot*sin(q2) + 60*q1dot*q3dot*sin(q3) + 60*q2dot*q3dot*sin(q3) + 80*q1dot*q2dot*sin(q2 + q3) + 80*q1dot*q3dot*sin(q2 + q3) + 80*q2dot*q3dot*sin(q2 + q3)))/(38682000*cos(2*q2) + 36090000*cos(2*q3) - 10736000*cos(2*q2 + 2*q3) - 75778219) + (2*(320000*cos(q2 + q3)^2 - 848400*cos(q2) + 180000*cos(q3)^2 + 480000*cos(q2 + q3)*cos(q3) - 1220989)*(tau2 - 210*q1dot^2*sin(q2) + 30*q3dot^2*sin(q3) - (105*grav*cos(q1 + q2))/2 - 10*grav*cos(q1 + q2 + q3) - 40*q1dot^2*sin(q2 + q3) + 60*q1dot*q3dot*sin(q3) + 60*q2dot*q3dot*sin(q3)))/(38682000*cos(2*q2) + 36090000*cos(2*q3) - 10736000*cos(2*q2 + 2*q3) - 75778219);
%     accel3 = (400*(4958*cos(q2 + q3) - 2121*cos(q2) - 6300*cos(q2)*cos(q3) + 1200*cos(q2 + q3)*cos(q3))*(tau1 + 210*q2dot^2*sin(q2) + 30*q3dot^2*sin(q3) - (105*grav*cos(q1 + q2))/2 - 60*grav*cos(q1) - 10*grav*cos(q1 + q2 + q3) + 40*q2dot^2*sin(q2 + q3) + 40*q3dot^2*sin(q2 + q3) + 420*q1dot*q2dot*sin(q2) + 60*q1dot*q3dot*sin(q3) + 60*q2dot*q3dot*sin(q3) + 80*q1dot*q2dot*sin(q2 + q3) + 80*q1dot*q3dot*sin(q2 + q3) + 80*q2dot*q3dot*sin(q2 + q3)))/(38682000*cos(2*q2) + 36090000*cos(2*q3) - 10736000*cos(2*q2 + 2*q3) - 75778219) - (20*(tau2 - 210*q1dot^2*sin(q2) + 30*q3dot^2*sin(q3) - (105*grav*cos(q1 + q2))/2 - 10*grav*cos(q1 + q2 + q3) - 40*q1dot^2*sin(q2 + q3) + 60*q1dot*q3dot*sin(q3) + 60*q2dot*q3dot*sin(q3))*(99160*cos(q2 + q3) - 42420*cos(q2) - 288300*cos(q3) + 32000*cos(q2 + q3)^2 - 126000*cos(q2)*cos(q3) + 168000*cos(q2 + q3)*cos(q2) + 24000*cos(q2 + q3)*cos(q3) - 97061))/(38682000*cos(2*q2) + 36090000*cos(2*q3) - 10736000*cos(2*q2 + 2*q3) - 75778219) - (10*(64000*cos(q2 + q3)^2 - 1153200*cos(q3) + 1764000*cos(q2)^2 + 672000*cos(q2 + q3)*cos(q2) - 2576441)*(30*q1dot^2*sin(q3) - tau3 + 30*q2dot^2*sin(q3) + 10*grav*cos(q1 + q2 + q3) + 40*q1dot^2*sin(q2 + q3) + 60*q1dot*q2dot*sin(q3)))/(38682000*cos(2*q2) + 36090000*cos(2*q3) - 10736000*cos(2*q2 + 2*q3) - 75778219);
%     Xdot=[q1dot;accel1;q2dot;accel2;q3dot;accel3];

    
end