function sys_y = output_system(Plant, Controller)
    % Builds output loop TF from plant system and controller system
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
    
    Aout = [ Ap Bp*Cc;  0.*Bc1*Cp Ac];
    Bout = [ Bp*Dc1; Bc1];
    Cout = -[ Cp Dp*Cc];%change sign for loop gain
    Dout = -[ Dp*Dc1];
    
    if nargout == 1
        sys_y = ss(Aout,Bout,Cout,Dout);
    elseif nargout == 4
        sys_y{1} = Aout;
        sys_y{2} = Bout;
        sys_y{3} = Cout;
        sys_y{4} = Dout;
    else
        sys_y = 'error';
    end
end