close all;
% clear all;

k_i = 0;
k_d = 0;
k_p = 20;


% s = tf('s');
% K = 1/s; 
% [K_num, K_dem ] = tfdata(K,'v');
% 
% 
% output = thetaout;
% input = motorin;
% signal = signalin;
% 
% figure;
% subplot(2,1,1);
% plot(output.Time, output.Data(:,1));
% ylabel('\theta (rads)');
% xlabel('time (s)');
% title('Output angle \theta');
% 
% subplot(2,1,2);
% plot(input.Time, input.Data(:,1));
% ylabel('input');
% xlabel('time (s)');
% title('Motor and signal input to system');
% hold on;
% plot(signal.Time, signal.Data(:,1), 'Color', 'Red');
% legend({'Motor input','Signal input'},'Location','best');
