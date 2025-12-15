## Interactive RSLQR Design Tool (Octave)
## Chris Bonney, July 2021
## 
## interactively design RSLQR gains for a controller, and view the 
## stability margins, and performance metrics
## 
## Utilizing the GUI Demo from Andreas Weber <andy@josoansi.de> as a base for the GUI
## https://github.com/gnu-octave/macgyver_utils/blob/master/demo_uicontrol.m

close all
clear h

graphics_toolkit qt

addpath('functions')

h.ax = axes ("position", [0.05 0.42 0.9 0.5]);
h.fcn = @(x) polyval([-0.1 0.5 3 0], x);

## Calculates Step Response and Open Loop Response
function [y,Lu,sys_u,Kx] = calc_step_and_openloop(qq)

  % Dynamics Constants
  V=886.78;
  Za=-1.3046*V;
  Zd=-0.2142*V;
  Ma=47.7109;
  Md=-104.8346;

  % Actuator Constants
  omega = 2.*pi*11;
  zeta = sqrt(1/2);


  %% Dynamics without actuator
  Ap = [Za/V  1  ;
         Ma   0 ];
  Bp = [Zd/V ;
         Md ];

  Cp = [Za 0  ;
        0  1 ];
  Dp = [Zd ;
        0 ];

  DesignPlant = ss(Ap,Bp,Cp,Dp);

  % Size of the plant model
  [nx,~]=size(Ap);

  %% Dynamics with Actuator
  % Actuator Model
  A_actuator = [0 1; -omega^2 -2*zeta*omega];
  B_actuator = [0; omega^2];

  % itegrating actuator into system model
  Plant.Ap = [   Ap      Bp zeros(2,1); 
              zeros(2,2)  A_actuator];
  Plant.Bp = [zeros(2,1); B_actuator];
  Plant.Cp = [Za 0 Zd 0; 
              eye(4)];
  Plant.Dp = 0*(Plant.Cp*Plant.Bp);

  Ap = Plant.Ap;
  Bp = Plant.Bp;
  Cp = Plant.Cp;
  Dp = Plant.Dp;
  AnalysisPlant = ss(Ap,Bp,Cp,Dp);

  % parameters for time and frequency domain simulations
  dt = 0.001; %time-step size
  t = 0:dt:5; %length of step simulation
  w = logspace(-5,5,500); %frequency values for frequency domain analysis
  
  Ccmd = DesignPlant.C(1,:);
  Dcmd = DesignPlant.D(1,:);
  % add integrator to model to build controller
  Aw = [     zeros(1,1)                     Ccmd      ; 
        zeros(size(DesignPlant.A,1),1)  DesignPlant.A];
  Bw = [Dcmd;   DesignPlant.B];

  % build Q and R matrices and find LQR gains
  Q = zeros(size(Aw)); %shape of Aw
  Q(1,1) = qq; %adjustable parameter
  R = 1;
  Kx = lqr(Aw,Bw,Q,R);
  
  ny_analysis = size(AnalysisPlant.C,1);
  ny_design = size(DesignPlant.C,1);
  
  % build common controller form model
  Ctrl.Ac = 0;
  Ctrl.Bc1 = zeros(1,ny_analysis);
  Ctrl.Bc1(1) = 1;
  Ctrl.Bc2 = [-1];
  Ctrl.Cc = -Kx(1);
  Ctrl.Dc1 = zeros(1,ny_analysis);
  Ctrl.Dc1(2:3) = -Kx(2:size(Aw,1));
  Ctrl.Dc2 = 0;

  % build closed-loop and open-loop systems and perform analysis with actuator
  sys_cl = cl_system(AnalysisPlant,Ctrl); % AnalysisPlant contains actuator
  sys_u = input_system(AnalysisPlant,Ctrl); 
  [y,~] = step(sys_cl,t);
  Lu = squeeze(freqresp(sys_u,w)); 
  
end

