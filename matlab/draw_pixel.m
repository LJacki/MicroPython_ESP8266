function draw_pixel(x, y, colour)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
m = [x x+1 x+1 x ];%逆时针旋转一周期的5个点的横坐标
n = [y y y+1 y+1 ];%逆时针旋转一周期的5个点的纵坐标
fill(m, n, colour);
end

