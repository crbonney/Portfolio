function sys_u = input_system(Plant, Controller)
    % Builds input loop TF from plant system and controller system
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
    
    Ain = [ Ap 0.*Bp*Cc;  Bc1*Cp Ac];
    Bin = [ Bp; Bc1*Dp];
    Cin = -[ Dc1*Cp Cc];%change sign for loop gain
    Din = -[ Dc1*Dp];
    
    if nargout == 1
        sys_u = ss(Ain,Bin,Cin,Din);
    elseif nargout == 4
        sys_u{1} = Ain;
        sys_u{2} = Bin;
        sys_u{3} = Cin;
        sys_u{4} = Din;
    else
        sys_u = 'error';
    end
end