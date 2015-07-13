% 将邻接矩阵(N*N)转化为边序列[(N*(N-1)/2)*1]

function x = adj2edge(adj)

N = size(adj,1);
idx = reshape(repmat(1:N,N,1)',N*N,1)>reshape(repmat(1:N,N,1),N*N,1);
x = adj(idx);

end