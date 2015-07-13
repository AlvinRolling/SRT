% (weighted)���ú˷�����Frobenius������С������������ԭͼ�������ڽӾ���ָ�
% function rat_sam = nuc_fro_weight(sam_vec,x)


% -----------------------
clear all;close all;clc;
% ��ʼ��
N = 50;% �ڵ���
sam_vec = 15:15:225;% ��������ʸ��
adj = gen_ba_weight(N,zeros(5,5),5);% ����ԭͼ�ڽӾ���
x = adj2edge(adj);% ���ڽӾ���adj(N*N)ת��Ϊ������x[(N*(N-1)/2)*1]

% --------------------------------------



len = length(sam_vec);% ��ͬ���������ĸ���
mse = zeros(len,1);
rat_sam = zeros(len,1);

num = 1;% �ظ�������ͬ����ʵ���ظ��Ĵ���

for idx=1:len
    disp(idx);
    for idx1=1:num
        sam_num = sam_vec(idx);
        % ����
        y = sam_weight(x,sam_num);
        % �ָ�
        x1 = rec_weight(y);
        % ����
        % �������
        mse(idx) = mse(idx)+(x1-x)'*(x1-x)/N;
        % �����ȣ�����������ԭͼ�����ı�
        rat_sam(idx) = rat_sam(idx)+sam_num/sum(x>0);
    end
    mse(idx) = mse(idx)/num;
    rat_sam(idx) = rat_sam(idx)/num;
end

% ------------------------
% ���ƹ�ϵ
plot_all_weight(mse,rat_sam);
% end