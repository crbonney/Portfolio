close all
s = tf('s');

%% Throttle Fit Check
At = [0 1; 0 bt];
Bt = [0; ct];

Ct = [0 1];
Dt = [0];

sys = ss(At,Bt,Ct,Dt);

sim = lsim(sys,(T(bang_bang_start_t:bang_bang_end_t-1)-T_trim),time(bang_bang_start_t:bang_bang_end_t-1)-time(bang_bang_start_t));

figure;
plot(w(bang_bang_start_t+delay:bang_bang_end_t+delay-1));
hold on;
plot(sim);
legend({'actual data','lsim'});

%% Elevator Fit Check
Ae = [0 1; 0 be]*1;
Be = [0; ce]*1.3;

Ce = [0 1];
De = [0];

sys = ss(Ae,Be,Ce,De);

sim = lsim(sys,(E(bang_bang_start_e:bang_bang_end_e-1))-E_trim,time(bang_bang_start_e:bang_bang_end_e-1)-time(bang_bang_start_e));

figure;
plot(q(bang_bang_start_e+delay:bang_bang_end_e+delay-1));
hold on;
plot(sim);
legend({'actual data','lsim'});

%% Aileron Fit Check
Aa = [0 1; 0 ba]*1;
Ba = [0; ca]*1.3;

Ca = [0 1];
Da = [0];

sys = ss(Aa,Ba,Ca,Da);

sim = lsim(sys,(A(bang_bang_start_a:bang_bang_end_a-1))-A_trim,time(bang_bang_start_a:bang_bang_end_a-1)-time(bang_bang_start_a));

figure;
plot(p(bang_bang_start_a+delay:bang_bang_end_a+delay-1));
hold on;
plot(sim);
legend({'actual data','lsim'});

%% Rudder Fit Check
Ar = [0 1; 0 ba]*1;
Br = [0; ca]*1.3;

Cr = [0 1];
Dr = [0];

sys = ss(Ar,Br,Cr,Dr);

sim = lsim(sys,(Rudder(bang_bang_start_r:bang_bang_end_r-1))-R_trim,time(bang_bang_start_r:bang_bang_end_r-1)-time(bang_bang_start_r));

figure;
plot(r(bang_bang_start_r+delay:bang_bang_end_r+delay-1));
hold on;
plot(sim);
legend({'actual data','lsim'});
