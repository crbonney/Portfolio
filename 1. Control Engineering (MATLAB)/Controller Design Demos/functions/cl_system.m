function [sys_cl] = cl_system(Plant, Controller)
    % Builds closed loop system from plant system and controller system
    % for ONE output: system object
    % for FOUR outputs: individual matrices
    % any other number of outputs results in error

    Ap = Plant.A;
    Bp = Plant.B;
    Cp = Plant.C;
    Dp = Plant.D;
    
    Ac  = Controller.Ac;
    Bc1 = Controller.Bc1;
    Bc2 = Controller.Bc2;
    Cc  = Controller.Cc;
    Dc1 = Controller.Dc1;
    Dc2 = Controller.Dc2;
    
    Z = inv(eye(size(Dc1*Dp))-Dc1*Dp);
    Acl = [     (Ap+Bp*Z*Dc1*Cp)              (Bp*Z*Cc);
        (Bc1*(Cp+Dp*Z*Dc1*Cp))  (Ac+Bc1*Dp*Z*Cc)];
    Bcl = [       Bp*Z*Dc2;
        (Bc2+Bc1*Dp*Z*Dc2)];
    Ccl = [(Cp+Dp*Z*Dc1*Cp) (Dp*Z*Cc)];
    Dcl =(Dp*Z*Dc2);

    if nargout == 1
        sys_cl = ss(Acl,Bcl,Ccl,Dcl);    
    elseif nargout == 4
        sys_cl{1} = Acl;
        sys_cl{2} = Bcl;
        sys_cl{3} = Ccl;
        sys_cl{4} = Dcl;
    else
        sys_cl = 'error';
    end
end

