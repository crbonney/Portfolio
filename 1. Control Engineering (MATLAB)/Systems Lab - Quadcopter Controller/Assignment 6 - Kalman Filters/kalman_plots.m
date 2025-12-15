load('RSdata.mat')

t = rt_simout.time;

ue = rt_simout.signals.values(:,1);
ve = rt_simout.signals.values(:,2);
we = rt_simout.signals.values(:,3);

ze = rt_simout.signals.values(:,4);

pe = rt_simout.signals.values(:,5);
qe = rt_simout.signals.values(:,6);
re = rt_simout.signals.values(:,7);

phie   = rt_simout.signals.values(:,8);
thetae = rt_simout.signals.values(:,9);

close all
figure
plot(t, pe);
hold on
plot(t, phie);
legend({'p_e','\phi_e'});

figure
plot(t, qe);
hold on
plot(t, thetae);
legend({'q_e','\theta_e'});

figure
plot(t, we);
hold on
plot(t, ze);
legend({'w_e','z_e'});
