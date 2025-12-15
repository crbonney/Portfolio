function  WorkEnvelope2( Rho, phi_max )

    
    Phi=linspace(-phi_max,phi_max);
    Theta=linspace(0,2*pi);
    [Phi,Theta]=meshgrid(Phi,Theta);
    [X,Y,Z]=sph2cart(Theta,Phi,Rho);
    % Z=R*sin(Phi);
    % X=R*cos(Phi).*cos(Theta);
    % Y=R*cos(Phi).*sin(Theta);
    surf(X,Y,Z, 'EdgeColor', 'none');
    alpha 0.5
end

