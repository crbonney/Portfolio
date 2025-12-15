
close all;
t_data = ScopeData(:,1);
data1  = ScopeData(:,2);
data2  = ScopeData(:,3);

t_sim  = simout.time+1;
sim1   = simout.Data(:,1);
sim2   = simout.Data(:,2);

figure
plot(t_data,data1,'r');
hold on
plot(t_sim,sim1,'b');
legend('Physical','Simulation','Location','best');
xlabel('time (s)');
ylabel('q_1 (rad)')

figure
plot(t_data,data2,'r');
hold on
plot(t_sim,sim2,'b');
legend('Physical','Simulation','Location','best');
xlabel('time (s)');
ylabel('q_2 (rad)')
