function [ P0 ] = TRANS01SF(P1, theta)

    [~,N] = size(P1);
    T01 =   [...
           cos(theta)  -sin(theta)  0  0 ;...
           sin(theta)   cos(theta)  0  0 ;...
               0             0      1  0 ;...
               0             0      0  1 ;...
    ];

    P0 = [P1; ones(1,N)];
    P0 = T01*P0;
    P0 = P0(1:3,:);


end

