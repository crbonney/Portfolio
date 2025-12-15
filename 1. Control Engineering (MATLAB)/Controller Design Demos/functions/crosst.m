function t1 = crosst(a,t,error_high=true)
% Created : 11-02-09, Eugene Lavretsky
% Modified : June 2021, Chris Bonney
% % create option to return high or low value on error (defaults high)
 
 
%find the last value of t where a crosses zero
n=prod(size(a));
j=0;
i=0;

while j < n,
  if a(n-j) > 0.,
    i=n-j;
    j=n+1;
  end;
  j=j+1;
end

% Index out of bounds check (error)
if ((i) < 1 || i == n) 
    if error_high == false
    % Return rise time of 0 for error
      t1 = 0;
    else 
    % Return "infinite" rise time for error
      t1 = 10000;
    end
    return
end

pp=inv([t(i) 1.;t(i+1) 1.])*[a(i);a(i+1)];
t1=-pp(2)/pp(1);
return