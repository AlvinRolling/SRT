% ������

clear all;close all;clc;

% ��ʼ��
N = 50;% �ڵ���
sam_vec = 5:11:225;% ��������ʸ��
adj = gen_ba(N,zeros(5,5),5);% ����ԭͼ�ڽӾ���
x = adj2edge(adj);% ���ڽӾ���adj(N*N)ת��Ϊ������x[(N*(N-1)/2)*1]

% �����ָ�
[pro_01 pro_10 rat_sam] = nuc_fro(sam_vec,x);

% ���ƹ�ϵ
plot_all(pro_01,pro_10,rat_sam);