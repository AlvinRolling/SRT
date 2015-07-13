% 将边序列[(N*(N-1)/2)*1]转化为邻接矩阵(N*N)

function adj = edge2adj(x)

N = (sqrt(1+8*length(x))+1)/2;% length(x)=N*(N-1)/2,N^2-N-2*length(x)=0
idx = reshape(repmat(1:N,N,1)',N*N,1)>reshape(repmat(1:N,N,1),N*N,1);
adj = zeros(N,N);
adj(idx) = x;
adj = adj+adj';

end