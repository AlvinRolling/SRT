% ��ԭͼ��������߲�����ÿ���߱��ɵ��������

function y = sam(x,sam_num)

all_edges = find(x);
sam_edges = all_edges(randperm(length(all_edges),sam_num));
y = zeros(length(x),1);
y(sam_edges) = 1;

end