
h = figure;
axis tight manual % this ensures that getframe() returns a consistent size
filename = 'digitalcontrol.gif';

##theta1 = ScopeData{1}.Values.Data(:,1);
##theta2 = ScopeData{1}.Values.Data(:,2);
theta1 = 0:0.1:pi;
theta2 = theta1;


frame0_links  = [...
        -.5 -.5 -.5 -.5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5;...
         .5 -.5 -.5  .5  .5  .5  .5  .5  .5 -.5 -.5 -.5 -.5 -.5 -.5  .5;...
        -15 -15 -.5 -.5 -15 -15 -.5 -.5 -.5 -.5 -.5 -.5 -15 -15 -15 -15;...
];

frame1_links = [...
         .5 -.5 -.5  .5  .5  .5  .5  .5  .5 -.5 -.5 -.5 -.5 -.5 -.5  .5;...
          8   8 -.5 -.5   8   8 -.5 -.5 -.5 -.5 -.5 -.5   8   8   8   8;...
        -.5 -.5 -.5 -.5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5 -.5  .5  .5;...
];
     
frame2_links = [...
         .2 -.2 -.2  .2  .2  .2  .2  .2  .2 -.2 -.2 -.2 -.2 -.2 -.2  .2;...
         12  12 -.5 -.5  12  12 -.5 -.5 -.5 -.5 -.5 -.5  12  12  12  12;...
        -.4 -.4 -.4 -.4 -.4   0   0 -.4   0   0 -.4   0   0 -.4   0   0;...
];

    rho = sqrt(8^2+12^2);
    phi_max = atan(12/8);

step = 2;
for (i=1:floor(length(theta1)/step))


    f1 = TransformPoints(TRANS0_1(theta1(i*step)),frame1_links);
    f2 = TransformPoints(TRANS0_1(theta1(i*step)),TransformPoints(TRANS1_2(theta2(i*step)),frame2_links));


    plot3(frame0_links(1,:),frame0_links(2,:), frame0_links(3,:),'bs-','LineWidth',3);
    axis([-15 15 -15 15 -15 15]);
    grid on
    hold on
    xlabel('x');
    ylabel('y');
    zlabel('z');
    plot3(f1(1,:),f1(2,:), f1(3,:),'rs-','LineWidth',3);
    plot3(f2(1,:),f2(2,:), f2(3,:),'go-', 'MarkerFaceColor', 'c', 'MarkerSize',5,'LineWidth',3);
    plot3(f2(1,end),f2(2,end), f2(3,end),'go-', 'MarkerFaceColor', 'c', 'MarkerSize',5,'LineWidth',3);
    axis([-15 15 -15 15 -15 15]);
%     WorkEnvelope2(rho, phi_max);
    drawnow
    
%           % Capture the plot as an image 
%       frame = getframe(h); 
%       im = frame2im(frame); 
%       [imind,cm] = rgb2ind(im,256); 
%       % Write to the GIF File 
%       if i == 1 
%           imwrite(imind,cm,filename,'gif', 'Loopcount',inf); 
%       else 
%           imwrite(imind,cm,filename,'gif','WriteMode','append'); 
%       end 
    hold off
end
