% 绘制虚警概率、漏报概率与采样比的函数关系

function plot_all(pro_01,pro_10,rat_sam)

hold on
plot(rat_sam,pro_01);
plot(0,1,'k');
hold off
xlabel('采样比');
ylabel('虚警概率');

figure;
hold on
plot(rat_sam,pro_10);
plot(0.0:0.1:1.0,1.0:-0.1:0.0,'r');
hold off
xlabel('采样比');
ylabel('漏报概率');

end