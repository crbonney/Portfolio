function [P] = TransformPoints(TM,Pv)

    [M,N] = size(Pv);
    P = [Pv; ones(1,N)];
    P = TM*P;
    P = P(1:3,:);
end
