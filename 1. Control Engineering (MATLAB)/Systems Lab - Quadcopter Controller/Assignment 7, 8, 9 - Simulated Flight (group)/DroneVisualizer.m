
% /// IMPORTANT ///
%T is array that hold states
%ZED is pointing downwards
%INSERT YOUR DATA HERE
%USE TO WORKSPACE BLOCK IN SIMULINK
%SAVE FORMAT AS ARRAY
%SAVE 2D SIGNALS AS 2-D ARRAY
%INPUT FOR TO WORKSPACE BLOCK MUST BE A BUS WITH
%STATES ORDERED:[XNED YNED ZNED Theta Phi PSI] FROM TOP DOWN
close all;
x = out.nonlinearraw(1,:)';
y = out.nonlinearraw(2,:)';
z = out.nonlinearraw(3,:)';
th = out.nonlinearraw(7,:)';
ph = out.nonlinearraw(8,:)';
ps = out.nonlinearraw(9,:)';

T = [x y z th ph ps]; %CHANGE THIS TO THE NAME OF THE VARIABLE CREATED BY TO WORKSPACE BLOCK

%the drone is .18 meters by .18 meters
d = .18/2;
c1 = [d; d; 0]; %motor coordinates compared to center of drone
c2 = [d; -d; 0];
c3 = -c1;
c4 = -c2;
for i = 1:floor(length(T(:,1))/11)
    XYZ = [T(11*i,1); T(11*i,2); -T(11*i,3)];
    theta = T(11*i,4);
    phi = T(11*i,5);
    psi = T(11*i,6);
    %Defining rotation matrices
    Rx = [1 0 0; 0 cos(theta) sin(theta); 0 -sin(theta) cos(theta)];
    Ry = [cos(phi) 0 -sin(phi); 0 1 0; sin(phi) 0 cos(phi)];
    Rz = [cos(psi) sin(psi) 0; -sin(psi) cos(psi) 0; 0 0 1];
    b1 = Rz*Ry*Rx*c1;
    b2 = Rz*Ry*Rx*c2;
    b3 = Rz*Ry*Rx*c3;
    b4 = Rz*Ry*Rx*c4;
    m1 = XYZ + b1;
    m2 = XYZ + b2;
    m3 = XYZ + b3;
    m4 = XYZ + b4;
    P1 = [m1 m3];
    P2 = [m2 m4];
    P3 = [m1 m2];
    P4 = [m3 m4];

    %displaying the drone
    plot3(P1(1,:),P1(2,:),P1(3,:),'k-', 'linewidth', 2);
    axis([-1 1 -1 1 0 2].*1);
    xlabel('X Axis [Meters]')
    ylabel('Y Axis [Meters]')
    zlabel('Height [Meters]')
    title("T = " + i*Ts);
    hold on;
    grid on;
    plot3(P2(1,:),P2(2,:),P2(3,:),'k-', 'linewidth', 2);
    plot3(P3(1,:),P3(2,:),P3(3,:),'ob', 'linewidth', 1);
    plot3(P4(1,:),P4(2,:),P4(3,:),'ok', 'linewidth', 1);
    drawnow;
    hold off
end