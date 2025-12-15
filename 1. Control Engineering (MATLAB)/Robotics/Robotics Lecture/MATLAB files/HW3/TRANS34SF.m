function [ P3 ] = TRANS34SF(P4, theta)

    [~,N] = size(P4);
    T34 =   [...
           cos(theta)  -sin(theta)  0  0 ;...
           sin(theta)   cos(theta)  0  0 ;...
               0             0      1  0 ;...
               0             0      0  1 ;...
    ];

    P3 = [P4; ones(1,N)];
    P3 = T34*P3;
    P3 = P3(1:3,:);


end

