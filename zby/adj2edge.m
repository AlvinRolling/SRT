% ���ڽӾ���(N*N)ת��Ϊ������[(N*(N-1)/2)*1]

function x = adj2edge(adj)

N = size(adj,1);
idx = reshape(repmat(1:N,N,1)',N*N,1)>reshape(repmat(1:N,N,1),N*N,1);
x = adj(idx);

end