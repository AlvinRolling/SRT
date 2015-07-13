% (weight)利用核范数与Frobenius范数最小化方法，对采样矢量进行邻接矩阵恢复

function x1 = rec(y)

N = (sqrt(1+8*length(y))+1)/2;% length(x)=N*(N-1)/2,N^2-N-2*length(x)=0
adj1 = zeros(N,N);
ratio = 3;% 边约束比例参数

cvx_begin quiet
    variable adj1(N,N)
    minimize(norm_nuc(adj1))
    subject to
        x1 = adj2edge(adj1);% 将邻接矩阵adj1(N*N)转化为边序列x1[(N*(N-1)/2)*1]
        x1(logical(y)) == y(logical(y));
        sum(x1) <= sum(y)*ratio;
%         max(max(x1)) <= 1;
%         min(min(x1)) >= 0;
cvx_end

% 转化为离散0-1矩阵
% x1 = (adj2edge(adj1)+adj2edge(adj1'))/2;
% m = mean(x1);
% x1(x1>m) = 1;
% x1(x1<m) = 0;
x1 = round(x1);