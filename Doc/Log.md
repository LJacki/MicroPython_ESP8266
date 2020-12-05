# MicroPython_ESP8266
一步一步，使用ESP8266来学习MicroPython.

COM口的波特率可以通过资源管理器进行设置。

使用最新版的手册MicroPython V1.13，更新日期为 04 Dec 2020.

使用之前，需要准备的硬件：

ESP8266模块；

MicroUSB的数据线（一定要确保可以传输数据，普通的给充电宝使用的可能只能供电）；

一台已经安装Python3环境的Windows电脑；

需要的软件：

MicroPython File Uploader.exe（基于串口烧录的MicroPython交互解释器）

最有效的参考资料：

官网的参考手册

默认已经有了这样的一个环境；

## 获取固件

像电脑一样，首先需要获取一个叫做固件的东西，可以看成是电脑系统的编译文件，并且把它烧录在ESP82666上。当前最新版本为esp8266-20200911-v1.13.bin；下载地址：

http://micropython.org/download/esp8266/

注意要根据ESP8266Flash的大小进行选取；

## 部署固件

需要USB数据线，使用串口转换（板载上有CH340或者PL2102）；

使用pip安装esptool

```bash
pip install esptool
```

将ESP8266插入电脑；

在任务管理器中找到COM，

需要在esptool.py的目录下进行擦除和烧录；

烧录：

```bash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
```

拒绝访问需要按一下RST；

通过串口访问，UART0 (GPIO1=TX, GPIO3=RX)，这个在板子上有；

烧录好之后，处于WIFI access point（AP）状态，可以从WIFI中找到；

## 使用 REPL prompt

有两种进入交互解释器的途径，一种是通过UART串口，一种是通过WIFI（这个我以前不知道）；

通过串口就是使用一些串口工具，使用WIFI就需要连接如同一个局域网下进行操作；

http://micropython.org/webrepl/

打印hello world；点灯；

一些功能，ctrl a，ctrl e；输入历史，tab自动补全；

续行和索引；

灯循环闪烁

## 内部系统文件

文件操作

文件列表

查看boot.py中有什么内容；

## 网络

STA和AP

以及后面的其他功能；
