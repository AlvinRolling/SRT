rng(234923);
N = 50;
nSamples = 100;
adj = gen_ba_weight(N,inf(5,5),5);
x = adj(:);
x_pos = find(x>0);
rPerm = randperm(length(x_pos));
omega = x_pos(sort(rPerm(1:nSamples)));
observations = adj(omega);    % the observed entries
mu = 0.001;        % smoothing parameter
addpath D:\matlab\SRT\TFOCS
Xk = solver_sNuclearBP({N,N,omega},observations,mu);
adj1 = round(Xk);
fprintf('Relative error, no rounding: %.8f%%\n', norm(adj-adj1,'fro')/norm(adj,'fro')*100 );