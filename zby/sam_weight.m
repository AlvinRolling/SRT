% (weight)对原图进行随机边采样，每条边被采到概率相等

function y = sam_weight(x,sam_num)

all_edges = find(x>0);
sam_edges = all_edges(randperm(length(all_edges),sam_num));
y = zeros(length(x),1);
y(sam_edges) = x(sam_edges);

end