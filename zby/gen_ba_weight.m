% generate uniformly_weighted adjacency matrix with BA-model

function adj = gen_ba_weight(N,adj0,m)

% Growth
n0 = size(adj0,1);
adj = zeros(N,N);
adj(1:n0,1:n0) = adj0;
degp = zeros(N,1);
degcump = [[1:n0]'./n0;ones(N-n0,1)];

% Preferential attachment
for k1=1:N-n0
    % Link m distinct edges
    link_edges = zeros(m,1);
    for k2=1:m
        link_edges(k2) = sum(degcump<=rand(1))+1;
        while sum(link_edges==link_edges(k2))>1
            link_edges(k2) = sum(degcump<=rand(1))+1;
        end
        tmp = rand(1);
        adj(k1+n0,link_edges(k2)) = tmp;
        adj(link_edges(k2),k1+n0) = tmp;
    end
    degp = sum(abs(adj)>0)';
    degp = degp./sum(degp);
    degcump = cumsum(degp);
end
end