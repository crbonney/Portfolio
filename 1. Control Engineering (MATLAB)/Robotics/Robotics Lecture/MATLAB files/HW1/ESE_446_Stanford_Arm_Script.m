function ESE_446_Stanford_Arm_Script(input)

theta1 = input(1);
theta2 = input(2);
d3     = input(3);
theta4 = input(4);
theta5 = input(5);
theta6 = input(6);

origin = [0;0;0];

% axis  = [...
%           0   0   0   0   1;...
%           0   0   1   0   0;...
%           1   0   0   0   0;...
% ];

Base  = [...
         -1  -1  -1  -1  -1   1   1  -1   1   1  -1   1   1  -1   1   1;...
          1  -1  -1   1   1   1   1   1   1  -1  -1  -1  -1  -1  -1   1;...
        -15 -15  -1  -1 -15 -15  -1  -1  -1  -1  -1  -1 -15 -15 -15 -15;...
];

Link1 = [...
          1  -1  -1   1   1   1   1   1   1  -1  -1  -1  -1  -1  -1   1;...
          1   1  -1  -1   1   1  -1  -1  -1  -1  -1  -1   1   1   1   1;...
         -1  -1  -1  -1  -1   1   1  -1   1   1  -1   1   1  -1   1   1;...
];

% Link1 = [...
%          .5 -.5 -.5  .5  .5  .5  .5  .5  .5 -.5 -.5 -.5 -.5 -.5 -.5  .5;...
%           2   2   1   1   2   2   1   1   1   1   1   1   2   2   2   2;...
%         -.5 -.5 -.5 -.5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5;...
% ];

Link2 = [...
          1  -1  -1   1   1   1   1   1   1  -1  -1  -1  -1  -1  -1   1;...
          1   1  -1  -1   1   1  -1  -1  -1  -1  -1  -1   1   1   1   1;...
         -1  -1  -1  -1  -1   1   1  -1   1   1  -1   1   1  -1   1   1;...
];

%no visible link in model
Link3 = [0;0;0];

Link4 = [...
        -.5 -.5 -.5 -.5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5;...
         .5 -.5 -.5  .5  .5  .5  .5  .5  .5 -.5 -.5 -.5 -.5 -.5 -.5  .5;...
        -15 -15  -1  -1 -15 -15  -1  -1  -1  -1  -1  -1 -15 -15 -15 -15;...
];

Link5 = [...
          1  -1  -1   1   1   1   1   1   1  -1  -1  -1  -1  -1  -1   1;...
          1   1  -1  -1   1   1  -1  -1  -1  -1  -1  -1   1   1   1   1;...
         -1  -1  -1  -1  -1   1   1  -1   1   1  -1   1   1  -1   1   1;...
];

Link6 = [...
        -.5 -.5 -.5 -.5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5;...
         .5 -.5 -.5  .5  .5  .5  .5  .5  .5 -.5 -.5 -.5 -.5 -.5 -.5  .5;...
          5   5   1   1   5   5   1   1   1   1   1   1   5   5   5   5;...
];

axes  = [...
         0 1.5 0  0  0  0  0;...
         0  0  0 1.5 0  0  0;...
         0  0  0  0  0 1.5 0;...
];

BaseLink1= TRANS01SF(Link1 ,theta1);

Link12   = TRANS12SF(Link2 ,theta2);
BaseLink2= TRANS01SF(Link12,theta1);
BaseLink2O = TRANS01SF(TRANS12SF(origin,theta2),theta1);

%no visible links
%   Link23   = TRANS23SF(Link3 ,d3    );
%   Link13   = TRANS12SF(Link23,theta2);
%   BaseLink3= TRANS01SF(Link13,theta1);

BaseLink3O = TRANS01SF(TRANS12SF(TRANS23SF(origin,d3),theta2),theta1);

Link34   = TRANS34SF(Link4 ,theta4);
Link24   = TRANS23SF(Link34,d3    );
Link14   = TRANS12SF(Link24,theta2);
BaseLink4= TRANS01SF(Link14,theta1);

Link45   = TRANS45SF(Link5 ,theta5);
Link35   = TRANS34SF(Link45,theta4);
Link25   = TRANS23SF(Link35,d3    );
Link15   = TRANS12SF(Link25,theta2);
BaseLink5= TRANS01SF(Link15,theta1);

Link56   = TRANS56SF(Link6 ,theta6);
Link46   = TRANS45SF(Link56,theta5);
Link36   = TRANS34SF(Link46,theta4);
Link26   = TRANS23SF(Link36,d3    );
Link16   = TRANS12SF(Link26,theta2);
BaseLink6= TRANS01SF(Link16,theta1);

Link67   = TRANS67SF(axes         );
Link57   = TRANS56SF(Link67,theta6);
Link47   = TRANS45SF(Link57,theta5);
Link37   = TRANS34SF(Link47,theta4);
Link27   = TRANS23SF(Link37,d3    );
Link17   = TRANS12SF(Link27,theta2);
BaseEOAT = TRANS01SF(Link17,theta1);

plot3(Base(1,:),Base(2,:),Base(3,:),'k-')
axis([-15 15 -15 15 -15 15]);
grid on
hold on
plot3(BaseLink1(1,:),BaseLink1(2,:),BaseLink1(3,:),'b-')
plot3(BaseLink2(1,:),BaseLink2(2,:),BaseLink2(3,:),'g-')
%   plot3(BaseLink3(1,:),BaseLink3(2,:),BaseLink3(3,:),'k-')
plot3(BaseLink4(1,:),BaseLink4(2,:),BaseLink4(3,:),'m-')
plot3(BaseLink5(1,:),BaseLink5(2,:),BaseLink5(3,:),'b-')
plot3(BaseLink6(1,:),BaseLink6(2,:),BaseLink6(3,:),'k-')
plot3(BaseLink2O(1,:),BaseLink2O(2,:),BaseLink2O(3,:),'r*')
plot3(BaseLink3O(1,:),BaseLink3O(2,:),BaseLink3O(3,:),'r*')
plot3(axes(1,:),   axes(2,:),   axes(3,:),   'r-')
plot3(axes(1,1),   axes(2,1),   axes(3,1),   'r*')
plot3(BaseEOAT(1,:), BaseEOAT(2,:), BaseEOAT(3,:), 'r-')
plot3(BaseEOAT(1,1), BaseEOAT(2,1), BaseEOAT(3,1), 'r*')

hold off

end