function [] = print_analysis(varargin)

designs = varargin;
n_designs = nargin;
colors = ['b','r','g','m','c','k'];

rtd  = 180/pi;
dd=0.:.001:2*pi;
xx1=cos(dd)-1;yy1=sin(dd);

%% Controller Models
disp(' ');
for ii = 1:n_designs
    disp(' ')
    disp([designs{ii}.name, ' Controller  Model'])
    disp('[ Ac Bc1 Bc1 ]')
##    OCTAVE CHANGE
##    HH = vpa([ designs{ii}.Controller.Ac designs{ii}.Controller.Bc1 designs{ii}.Controller.Bc2],3)
    HH = ([ designs{ii}.Controller.Ac designs{ii}.Controller.Bc1 designs{ii}.Controller.Bc2])
    disp('[ Cc Dc1 Dc2 ]')
##    HH = vpa([designs{ii}.Controller.Cc designs{ii}.Controller.Dc1 designs{ii}.Controller.Dc2],3)
    HH = ([designs{ii}.Controller.Cc designs{ii}.Controller.Dc1 designs{ii}.Controller.Dc2])

end

%% Closed Loop Eigenvalues/vectors
disp(' ')
for ii= 1:n_designs
    disp(' ')
    [V,D] = eig(designs{ii}.sys_cl.A);
    disp([designs{ii}.name, ' Closed Loop Eigenvectors'])
    V
    disp([designs{ii}.name, ' Closed Loop Eigenvalues'])
    diag(D)
end

%% Step Response
figure('Name','Command State Step Response');
leg = {};
for ii = 1:n_designs
    plot(designs{ii}.t,designs{ii}.y(:,1),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' response: Tr=', num2str(designs{ii}.metric(5)));
end
legend(leg(:),'Location','best');
xlabel('time (sec)')
ylabel('Command Variable')
title('Command State Step Response');

figure('Name','q Step Response');
leg = {};
for ii = 1:n_designs
    plot(designs{ii}.t,designs{ii}.y(:,2),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' response: Tr=', num2str(designs{ii}.metric(5)));
end
legend(leg(:),'Location','best');
xlabel('time (sec)')
ylabel('q')
title('q Step Response');
##
##figure('Name','delta Step Response');
##leg = {};
##for ii = 1:n_designs
##    plot(designs{ii}.t,designs{ii}.y(:,3),colors(ii),'LineWidth',2);
##    grid on
##    hold on
##    leg{ii} = strcat(designs{ii}.name, ' response: Tr=', num2str(designs{ii}.metric(5)));
##end
##legend(leg(:),'Location','best');
##xlabel('time (sec)')
##ylabel('delta')
##title('delta Step Response');
##
##figure('Name','deltadot Step Response');
##leg = {};
##for ii = 1:n_designs
##    plot(designs{ii}.t,designs{ii}.y(:,4),colors(ii),'LineWidth',2);
##    grid on
##    hold on
##    leg{ii} = strcat(designs{ii}.name, ' response: Tr=', num2str(designs{ii}.metric(5)));
##end
##legend(leg(:),'Location','best');
##xlabel('time (sec)')
##ylabel('deltadot')
##title('deltadot Step Response');
%% Plant Input Nyquist Plot

figure('Name','Nyquist Plot at Plant Input');
leg = {};
for ii = 1:n_designs
    plot(squeeze(real(designs{ii}.Lu)),squeeze(imag(designs{ii}.Lu)),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' Lu');
end
leg{n_designs+1} = 'Unit Circle';
plot(xx1,yy1,'k:','LineWidth',1.5);
legend([leg(:)],'Location','best');
xlabel('Real Lu')
ylabel('Imag Lu')
axis([-3 3 -3 3]);
title('Nyquist Plot at Plant Input');

%% Bode Magnitude Plot
figure('Name','Bode Magnitude at Plant Input');
leg = {};
for ii = 1:n_designs
    semilogx(designs{ii}.w,20*log10(abs(designs{ii}.Lu)),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' Lu: LGCF=', num2str(designs{ii}.metric(4)));
end
legend(leg(:),'Location','best');
xlabel('Frequency (rps)')
ylabel('Magnitude (dB)')
title('Bode Magnitude Plot at Plant Input');

%% Return Difference at Plant Input

figure('Name','Return Difference at Plant Input');
leg = {};
for ii = 1:n_designs
    semilogx(designs{ii}.w,20*log10(abs(designs{ii}.rd)),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' RD: min(I+Lu)=', num2str(designs{ii}.metric(2)));
end
legend(leg(:),'Location','best');
xlabel('Frequency (rps)')
ylabel('Magnitude (dB)')
title('Return Difference at Plant Input')

%% Stability Robustness at Plant Input

figure('Name','Stability Robustness at Plant Input');
leg = {};
for ii = 1:n_designs
    semilogx(designs{ii}.w,20*log10(abs(designs{ii}.sr)),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' SR: min(I+inv(Lu))=', num2str(designs{ii}.metric(3)));
end
legend(leg(:),'Location','best');
xlabel('Frequency (rps)')
ylabel('Magnitude (dB)')
title('Stability Robustness at Plant Input')


%% Classical Margins

disp(' ')
for ii = 1:n_designs
    disp(' ')
    disp([designs{ii}.name, ' Classical Margins']);
    disp(designs{ii}.classical_margins);
