# MicroPython_ESP8266

之前写博客每篇文章基本是独立的，都是按照学习，记录，分享的逻辑。此次想通过有主题的系列文章，带来有稍有深度的分享。

本系列将使用MicroPython驱动ESP8266，借助贝壳物联接入天猫精灵，简易实现智能家居控制体验。

## 已有文章目录

[MicroPython_ESP8266_IoT——第一回 新手上路（开始之前要准备）.md](https://github.com/LJacki/MicroPython_ESP8266/blob/main/专栏系列文章/MicroPython_ESP8266_IoT——第一回 新手上路（开始之前要准备）.md)

[MicroPython_ESP8266_IoT——第二回 致敬点灯（一切从点灯开始）.md](https://github.com/LJacki/MicroPython_ESP8266/blob/main/专栏系列文章/MicroPython_ESP8266_IoT——第二回 致敬点灯（一切从点灯开始）.md)

[MicroPython_ESP8266_IoT——第三回 纸上得来（学习手册知识点）.md](https://github.com/LJacki/MicroPython_ESP8266/blob/main/专栏系列文章/MicroPython_ESP8266_IoT——第三回 纸上得来（学习手册知识点）.md)

[MicroPython_ESP8266_IoT——第四回 初入联网（接入了贝壳物联）.md](https://github.com/LJacki/MicroPython_ESP8266/blob/main/专栏系列文章/MicroPython_ESP8266_IoT——第四回 初入联网（接入了贝壳物联）.md)

## 新的发现

整理资料，做WOL；

https://zh.wikipedia.org/wiki/%E7%B6%B2%E8%B7%AF%E5%96%9A%E9%86%92

http://www.hackernotcracker.com/2006-04/WOL-wake-on-lan-tutorial-with-bonus-php-script.html

00-42-38-AC-42-D4

192.168.1.16


STA & AP 介绍 https://randomnerdtutorials.com/micropython-esp32-esp8266-access-point-ap/

AP状态下的默认IP地址为192.168.4.1，可以通过`ap.ifconfig()`获得。在浏览器输入对应ip地址就可以连接到对应的web。

这个发现在Micropython上的socket模块上，不能支持广播，原生的Python库是可以的。

又因为BIOS中可以设定为定时开机，也就，暂时不解决了。

## uPyCraft IDE

https://randomnerdtutorials.com/install-upycraft-ide-windows-pc-instructions/#more-74513

uPyCraft 的使用；http://docs.dfrobot.com.cn/upycraft/

## web登录wifi

相关资料：

https://www.cnblogs.com/imliubo/p/10457273.html

https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/

https://randomnerdtutorials.com/wifimanager-with-esp8266-autoconnect-custom-parameter-and-manage-your-ssid-and-password/

https://randomnerdtutorials.com/micropython-wi-fi-manager-esp32-esp8266/

Here’s how the process works:

- When the ESP32 boots for the first time, it’s set as an [Access Point](https://randomnerdtutorials.com/micropython-esp32-esp8266-access-point-ap/);
- You can connect to that Access Point by establishing a connection with the WiFiManager network and going to the IP address 192.164.4.1;
- A web page opens that allows you to choose and configure a network;
- The ESP32 saves those network credentials so that later it can connect to that network (Station mode);
- Once a new SSID and password is set, the ESP32 reboots, it is set to Station mode and tries to connect to the previously saved network;
- If it establishes a connection, the process is completed successfully. Otherwise, it will be set up as an Access Point for you to configure new network credentials.

## MciroPython + Pycharm

https://github.com/vlasovskikh/intellij-micropython github仓库地址；

https://singtown.com/learn/48860/

Device path COM5
Quit: Ctrl+] | Stop program: Ctrl+C | Reset: Ctrl+D

烧录文件和串口打印的时候不能占用串口，所以如果不用REPL，使用Ctrl + ]退出串口占用；

## DHT模块

只有DHT模块工作的时候，间隔至少5s，不会引起dht设备测量异常。

如果只有中断情况下，会不会退出？

需要在加入贝壳物联后检测是否在线。

