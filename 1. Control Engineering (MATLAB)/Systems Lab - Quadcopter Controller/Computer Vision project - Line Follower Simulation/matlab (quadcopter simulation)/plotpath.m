close all

x = out.nonlinearraw(:,1);
y = out.nonlinearraw(:,2);
z = -out.nonlinearraw(:,3);
% ps = out.nonlinearraw(:,9);

%% init figure and plot drone path
figure
grid on
hold on
plot3(x,y,z,'-k', 'linewidth', 3) % drone path

%% Show "Combo" path
% c_rad = sqrt(8);
% th = linspace(pi/4,3*pi/4,20);
% x_c = c_rad*cos(th);
% y_c = c_rad*sin(th);
% z_c = ones(length(th));
% 
% l1 = [-4 -2; 0 2; 1 1];
% l2 = [2 5; 2 5; 1 1];
% 
% plot3(x_c,y_c,z_c, '-g', 'linewidth', 2); % circle path
% plot3(l1(1,:),l1(2,:),l1(3,:),'-g', 'linewidth', 2); % line paths
% plot3(l2(1,:),l2(2,:),l2(3,:),'-g', 'linewidth', 2);
% axis([-4.5,4.5,-0.5,4.5,0,1.5])

%% Show "Circle" path

c_rad = 2;
th = linspace(0,2*pi,100);
x_c = c_rad*cos(th);
y_c = c_rad*sin(th);
z_c = ones(length(th));

plot3(x_c,y_c,z_c, '-g', 'linewidth', 2); % circle path
axis([-2.5,2.5,-2.5,2.5, 0, 1.5])


%% Show "Line" path

% l1 = [0 4; 2 -2; 1 1];
% plot3(l1(1,:),l1(2,:),l1(3,:),'-g', 'linewidth', 2); % line paths
% axis([-0.5,4.5,-2.5,2.5, 0, 1.5])


%% Show "Angle" path

% l1 = [0 2; 2 2; 1 1];
% l2 = [2 4; 2 -4; 1 1];
% 
% plot3(l1(1,:),l1(2,:),l1(3,:),'-g', 'linewidth', 2); % line paths
% plot3(l2(1,:),l2(2,:),l2(3,:),'-g', 'linewidth', 2);
% axis([-0.5,4.5,-2.5,2.5, 0, 1.5])

%% Graph Settings

set(gcf,'color','w');
xlabel('X Axis (m)')
ylabel('Y Axis (m)')
zlabel('Height (m)')
view(-45,45);
legend("UAV path", "Command","Location","northeast")
