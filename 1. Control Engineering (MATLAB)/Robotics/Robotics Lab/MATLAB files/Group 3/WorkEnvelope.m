function [ envelope ] = WorkEnvelope(end_effector, T01, T12)

axis tight

frame0_links = ...
    [0  0;...  %X
     0  0;...  %Y
     0 -15];   %Z

frame1_links = ...
    [0  0  0  0 0;... %X
     0  0  6  6 8;... %Y
     0 -1 -1  0 0];   %Z

frame2_links = ...
    [0   0;... %X
     0  12;... %Y
     0   0];   %Z

envelope = [];

##filename = 'make_envelope.gif';

h = figure;
for theta1=linspace(0,2*pi,20)
    for theta2=linspace(0,2*pi,50);

        f1 = TransformPoints(TRANS0_1(theta1),frame1_links);
        f2 = TransformPoints(TRANS0_1(theta1),TransformPoints(TRANS1_2(theta2),frame2_links));

        f3 = TransformPoints(T01(theta1),TransformPoints(T12(theta2),end_effector));
        envelope = [envelope, f3(:,end)];  
        
        plot3(frame0_links(1,:),frame0_links(2,:), frame0_links(3,:),'bs-','LineWidth',3);
        axis([-15 15 -15 15 -15 15]);
        grid on
        hold on
        xlabel('x');
        ylabel('y');
        zlabel('z');
        plot3(f1(1,:),f1(2,:), f1(3,:),'rs-','LineWidth',3);
        plot3(f2(1,:),f2(2,:), f2(3,:),'go-', 'MarkerFaceColor', 'c', 'MarkerSize',5,'LineWidth',3);        
        plot3(envelope(1,:), envelope(2,:), envelope(3,:));
        hold off
        drawnow
        
##        % Capture the plot as an image 
##        frame = getframe(h); 
##        im = frame2im(frame); 
##        [imind,cm] = rgb2ind(im,256); 
##
##          if theta1 == 0 
##              imwrite(imind,cm,filename,'gif', 'Loopcount',inf); 
##          else 
##              imwrite(imind,cm,filename,'gif','WriteMode','append'); 
##          end 
        
    end
end

end