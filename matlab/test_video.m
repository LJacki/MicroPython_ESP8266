% close all;
clear;

%% parameter declariton
hcnt = 16;
vcnt = 8;
%% meshgrid
map_v = 0:1:vcnt;
map_h = 0:1:hcnt;
[x,y] = meshgrid(map_v,map_h);
set(gca, 'color', [0 0 0]);
plot(x,y,'w')
hold on
plot(x',y','w')

%% draw pattern only one color one pixel
 for h = 0:1:hcnt-1
     for v = 0:1:vcnt-1
         draw_pixel(v, hcnt-1-h, [0.2, 0.2, 0.2]);
         pause(0.001)
     end
%      pause(0.5)
 end
 