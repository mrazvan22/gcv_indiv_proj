X = [0., 0., 1.;
     1., 0., 0.; 
     2., 2., 2.; 
     3., 5., 4.];
Y = [ 0.1, -0.2; 
      0.9,  1.1; 
      6.2,  5.9; 
     11.9, 12.3];

% U,V - scores
% A, B - weights??
[A,B,r,U,V] = canoncorr(X,Y)

%plot(U(:,1),V(:,1),'.')

csvwrite('matlab_weights_X.csv',A);
csvwrite('matlab_weights_Y.csv',B);

exit();