% 利用核范数与Frobenius范数最小化方法，进行原图采样和邻接矩阵恢复

function [pro_01 pro_10 rat_sam] = nuc_fro(sam_vec,x)

len = length(sam_vec);% 不同采样边数的个数
pro_01 = zeros(len,1);
pro_10 = zeros(len,1);
rat_sam = zeros(len,1);

num = 10;% 重复次数，同参数实验重复的次数

for idx=1:len
    disp(idx);
    for idx1=1:num
        sam_num = sam_vec(idx);
        % 采样
        y = sam(x,sam_num);
        % 恢复
        x1 = rec(y);
        % 评价
        % 虚警概率，原图不连边中新图连边所占比例
        pro_01(idx) = pro_01(idx)+length(find(x1&~x))/length(find(~x));
        % 漏报概率，原图连边中新图不连边所占比例
        pro_10(idx) = pro_10(idx)+length(find(~x1&x))/length(find(x));
        % 采样比，采样边数与原图边数的比
        rat_sam(idx) = rat_sam(idx)+sam_num/sum(x);
    end
    pro_01(idx) = pro_01(idx)/num;
    pro_10(idx) = pro_10(idx)/num;
    rat_sam(idx) = rat_sam(idx)/num;
end

end