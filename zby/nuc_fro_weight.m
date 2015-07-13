% (weighted)利用核范数与Frobenius范数最小化方法，进行原图采样和邻接矩阵恢复
% function rat_sam = nuc_fro_weight(sam_vec,x)


% -----------------------
clear all;close all;clc;
% 初始化
N = 50;% 节点数
sam_vec = 15:15:225;% 采样边数矢量
adj = gen_ba_weight(N,zeros(5,5),5);% 生成原图邻接矩阵
x = adj2edge(adj);% 将邻接矩阵adj(N*N)转化为边序列x[(N*(N-1)/2)*1]

% --------------------------------------



len = length(sam_vec);% 不同采样边数的个数
mse = zeros(len,1);
rat_sam = zeros(len,1);

num = 1;% 重复次数，同参数实验重复的次数

for idx=1:len
    disp(idx);
    for idx1=1:num
        sam_num = sam_vec(idx);
        % 采样
        y = sam_weight(x,sam_num);
        % 恢复
        x1 = rec_weight(y);
        % 评价
        % 均方误差
        mse(idx) = mse(idx)+(x1-x)'*(x1-x)/N;
        % 采样比，采样边数与原图边数的比
        rat_sam(idx) = rat_sam(idx)+sam_num/sum(x>0);
    end
    mse(idx) = mse(idx)/num;
    rat_sam(idx) = rat_sam(idx)/num;
end

% ------------------------
% 绘制关系
plot_all_weight(mse,rat_sam);
% end