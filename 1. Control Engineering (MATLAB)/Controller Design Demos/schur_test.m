clear all
clc

H = [
            0  -1.1569e+03            0  -3.6080e+04  -4.0687e+01  -1.9913e+04;
            0  -1.3046e+00   1.0000e+00  -4.0687e+01  -4.5882e-02  -2.2456e+01;
            0   4.7711e+01            0  -1.9913e+04  -2.2456e+01  -1.0990e+04;
  -1.0000e-04            0            0            0            0            0;
            0            0            0   1.1569e+03   1.3046e+00  -4.7711e+01;
            0            0            0            0  -1.0000e+00            0
];

[V, Lmda] = eig(H)

k = size(Lmda,1);
i=1;
while i<=(k)
  if (real(Lmda(i,i) > 0))
    Q = eye(size(Lmda,1));
    Q(i,i) = 0;
    Q(k,k) = 0;
    Q(i,k) = 1;
    Q(k,i) = 1;
    Lmda = Q'*Lmda*Q;
    V = Q'*V*Q;
    k--;
  else
    i++;
  endif
  
end

Lmda
  
LmdaS = real(Lmda) < 0

