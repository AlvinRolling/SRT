% (weight)���ú˷�����Frobenius������С���������Բ���ʸ�������ڽӾ���ָ�

function x1 = rec(y)

N = (sqrt(1+8*length(y))+1)/2;% length(x)=N*(N-1)/2,N^2-N-2*length(x)=0
adj1 = zeros(N,N);
ratio = 3;% ��Լ����������

cvx_begin quiet
    variable adj1(N,N)
    minimize(norm_nuc(adj1))
    subject to
        x1 = adj2edge(adj1);% ���ڽӾ���adj1(N*N)ת��Ϊ������x1[(N*(N-1)/2)*1]
        x1(logical(y)) == y(logical(y));
        sum(x1) <= sum(y)*ratio;
%         max(max(x1)) <= 1;
%         min(min(x1)) >= 0;
cvx_end

% ת��Ϊ��ɢ0-1����
% x1 = (adj2edge(adj1)+adj2edge(adj1'))/2;
% m = mean(x1);
% x1(x1>m) = 1;
% x1(x1<m) = 0;
x1 = round(x1);