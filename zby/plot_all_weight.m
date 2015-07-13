% (weight)绘制均方误差与采样比的函数关系

function plot_all_weight(mse,rat_sam)

hold on
plot(rat_sam,mse);
hold off
xlabel('采样比');
ylabel('均方误差');

end