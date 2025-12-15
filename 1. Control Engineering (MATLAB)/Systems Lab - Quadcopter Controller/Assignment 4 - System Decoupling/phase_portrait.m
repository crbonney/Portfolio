
xdot = @(t,x) Aaileron*x;

% x = -1:0.1:1;
x = -2:0.2:2;
y = -2:0.2:2;
timespan = 0:0.1:1;

soln = zeros(length(timespan),length(x)*length(y),2);
% soln = zeros(length(timespan),length(x)*length(y)*length(z)*length(w),4);
for i=1:length(x)
    for j=1:length(y)
                [t,state] = ode45(xdot, timespan, [0;x(i);0;y(j)]);
                soln(:,i+j*length(x),1) = state(:,1);
                soln(:,i+j*length(x),2) = state(:,3);
    end
end

%% Plot
[t,len,~] = size(soln);
figure('Color', 'w');
% %plots all sol'ns
for n=1:len
    plot(soln(:,n,1),soln(:,n,2));
    hold on;
end
xlabel('Y (m)');
ylabel('\phi (rad)');
title('Aileron subsystem Phase Portrait (Y,\phi)');
