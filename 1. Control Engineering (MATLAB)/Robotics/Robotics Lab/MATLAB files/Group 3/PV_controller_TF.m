
k = 1.74;
tau = 0.025;

Mp = 0.05;
tp = 0.15;

zeta = sqrt(log(Mp)^2/(pi^2+log(Mp)^2));
omega = pi/(tp*sqrt(1-zeta^2));

P = omega^2*tau/k;
V = (2*zeta*omega*tau-1)/k;

k1 = 1;
k2 = 0;
