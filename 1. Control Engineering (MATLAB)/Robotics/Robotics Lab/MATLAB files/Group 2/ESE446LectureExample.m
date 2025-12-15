
Link1P1 = [0;0;0];
Link1P2 = [4;0;0];
Link1P3 = [4;0;1];
Link1P4 = [6;0;1];
Link1P5 = [4;0;1];
Link1P6 = [4;0;-1];
Link1P7 = [6;0;-1];

Link1Des = [Link1P1,Link1P2,Link1P3,Link1P4,Link1P5,Link1P6,Link1P7];

BaseP1 = [0;0;-10];
BaseP2 = [0;0;0];

BaseDes = [BaseP1,BaseP2];

for theta1=0:pi/60:2*pi;
    
    BaseDesX = BaseDes(1,:);
    BaseDesY = BaseDes(2,:);
    BaseDesZ = BaseDes(3,:);
    plot3(BaseDesX,BaseDesY,BaseDesZ,'rs-')
    axis([-15 15 -15 15 -15 15]);
    grid on
    hold on
    BaseLink1=TRANS01SF(Link1Des,theta1);
    BaseLink1X=BaseLink1(1,:);
    BaseLink1Y=BaseLink1(2,:);
    BaseLink1Z=BaseLink1(3,:);
    plot3(BaseLink1X,BaseLink1Y,BaseLink1Z,'b-')
    hold off
    pause(0.05)
end