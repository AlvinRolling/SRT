% (weight)��ԭͼ��������߲�����ÿ���߱��ɵ��������

function y = sam_weight(x,sam_num)

all_edges = find(x>0);
sam_edges = all_edges(randperm(length(all_edges),sam_num));
y = zeros(length(x),1);
y(sam_edges) = x(sam_edges);

end