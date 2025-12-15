close all;
x_0 = [0;0.3;6;6];

timespan = [0 3];

sat = @(x, range) min(max(x, range(1)), range(2));
% sat = @(x, range) 0;

f = @(x) (A*x - B*sat(K*x,[-10,10]));
[t,state] = ode45( @(t,z) f(z),timespan, x_0);

figure;
plot(t,state);
hold on;
plot(t,sat(K*state',[-10,10]));
legend({'q_1','q_2','dq_1','dq_2','v'});
