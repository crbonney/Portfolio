%% Elevator Decoupled
%X,u,theta,q
Aelevator
Belevator
%u,q
Celevator
Delevator

%% Elevator controller
%u,theta,q
Aelevator(2:end,2:end)
Belevator(2:end)
%u,q
Celevator(:,2:end)
Delevator

%% Rudder Decoupled
%Psi,r
Arudder
Brudder
%r
Crudder
Drudder

%% Rudder Controller
%r
Arudder(2,2)
Brudder(2)
%r
Crudder(1,2)
Drudder

%% Throttle Decoupled/Controller
%Z,w
Athrust
Bthrust
%Z
Cthrust
Dthrust

