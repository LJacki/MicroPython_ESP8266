% close all;
clear;

j=0:1:64;
i=0:1:128;
[x,y] = meshgrid(i,j);
set(gca, 'color', [0 0 0]);
plot(x,y,'w')
hold on
plot(x',y','w')

 for i = 0:1:128
     for j = 0:1:64
         draw_pixel(i, j, 'g');
         pause(0.001)
     end
 end

 for i = 42:1:80
     for j = 0:1:15
         draw_pixel(i, j, 'r');
         pause(0.001)
     end
 end
 
