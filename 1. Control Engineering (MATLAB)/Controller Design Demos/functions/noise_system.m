function sys_v = noise_system(Plant, Controller)
    % Builds noise-to-control TF from plant system, controller, and closed
    % loop system
    
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

    Bv = [       Bp*Z*Dc1;
        (Bc1+Bc1*Dp*Z*Dc1)];
    Cv  = [ Z*Dc1*Cp Z*Cc];
    Cvv = [ Cv ; Cv*Acl ];
    Dv = Z*Dc1;
    Dvv = [ Dv; Cv*Bv];
    
    if nargout == 1
        sys_v = ss(Acl,Bv,Cvv,Dvv);
    elseif nargout == 4
        sys_v{1} = Acl;
        sys_v{2} = Bv;
        sys_v{3} = Cvv;
        sys_v{4} = Dvv;
    else
        sys_v = 'error';
    end
end