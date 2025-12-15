% creates a joint vector for the position of the stanford arm from 
% a cartesian input; doesn't calculate wrist angles or EOAT
function joint_vector  = Cartesian_to_Joints(x,y,z)
%% initialize
joint_vector = zeros(1,6);

%% Calculate spherical
phi = atan2(y,x);
rho = sqrt(x.^2 + y.^2 + z.^2);
theta = acos(z/rho);

%% d3 
if (rho < 2)
    rho = 2;
end
d3 = sqrt(rho^2-4);
joint_vector(3) = d3;

%% theta2
theta_bound = pi/2-atan2(d3,2);
if (theta <= theta_bound)
    theta = theta_bound + 0.01;
elseif (theta >= pi-theta_bound)
    theta = pi-theta_bound - 0.01;
end
theta2 = acos(rho*cos(theta)/d3);
joint_vector(2) = theta2;

%% theta1
alpha = atan2(2,d3*sin(theta2));

theta1 = phi - alpha;
joint_vector(1) = theta1;
end