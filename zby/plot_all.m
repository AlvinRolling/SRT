% �����龯���ʡ�©������������ȵĺ�����ϵ

function plot_all(pro_01,pro_10,rat_sam)

hold on
plot(rat_sam,pro_01);
plot(0,1,'k');
hold off
xlabel('������');
ylabel('�龯����');

figure;
hold on
plot(rat_sam,pro_10);
plot(0.0:0.1:1.0,1.0:-0.1:0.0,'r');
hold off
xlabel('������');
ylabel('©������');

end