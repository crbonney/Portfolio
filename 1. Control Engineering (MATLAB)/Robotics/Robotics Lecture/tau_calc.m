function Tau = tau_calc(Gravity,Q)

SFric1=0;
DFric1=200;
SFric2=0;
DFric2=150;
SFric3=0;
DFric3=100;

grav=Gravity;

q1 = Q(1);
q2 = Q(3);
q3 = Q(5);
q1dot = Q(2);
q2dot = Q(4);
q3dot = Q(6);

Vq = [...
      - q3dot*(40*q2dot*sin(q2 + q3) + q3dot*(40*sin(q2 + q3) + 30*sin(q3))) - q2dot*(q3dot*(40*sin(q2 + q3) + 60*sin(q3)) + q2dot*(40*sin(q2 + q3) + 210*sin(q2))) - q1dot*(q3dot*(80*sin(q2 + q3) + 60*sin(q3)) + q2dot*(80*sin(q2 + q3) + 420*sin(q2)));...
      210*q1dot^2*sin(q2) - 30*q3dot^2*sin(q3) + 40*q1dot^2*sin(q2 + q3) - 60*q1dot*q3dot*sin(q3) - 60*q2dot*q3dot*sin(q3);...
      30*q1dot^2*sin(q3) + 30*q2dot^2*sin(q3) + 40*q1dot^2*sin(q2 + q3) + 60*q1dot*q2dot*sin(q3);...
];

Gq = [...
      (5*grav*(4*cos(q1 + q2 + q3) + 21*cos(q1 + q2) + 56*cos(q1)))/2;...
      (105*grav*cos(q1 + q2))/2 + 10*grav*cos(q1 + q2 + q3);...
      10*grav*cos(q1 + q2 + q3);...
];


F1=SFric1*sign(q1dot) + DFric1*q1dot;
F2=SFric2*sign(q2dot) + DFric2*q2dot;
F3=SFric3*sign(q3dot) + DFric3*q3dot;
Fq=[F1;F2;F3];

Tau = Vq + Gq + Fq;

end