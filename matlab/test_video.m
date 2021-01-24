close all;
clear;

j=0:1:10;
i=0:1:30;
[x,y] = meshgrid(i,j);
plot(x,y,'b')
hold on
plot(x',y','b')


m = [0 1 1 0 0]; %逆时针旋转一周期的5个点的横坐标
n = [0 0 1 1 0]; %逆时针旋转一周期的5个点的纵坐标
fill(m, n, 'r');

pause(0.5)

m = [1 2 2 1 ];
n = [1 1 2 2 ];
fill(m, n, 'g');

pause(0.5)

m = [2 3 3 2 ];
n = [2 2 3 3 ];
fill(m, n, 'b');

pause(0.5);

function [a, b, c, d, e] = pixel(axis)
