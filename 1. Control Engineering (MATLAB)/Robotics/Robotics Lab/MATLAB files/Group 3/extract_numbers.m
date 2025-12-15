%% extract data from simout structure
t     = simout.time;
q1    = simout.signals.values(:,1);
q2    = simout.signals.values(:,2);
q1dot = simout.signals.values(:,3);
q2dot = simout.signals.values(:,4);
v     = simout.signals.values(:,5);