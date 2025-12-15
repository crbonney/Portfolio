close all;

load('RSdata.mat');
Fs = 200;
% sensors
t  = rt_simout.time;

% sensors = rt_simout.signals.values;
u    = rt_simout.signals.values(:, 1);
X    = rt_simout.signals.values(:, 2);
v    = rt_simout.signals.values(:, 3);
Y    = rt_simout.signals.values(:, 4);
ax   = rt_simout.signals.values(:, 5);
ay   = rt_simout.signals.values(:, 6);
az   = rt_simout.signals.values(:, 7);
w    = rt_simout.signals.values(:, 8);
p    = rt_simout.signals.values(:, 9);
% phi  = rt_simout.signals.values(:,10);
% q    = rt_simout.signals.values(:,11);
% theta= rt_simout.signals.values(:,12);
% r    = rt_simout.signals.values(:,13);
% psi  = rt_simout.signals.values(:,14);
% h    = rt_simout.signals.values(:,15);
% Vbat = rt_simout.signals.values(:,16);

for i=1:9
   figure 
   plot(t,rt_simout.signals.values(:,i))
end

% sensors = rt_simout.signals.values;
% u_uf    = rt_simout.signals.values(:,17);
% X_uf    = rt_simout.signals.values(:,18);
% v_uf    = rt_simout.signals.values(:,19);
% Y_uf    = rt_simout.signals.values(:,20);
% ax_uf   = rt_simout.signals.values(:,21);
% ay_uf   = rt_simout.signals.values(:,22);
% az_uf   = rt_simout.signals.values(:,23);
% w_uf    = rt_simout.signals.values(:,24);
% p_uf    = rt_simout.signals.values(:,25);
% phi_uf  = rt_simout.signals.values(:,26);
% q_uf    = rt_simout.signals.values(:,27);
% theta_uf= rt_simout.signals.values(:,28);
% r_uf    = rt_simout.signals.values(:,29);
% psi_uf  = rt_simout.signals.values(:,30);
% h_uf    = rt_simout.signals.values(:,31);
% Vbat_uf = rt_simout.signals.values(:,32);

Z = -h;
Z_uf = -h_uf;
% az = -az-8.84;
% w = -w-8.84*t;
states = [X,u,ax,Y,v,ay,Z,w,az,phi,p,theta,q,psi,r];
states_unfiltered = [X_uf,u_uf,ax_uf,Y_uf,v_uf,ay_uf,Z_uf,w_uf,az_uf,phi_uf,p_uf,theta_uf,q_uf,psi_uf,r_uf];
state_names = ["X","u","ax","Y","v","ay","Z","w","az","phi","p","theta","q","psi","r"];

% PLOT STATES
% for i=1:size(states,2)
%     figure;
%     plot(t,states(:,i));
%     hold on
%     plot(t,states_unfiltered(:,i));
%     xlabel('t');
%     ylabel(state_names(i));
%     legend('filtered','unfiltered');
% end

fourier_data = [p,q,r,ax,ay,az,h];
fourier_unfiltered_data = [p_uf,q_uf,r_uf,ax_uf,ay_uf,az_uf,h_uf];
fourier_names = ["p","q","r","ax","ay","az","h"];
fourier_out  = fft(fourier_data, [], 1);
fourier_unfiltered_out  = fft(fourier_unfiltered_data, [], 1);
L = size(fourier_out,1);
if (mod(L,2) == 1)
    L = L+1;
    fourier_out = [fourier_out; zeros(1,size(fourier_out,2))];
    fourier_unfiltered_out = [fourier_unfiltered_out; zeros(1,size(fourier_unfiltered_out,2))];
end
P2 = abs(fourier_out/L);
P1 = P2(1:L/2+1,:);
P1(2:end-1,:) = 2*P1(2:end-1,:);

P2_uf = abs(fourier_unfiltered_out/L);
P1_uf = P2_uf(1:L/2+1,:);
P1_uf(2:end-1,:) = 2*P1_uf(2:end-1,:);


f = Fs*(0:(L/2))/L;

% PLOT FOURIER STATES
% for i=1:size(fourier_out,2)
%     figure;
%     plot(f,P1(:,i));
%     hold on
%     plot(f,P1_uf(:,i));
%     xlabel('f (Hz)');
%     ylabel(fourier_names(i));   
%     legend('filtered','unfiltered');
% end


s = tf('s');
T = 100/(s+100);
pqr_filter = T*eye(3);
pqr_unfiltered = s/s*eye(3);
angles_filter = pqr_filter/s;
figure;
bode(pqr_filter);
hold on
bode(pqr_unfiltered);
bode(angles_filter)
legend('filter','no filter','integrated angles','Location','best');
axis([-5 5 -5 5]);
figure;
nyquist(pqr_filter);
hold on
nyquist(pqr_unfiltered);
nyquist(angles_filter)
legend('filter','no filter','integrated angles','Location','best');
