## 第二回 致敬点灯（一切从点灯开始）

续接上回，接着折腾，接着学。

## ESP8266通用信息

ESP8266是Espressif Systems推出的一种流行的，具有WiFi功能的片上系统（SoC）。相关的Datasheet可以在[这里下载](https://sharewow.lanzous.com/b00u1gt5c) （密码参考第一回内容）。

MicroPython for ESP8266库（应该叫方法）中的Pin number都是基于ESP8266的芯片，而不是ESP8266模块引出的引脚（意思就是不是那焊接的两排排针的序号）。在网络上找到了一张适配的引脚接线图（花了好长时间），可以适配于ESP8266模块和ESP8266的芯片，这张图放的是原图，可以直接下载保存：

<img src="https://gitee.com/sharewow/pic_repo/raw/master/img/NODEMCU_DEVKIT_V1.0_PINMAP.png" alt="NODEMCU_DEVKIT_V1.0_PINMAP" style="zoom:50%;" />

为了后面使用方便，下里提供一些技术规格：

- CPU频率：80 MHz，可以超频至160 MHz（是不是一听到超频就激动满满）；
- 总可用RAM：94KB（部分预留给系统）；
- 外部FlashROM：存放程序和数据，通过SPI烧录FLash，当前模块挂在的胃4 MB；
- GPIO：16 + 1（GPIOs 可复用为其他功能，包括外部FlashROM，UART，深睡唤醒等等）；
- UART：一组收发UART（无硬件握手协议），一组只有TX的UART；
- SPI：2组SPI接口（一组用于FlashROM）；
- I2C：无外部I2C（在任何引脚上均可以实现）；
- 编程：使用UART的Boot ROM引导程序。

### 内部资源限制

ESP8266芯片的片上资源非常有限（RAM），因此建议避免分配太多的容量给对象（list列表，dictionaries字典），使用完文件系统，sockets等要注意及时关闭。

关于ESP8266启动进程，Real-time clock，Sockets 和 WiFi buffer 溢出，SSL/TLS限制的信息，可参考[官方文档](http://docs.micropython.org/en/latest/esp8266/general.html) ，此处不再赘述。

## 电脑识别串口

将ESP8266模块通过MicroUSB线缆，与PC连接。默认此时已经完成了ESP8266模块的上电操作。

电脑端应该已经识别了ESP8266模块上的串口芯片，如果在资源管理器中看到对应的COM口出现感叹号，就必须要安装串口相关驱动了（这个之前有提到过）。下图所示的状态就是已经识别并成功安装驱动：

![驱动安装识别](https://gitee.com/sharewow/pic_repo/raw/master/img/%E9%A9%B1%E5%8A%A8%E5%AE%89%E8%A3%85%E8%AF%86%E5%88%AB.png)

也可以在CMD控制台中输入`mode` 指令：

```bash
C:\Users\Administrator>mode
```

控制台中就会列举出已经连接的串口，如下图所示：

<img src="https://gitee.com/sharewow/pic_repo/raw/master/img/%E6%8E%A7%E5%88%B6%E5%8F%B0%20COM%E5%8F%A3.png" alt="控制台 COM口" style="zoom:50%;" />

#### 串口波特率修改方式

串口波特率如果不是115200，可以在设备管理器中进行修改，操作步骤如下（这个GIF制作的设置不动的颜色默认为绿色，不过不影响内容表达）：

![COM config](https://gitee.com/sharewow/pic_repo/raw/master/img/COM%20config.gif)

## 获取和烧录固件

### 获取固件

固件（firmware）可以理解为电脑的系统，有三种版本，适配不同的外挂Flash大小；本系列ESP8266模块外挂Flash大小为4M，所以可以选用Stable firmware，[这里是下载地址](http://micropython.org/download/esp8266/) （如果无法下载或下载过慢，之前的LZ网盘连接里面也有此固件下载）选择最新版的即可：

- esp8266-20200911-v1.13.bin (elf, map) (latest)

### 烧录固件

需要使用esptool工具来烧录刚才下载好的固件。

#### 安装esptool

在CMD控制台中使用`pip` 工具安装esptool。pip为Python解释器的工具，此处使用python 3，对应指令应修改为：

```bash
pip3 install esptool
```

如果提示pip需要更新，可按照提示指令将pip更新为最新版本。

安装好之后键入`esptool.py version` ，可以查看当前工具版本：

```bash
C:\Users\Administrator>esptool.py version
esptool.py v2.6
2.6
```

这样，就可以愉快的使用此工具进行ESP8266的固件烧录了。

#### 擦除Flash

可以使用这样的命令清除ESP8266模块上flash内容（现在端口修改为COM8）：

```bash
esptool.py --port COM8 erase_flash
```

如果擦除成功控制台会出现下面的提示：

```bash
C:\Python3\Lib\site-packages>esptool.py --port COM8 erase_flash
esptool.py v2.6
Serial port COM8
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
MAC: b4:e6:2d:34:ae:9d
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 9.2s
Hard resetting via RTS pin...

C:\Python3\Lib\site-packages>
```

如果命令行执行一直显示`serial.serialutil.SerialException: could not open port 'COM8': PermissionError(13, '拒绝访问。', None, 5)` ，有两点建议：

1. 命令行切换到esptool.py的安装目录：`C:\Python3\Lib\site-packages>` ;
2. 重新对ESP8266模块重新上电。

直至出现烧录，结束之后可以通过板载的`RST`按钮进行复位。

#### 可以烧录啦

接着刚才的目录，将firmware文件`esp8266-20200911-v1.13.bin` 拷贝到该目录下，在控制台中执行：

```bash
esptool.py --port COM8 --baud 460800 write_flash --flash_size=detect 0 esp8266-20200911-v1.13.bin
```

成功安装将得到的结果如下：

```bash
C:\Python3\Lib\site-packages>esptool.py --port COM8 --baud 460800 write_flash --flash_size=detect 0 esp8266-20200911-v1.13.bin
esptool.py v2.6
Serial port COM8
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
MAC: b4:e6:2d:34:ae:9d
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Flash params set to 0x0040
Compressed 638928 bytes to 419659...
Wrote 638928 bytes (419659 compressed) at 0x00000000 in 9.4 seconds (effective 541.1 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...

C:\Python3\Lib\site-packages>
```

而且， 烧录成功默认ESP8266处于AP状态，也就是说可以打开手机或电脑WIFI搜索，搜索到以MicroPython-xxxxxx形式存在的WIFI，这种连接方式作用于下一小节，通过WIFI连接REPL prompt。

如果未能成功安装，详细的排查方案参考这里[解决安装问题](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#troubleshooting-installation-problems) 。笔者提供两个检查方法：

1. 检查命令行格式是否正确；
2. 检查检查端口是否识别，可以先进行擦除，擦除成功后紧接着进行烧录；

固件烧录成功，也就意味着已经安装好解释器了，可以对输入的Python命令行或脚本进行解释了，那么如何使用这个解释器呢？

## 使用REPL prompt

REPL(Read Evaluate Print Loop)，可以理解为循环读取评估板信息。ESP8266模块就可以通过这互动了解内部的MicroPython程序或者命令行操作。可以通过UART串口或者WIFI进行连接。

本系列只介绍UART连接，WIFI连接可自行查看[WebREPL - a prompt over WiFi](http://docs.micropython.org/en/latest/esp8266/tutorial/repl.html#webrepl-a-prompt-over-wifi) 。

### UART prompt

REPL始终映射的是UART0外设，ESP8266的GPIO1为TX，GPIO3为RX，波特率为1152000。

本系列的ESP8266模块上有串口芯片，因此可以通过MicrUSB线缆直接连接电脑。

在Windows，本系列选用的是`Tera Term` 工具，这里留下[Tera Term下载地址]()正如前面所述，也可以使用其他带有串口接受和发送的软件。

打开软件，设置好COM8和波特率，按下ESP8266模块的`RST` 按键，即可获取信息：

```bash
MicroPython v1.13 on 2020-09-11; ESP module with ESP8266
Type "help()" for more information.
>>>
```

这样就是熟悉的界面，类似于Python的解释器样式，就可以使用Python的命令行操作：

![MicroPython解释器](https://gitee.com/sharewow/pic_repo/raw/master/img/MicroPython%E8%A7%A3%E9%87%8A%E5%99%A8.png)

嗯嗯，可以在这里试一试Python相关的命令行操作，熟悉之后，就可以点灯啦！

## 点灯大法

ESP8266模块默认板载GPIO2连接了一颗LED灯（本系列是蓝色的灯）。可以控制GPIO2来改变灯的状态，键入如下Code，以下示意带逐行解释，实际操作不需要输入`#`以及该行后面内容：

```python
>>> import machine		# 导入machine
>>> pin = machine.Pin(2, machine.Pin.OUT)		#定义引脚2为输出类型，名称为pin
>>> pin.on()		# pin引脚打开（输出高电平）
>>> pin.off()		# pin引脚关闭（输出低电平）
>>>
```

如果操作正常，就应该能看到ESP8266模块上的灯亮起；上述`pin.on() `和 `pin.off()` 的状态与本系列的LED灯的控制相反，这个取决于LED在板子上的连接方式，不必过多纠结。

### 循环点灯

在这个REPL pormpt命令行中，支持很多常规操作如：

- 上键下键，获取输入历史；
- Tab自动补全；
- 函数，方法定义自动换行续航，缩进；
- Ctrl - E进入特殊粘贴模式，可以粘贴一段Code；

那么就可以定义一个LED跳转的函数，进行循环电灯的操作：

```python
>>> import machine
>>> pin = machine.Pin(2, machine.Pin.OUT)
>>> pin.on()
>>> pin.off()
>>> def toggle(p):
...     p.value(not p.value())
...
>>> toggle(pin)
>>> toggle(pin)
>>> import time
>>> while True:
...     toggle(pin)
...     time.sleep_ms(500)
...

```

ESP8266模块GPIO2被驱动闪烁的实际效果图如下：

![Blink](https://i.loli.net/2020/12/20/6lLsvpbzq35Gh2X.gif)

这个时候肯定是极大的喜悦。

这种命令行进行code编写，在学习的时候比较方便；但是如果程序内容比较多，还是通过脚本文件结构清晰，方便，第四回会介绍通过更新MicroPython脚本文件的形式进行程序编写。

通过配置GPIO为PWM输出，也可以实现LED的呼吸状态，在第三回，介绍PWM驱动的时候会尝试。

## 结束语

第二回的内容比较重要，虽然是简单的点灯，但可以将整个烧录流程，REPL prompt方式熟悉。

接着就是第三回，学习其他常用的驱动方法。

2020-12-20；





