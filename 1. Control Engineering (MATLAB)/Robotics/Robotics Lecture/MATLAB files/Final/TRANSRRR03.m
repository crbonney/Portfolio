function [ P3 ] = TRANSRRR03(P0, theta, L)

    P1 = TRANSRRR(P0, theta(1), L(1));
    P2 = TRANSRRR(P1, theta(2), L(2));
    P3 = TRANSRRR(P2, theta(3), L(3));
    

end