end

%% Singular Value GM/PM Margins

disp(' ')
for ii=1:n_designs
    disp(' ')
    disp([designs{ii}.name, ' Combined SV Margins']);
    disp(['Min SV of RD: min(I+Lu) = ' num2str(designs{ii}.metric(2))]);
    disp(['Min SV of SR: min(I+Lu) = ' num2str(designs{ii}.metric(3))]);
%     % Return Difference Margins
    RDu_nGM = 1/(1+designs{ii}.metric(2));
    RDu_pGM = 1/(1-designs{ii}.metric(2));
    RDu_Pha = 2*asin(designs{ii}.metric(2)/2);
    RDu_nGM_dB = 20*log10(RDu_nGM);
    RDu_pGM_dB = 20*log10(RDu_pGM);
    RDu_Pha_deg = 180*RDu_Pha/pi ;
%     disp('RDu_nGM RDu_pGM RDu_Pha')
%     disp([num2str(RDu_nGM) ' ' num2str(RDu_pGM) ' ' num2str(RDu_Pha)])
%     disp([num2str(RDu_nGM_dB) ' dB ' num2str(RDu_pGM_dB) ' dB ' num2str(RDu_Pha_deg) ' deg'])
%     % Stability Robustness Margins
% 
    SRu_nGM = 1-designs{ii}.metric(3);
    SRu_pGM = 1+designs{ii}.metric(3);
    SRu_Pha = 2*asin(designs{ii}.metric(3)/2);
    SRu_nGM_dB = 20*log10(SRu_nGM);
    SRu_pGM_dB = 20*log10(SRu_pGM);
    SRu_Pha_deg = 180*SRu_Pha/pi ;
%     disp('SRu_nGM SRu_pGM SRu_Pha')
%     disp([num2str(SRu_nGM) ' ' num2str(SRu_pGM) ' ' num2str(SRu_Pha)])
%     disp([num2str(SRu_nGM_dB) ' dB ' num2str(SRu_pGM_dB) ' dB ' num2str(SRu_Pha_deg) ' deg'])
    % Combined Singular Value Margins
    disp(sprintf(['Singular Value GM = [', num2str(min(RDu_nGM_dB,SRu_nGM_dB)),' dB , ',num2str(max(RDu_pGM_dB,SRu_pGM_dB)) ' dB]']));
    disp(sprintf(['Singular Value PM = [+/-', num2str(max(RDu_Pha_deg,SRu_Pha_deg)) ' deg]']));
%     disp(sprintf(['  SV GM-      SV GM+        SV +/-PM \n', ...
%   num2str(min(RDu_nGM_dB,SRu_nGM_dB)) 'dB   ' num2str(max(RDu_pGM_dB,SRu_pGM_dB)) 'dB     ' num2str(max(RDu_Pha_deg,SRu_Pha_deg)) 'deg']));
end

%% Bode Magnitude Plot of Senistivity (S)

figure('Name','Sens Magnitude Plot (S)');
leg = {};
for ii = 1:n_designs
    semilogx(designs{ii}.w,20*log10(abs(designs{ii}.S(1,:))),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' S: Smax=', num2str(designs{ii}.metric(12)));
end
legend(leg(:),'Location','best');
xlabel('Frequency (rps)')
ylabel('Magnitude (dB)')
title('Sens Magnitude Plot (S)')


%% Bode Magnitude Plot of Complimentary Sensitivity (T)

figure('Name','Comp Sens Magnitude Plot (T)');
leg = {};
for ii = 1:n_designs
    semilogx(designs{ii}.w,20*log10(abs(designs{ii}.T(1,:))),colors(ii),'LineWidth',2);
    grid on
    hold on
    leg{ii} = strcat(designs{ii}.name, ' T: Tmax=', num2str(designs{ii}.metric(11)));
end
legend(leg(:),'Location','best');
xlabel('Frequency (rps)')
ylabel('Magnitude (dB)')
title('Comp Sens Magnitude Plot (T)')

%% Noise-to-Control Magnitude Plot

figure('Name','Noise-2-Control');
leg = {};
for ii = 1:n_designs
    semilogx(designs{ii}.w,designs{ii}.dele_Az,colors(ii),'LineWidth',2);
    grid on
    hold on
    semilogx(designs{ii}.w,designs{ii}.dele_q,strcat(colors(ii),'--'),'LineWidth',2);
    leg{2*ii-1} = strcat(designs{ii}.name, ' Az');
    leg{2*ii} = strcat(designs{ii}.name, ' q');
end
legend(leg(:),'Location','best');
xlabel('Frequency (rps)')
ylabel('Magnitude (dB)')
title('Noise to Control')

figure('Name','Noise-2-Control Rate');
leg = {};
for ii = 1:n_designs
    semilogx(designs{ii}.w,designs{ii}.deledot_Az,colors(ii),'LineWidth',2);
    grid on
    hold on
    semilogx(designs{ii}.w,designs{ii}.deledot_q,strcat(colors(ii),'--'),'LineWidth',2);
    leg{2*ii-1} = strcat(designs{ii}.name, ' Az');
    leg{2*ii} = strcat(designs{ii}.name, ' q');
end
legend(leg(:),'Location','best');
xlabel('Frequency (rps)')
ylabel('Magnitude (dB)')
title('Noise to Control Rate')


end

