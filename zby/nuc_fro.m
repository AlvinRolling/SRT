% ���ú˷�����Frobenius������С������������ԭͼ�������ڽӾ���ָ�

function [pro_01 pro_10 rat_sam] = nuc_fro(sam_vec,x)

len = length(sam_vec);% ��ͬ���������ĸ���
pro_01 = zeros(len,1);
pro_10 = zeros(len,1);
rat_sam = zeros(len,1);

num = 10;% �ظ�������ͬ����ʵ���ظ��Ĵ���

for idx=1:len
    disp(idx);
    for idx1=1:num
        sam_num = sam_vec(idx);
        % ����
        y = sam(x,sam_num);
        % �ָ�
        x1 = rec(y);
        % ����
        % �龯���ʣ�ԭͼ����������ͼ������ռ����
        pro_01(idx) = pro_01(idx)+length(find(x1&~x))/length(find(~x));
        % ©�����ʣ�ԭͼ��������ͼ��������ռ����
        pro_10(idx) = pro_10(idx)+length(find(~x1&x))/length(find(x));
        % �����ȣ�����������ԭͼ�����ı�
        rat_sam(idx) = rat_sam(idx)+sam_num/sum(x);
    end
    pro_01(idx) = pro_01(idx)/num;
    pro_10(idx) = pro_10(idx)/num;
    rat_sam(idx) = rat_sam(idx)/num;
end

end