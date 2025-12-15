

% GMatrix=[0;0;0];
% GMatrix(1)=15*grav*((3*cos(q1 + q2))/2 + 4*cos(q1)) + 10*grav*(cos(q1 + q2 + q3) + 3*cos(q1 +q2) +4*cos(q1)) + 40*grav*cos(q1);
% GMatrix(2)=10*grav*(cos(q1 + q2 + q3) + 3*cos(q1 + q2)) + (45*grav*cos(q1 + q2))/2;
% GMatrix(3)=10*grav*cos(q1 + q2 + q3);
GMatrix = [15*grav*((3*cos(q1 + q2))/2 + 4*cos(q1)) + 10*grav*(cos(q1 + q2 + q3) + 3*cos(q1 +q2) +4*cos(q1)) + 40*grav*cos(q1);...
           10*grav*(cos(q1 + q2 + q3) + 3*cos(q1 + q2)) + (45*grav*cos(q1 + q2))/2;...
           10*grav*cos(q1 + q2 + q3)];