% Called whenever the value of a slider changes    
% updates plots and text for analysis
function update_plot (obj, init = false)

  ## gcbo holds the handle of the control
  h = guidata (obj);
  replot = false;
  recalc = false;
  switch (gcbo)
    case {h.Q_slider}
      recalc = true;
    endswitch

  if (recalc || init)
    Q_value = get (h.Q_slider, "value");
    Q_value = 10^Q_value;
    set (h.Q_label, "string", sprintf (["Q(1,1) Value: ", num2str(Q_value,3)]));

    dt = 0.001;
    t = 0:dt:5;
    w = logspace(-5,5,500);

    % builds controller and performs analysis on system
    [y, Lu, sys_u, Kx] = (calc_step_and_openloop(Q_value));
    y = y(:,1)';
    
    set (h.kx_label, "string", sprintf (["Kx = [", num2str(Kx,3), "]"]));

    
    ye = abs(ones(size(y))-y);  % error for y
    fv = 0; %ye(numel(ye)); % final value of the error, can be set to value of final value of simulation or to 0

    e_n = ye - fv*ones(size(ye)) - 0.03*ones(size(ye)); %calculate time to reach 97% of final value
    taur = t(find(e_n < 0,1));
    
    e_n = ye - fv*ones(size(ye)) - 0.05*ones(size(ye)); %calculate settle time to reach 95% of final value
    e_n1 = abs(e_n) + e_n;
    taus = crosst(e_n1,t); % settling time
    
    if (taur) 
      set (h.rise_time, "string", sprintf ("97%% Rise time: %.3f", taur));
    else 
      set (h.rise_time, "string", sprintf ("97%% Rise time: > 5"));
    end
    
    if (taus <= 5) 
      set (h.settle_time, "string", sprintf ("95%% Settle time: %.3f", taus));
    else 
      set (h.settle_time, "string", sprintf ("95%% Settle time: > 5"));
    end
    
    % singular value margins analysis
    rd = sigma(1+sys_u,w);
    rd_min = min(min(abs(rd)));
    sr = sigma(1+inv(sys_u),w);
    sr_min = min(min(abs(sr)));
    RDu_nGM = 1/(1+rd_min);
    RDu_pGM = 1/(1-rd_min);
    RDu_Pha = 2*asin(rd_min/2);
    RDu_nGM_dB = 20*log10(RDu_nGM);
    RDu_pGM_dB = 20*log10(RDu_pGM);
    RDu_Pha_deg = 180*RDu_Pha/pi ;
    SRu_nGM = 1-sr_min;
    SRu_pGM = 1+sr_min;
    SRu_Pha = 2*asin(sr_min/2);
    SRu_nGM_dB = 20*log10(SRu_nGM);
    SRu_pGM_dB = 20*log10(SRu_pGM);
    SRu_Pha_deg = 180*SRu_Pha/pi ;
    pos_gm = (max(RDu_pGM_dB,SRu_pGM_dB));
    if (imag(pos_gm) ~= 0) 
      pos_gm = 'infinite';
    else 
      pos_gm = num2str(max(RDu_pGM_dB,SRu_pGM_dB));
    end
    
    set (h.sv_gain_margin, "string", sprintf(['SV GM = [', num2str(min(RDu_nGM_dB,SRu_nGM_dB)),' dB , ',pos_gm ' dB]']));
    set (h.sv_phase_margin, "string", sprintf(['SV PM = [+/-', num2str(max(RDu_Pha_deg,SRu_Pha_deg)) ' deg]']));
    
    [GM, PM, PCF, LGCF] = margin(sys_u);
    
    set (h.classic_gain_margin, "string", sprintf ("Classic Pos Gain Margins: %.3f dB", 20*log10(GM)));
    set (h.classic_phase_margin, "string", sprintf ("Classic Phase Margins: %.3f deg", PM));
    
    # first iteration
    if (init)
      # left plot (step response)
      subplot(2,2,1)
      # plot step
      h.plot = plot (t, y, "b");
      hold on
      # plot 95% and 105% of step lines
      h.limplot1 = plot(t, 1.05*ones(size(t)),'b--','LineWidth',0.5);
      h.limplot2 = plot(t, .95*ones(size(t)),'b--','LineWidth',0.5);
      grid on
      title("Closed-Loop Step Response");
      ylabel("y");
      xlabel("time (s)");
      # right plot (nyquist)
      subplot(2,2,2)
      # plot nyquist
      h.plot2 = plot(squeeze(real(Lu)),squeeze(imag(Lu)),"r",'LineWidth',2);
      hold on

      # plot unit circle centered at (-1,0i) for stability margin analysis
      dd=0.:.001:2*pi;
      xx1=cos(dd)-1;yy1=sin(dd);
      h.circleplot = plot(xx1,yy1,'k:','LineWidth',1.5);

      # plot center of unit circle at (-1,0i)
      h.dotplot = plot(-1,0,'ko','LineWidth',0.5);
      hold off
      axis([-3,1,-2,2]);
      title("Nyquist Plot of L_u");
      xlabel("Re");
      ylabel("Im");
      grid on
      guidata (obj, h);
    # after plots are initialized, just edit the data instead of making new plots
    else
      # update step response and nyquist plots
      set (h.plot, "ydata", y);
      set (h.plot2, "xdata", squeeze(real(Lu)));
      set (h.plot2, "ydata", squeeze(imag(Lu)));
    endif
  endif

  
endfunction

## noise
h.Q_label = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "Q(1,1) Value:",
                           "horizontalalignment", "left",
                           "position", [0.05 0.4 0.35 0.08]);

h.Q_slider = uicontrol ("style", "slider",
                            "units", "normalized",
                            "string", "slider",
                            "callback", @update_plot,
                            'min', -8,                         
                            'max', 3,                        
                            "value", -3,
                            "position", [0.05 0.35 0.35 0.05]);

h.kx_label = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "Kx: ",
                           "horizontalalignment", "left",
                           "position", [0.05 0.275 0.35 0.08]);
                           
h.kx_descrip = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "Kx = [K_int,  K_prop,  K_der]",
                           "horizontalalignment", "left",
                           "position", [0.05 0.225 0.35 0.05]);


h.rise_time = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "Rise time:",
                           "horizontalalignment", "left",
                           "position", [0.5 0.4 0.55 0.05]);

h.settle_time = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "Settle time:",
                           "horizontalalignment", "left",
                           "position", [0.5 0.35 0.55 0.05]);                           

h.sv_gain_margin = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "SV Gain Margin: ",
                           "horizontalalignment", "left",
                           "position", [0.5 0.3 0.55 0.05]);       

h.sv_phase_margin = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "SV Phase Margin: ",
                           "horizontalalignment", "left",
                           "position", [0.5 0.25 0.55 0.05]);       

h.classic_gain_margin = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "Classic Gain Margin: ",
                           "horizontalalignment", "left",
                           "position", [0.5 0.2 0.55 0.05]); 

h.classic_phase_margin = uicontrol ("style", "text",
                           "units", "normalized",
                           "string", "Classic Phase Margin: ",
                           "horizontalalignment", "left",
                           "position", [0.5 0.15 0.55 0.05]); 
                           
                           
set (gcf, "color", get(0, "defaultuicontrolbackgroundcolor"))
guidata (gcf, h)
update_plot (gcf, true);
