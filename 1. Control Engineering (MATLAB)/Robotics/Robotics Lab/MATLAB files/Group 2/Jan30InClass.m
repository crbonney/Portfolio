
close all;

frame0_links = [0 0 0;...
                0 0 -5];

frame1_links = [0 0 0; ...
                0 0 -1; ...
                0 6 -1; ...
                0 6 0; ...
                0 8 0];
               %X Y Z

frame2_links = [0 0 0; ...
                0 12 0];

theta1 = pi/4;
theta2 = pi/2;

            
figure;
plot3(frame1_links(:,1),frame1_links(:,2), frame1_links(:,3));

% TM0_1 = @(theta) [cos(theta) -sin(theta) 0 0;...
%                   sin(theta)  cos(theta) 0 0;...
%                   0               0      1 0;...
%                   0               0      0 1];

TRANS0_1 = @(P_1,theta) [[[cos(theta) -sin(theta) 0 0;...
                           sin(theta)  cos(theta) 0 0;...
                           0               0      1 0;...
                           0               0      0 1]...
                           *[P_1; 1]]'*[1 0 0; 0 1 0; 0 0 1; 0 0 0]]';
L = 8;
                       
TRANS1_2 = @(P_2,theta) [[[cos(theta) -sin(theta) 0 0;...
                           0               0     -1 L;...
                           sin(theta)  cos(theta) 0 0;...
                           0               0      0 1]...
                           *[P_2; 1]]'*[1 0 0; 0 1 0; 0 0 1; 0 0 0]]';


%P_0 = TRANS0_1(TRANS1_2(P_2,theta2), theta1);

figure;
plot3(frame0_links(:,1),frame0_links(:,2), frame0_links(:,3));
      

frame1_2_links = frame2_links;
for i=1:size(frame1_2_links,1)
   frame1_2_links(i,:) = TRANS1_2(frame1_2_links(i,:)',theta2);
    
end

frame1_links = [frame1_links; frame1_2_links];

frame0_1_links = frame1_links;
for i=1:size(frame0_1_links,1)
   frame0_1_links(i,:) = TRANS0_1(frame0_1_links(i,:)',theta1); 
    
end
frame0_links = [frame0_links; frame0_1_links];


figure;
plot3(frame0_links(:,1),frame0_links(:,2), frame0_links(:,3));