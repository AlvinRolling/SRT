% 主函数

clear all;close all;clc;

% 初始化
N = 50;% 节点数
sam_vec = 5:11:225;% 采样边数矢量
adj = gen_ba(N,zeros(5,5),5);% 生成原图邻接矩阵
x = adj2edge(adj);% 将邻接矩阵adj(N*N)转化为边序列x[(N*(N-1)/2)*1]

% 采样恢复
[pro_01 pro_10 rat_sam] = nuc_fro(sam_vec,x);

% 绘制关系
plot_all(pro_01,pro_10,rat_sam);