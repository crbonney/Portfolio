
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
% x = out.nonlinearraw(1,:)';
% y = out.nonlinearraw(2,:)';
% z = out.nonlinearraw(3,:)';
% th = out.nonlinearraw(7,:)';
% ph = out.nonlinearraw(8,:)';
% ps = out.nonlinearraw(9,:)';
K = RSLQR_Aileron.Kx;
y = -RSLQR_Aileron.y(:,1);
v = -RSLQR_Aileron.y(:,2);
ph = -RSLQR_Aileron.y(:,3);
p = -RSLQR_Aileron.y(:,4);
t = RSLQR_Aileron.t;
e = cumtrapz(t,y+1);

u = -K*[e';y';v';ph';p'];

x = 0.*y;
z = ones(size(y));
th = 0.*z;
% ph = 0.*z;
ps = 0.*z;


T = [x y z ph th ps]; %CHANGE THIS TO THE NAME OF THE VARIABLE CREATED BY TO WORKSPACE BLOCK


%the drone is .18 meters by .18 meters
d = .18/2;
c1 = [d; d; 0]; %motor coordinates compared to center of drone
c2 = [d; -d; 0];
c3 = -c1;
c4 = -c2;
arrow = [d*5; 0; 0];
time_scaling = 20; % how fast simulation runs
disp('ping');
start_time = 0.05;

h = figure;
% set(gcf, 'Position',  [100, 100, 1100, 500])
for i = [zeros(1,20), start_time:floor(length(T(:,1))/time_scaling)]
    if i ~= 0
    t = i*time_scaling;
    XYZ = [T(t,1); T(t,2); T(t,3)];
    theta = T(t,4);
    phi = T(t,5);
    psi = T(t,6);
    %Defining rotation matrices
    Rx = [1 0 0; 0 cos(theta) sin(theta); 0 -sin(theta) cos(theta)];
    Ry = [cos(phi) 0 -sin(phi); 0 1 0; sin(phi) 0 cos(phi)];
    Rz = [cos(psi) sin(psi) 0; -sin(psi) cos(psi) 0; 0 0 1];
    b1 = Rz*Ry*Rx*c1;
    b2 = Rz*Ry*Rx*c2;
    b3 = Rz*Ry*Rx*c3;
    b4 = Rz*Ry*Rx*c4;
    ar = Rz*Ry*Rx*arrow;
    m1 = XYZ + b1;
    m2 = XYZ + b2;
    m3 = XYZ + b3;
    m4 = XYZ + b4;
    ar = XYZ + ar;
    ctr = XYZ;
    P1 = [m1 m3];
    P2 = [m2 m4];
    P3 = [m1 m2];
    P4 = [m3 m4];

    %displaying the drone
    plot3(P1(1,:),P1(2,:),P1(3,:),'k-', 'linewidth', 2);
    axis([-1.5 1.5 -1.5 1.5 0 1.5].*1);
    xlabel('X Axis [Meters]')
    ylabel('Y Axis [Meters]')
    zlabel('Height [Meters]')

%     if t*Ts > 10        
        title("T = " + i/25);
%     else
%         title("T = " + t*Ts + " (setup)");
%     end
    hold on;
    grid on;
    plot3(P2(1,:),P2(2,:),P2(3,:),'k-', 'linewidth', 2);
    quiver3(T(t,1), T(t,2), T(t,3),0,u(t)/2,0,'r','LineWidth',3)
    plot3(P3(1,:),P3(2,:),P3(3,:),'ob', 'linewidth', 1);
    plot3(P4(1,:),P4(2,:),P4(3,:),'ok', 'linewidth', 1);
%     plot3(x_c,y_c,z_c, '-g', 'linewidth', 1);
%     plot3([ctr(1), ar(1)], [ctr(2), ar(2)], [ctr(3), ar(3)], '-k', 'linewidth', 1);
    view(45,45);
    drawnow;
    hold off
    else 
        plot3(0,0,0)
        grid on
    axis([-1.5 1.5 -1.5 1.5 0 1.5].*1);
    view(45,45);
        xlabel('X Axis [Meters]')
    ylabel('Y Axis [Meters]')
    zlabel('Height [Meters]')
            title("T = " + 0);

        drawnow;
    end
    
    
end