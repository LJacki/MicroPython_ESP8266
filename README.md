# MicroPython_ESP8266

之前写博客每篇文章基本是独立的，都是按照学习，记录，分享的逻辑。此次想通过有主题的系列文章，带来有稍有深度的分享。

本系列将使用MicroPython驱动ESP8266，借助贝壳物联接入天猫精灵，简易实现智能家居控制体验。

## 开始之前要准备

涉及到软件和硬件并不像以前那么复杂，只需稍许准备即可。

### MicroPython

总觉得编程语言总是越学越难，如果刚上手就能够驱动硬件，初学即巅峰，岂不是美滋滋？

那么MicroPython就比较容易上手，而且可以直观的操作UART，I2C，SPI，PWM，ADC等等外设。想一想初学80C51的时候逐个控制寄存器读写，再到初学STM32的时候使用固件库进行初始化，流程也是非常繁琐。现在ST官方都在推CubeMx，通过可视化的界面，完成底层与外设接口的配置，有效的减少了项目开发前期的工作量。现在都是在挤出时间来捣鼓些小玩意，那就要以最快的速度把东西搞出来，也算是降低了不少时间成本。

本系列默认读者已经掌握基本的Python编程能力。如果是初学者需要自行学习， [廖雪峰](https://www.liaoxuefeng.com/wiki/1016959663602400/)， [菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html) 等Python 3教程都是容易上手的。本系列能够使用到的语法也非常简单，只要理解能力不差（只要笔者描述的够明白），也可以继续学习下去，有关语法的疑问可以遇到之后再通过互联网解答。

MicroPython的相关信息可以通过[MicroPython官网](http://www.micropython.org/) 了解到，不想看官网的可以参考下面谷歌翻译的简介：

> MicroPython是Python 3编程语言的一种精简而高效的实现，其中包括Python标准库的一小部分，并且经过优化可在微控制器和受限环境中运行。
>
> MicroPython pyboard是一种紧凑的电子电路板，可在裸机上运行MicroPython，从而为您提供了可用于控制各种电子项目的低级Python操作系统。
>
> MicroPython充满了高级功能，例如交互式提示，任意精度整数，闭包，列表理解，生成器，异常处理等。 但是它足够紧凑，可以在256 k的代码空间和16 k的RAM中运行。
>
> MicroPython的目标是与普通Python尽可能兼容，从而使您可以轻松地将代码从桌面传输到微控制器或嵌入式系统。

一句话概括，可以使用Python驱动MCU。

### ESP8266

硬件的选择本质上是坑多和坑少的尝试，别问我为什么知道的。

大多数开发阶段，为了迅捷方便，可以买市场上已经成熟的模块。就像买电脑一样，买一台已经组装好的机器，而不是东市买内存，西市买主板，南市买显卡，北市买电源。

当然必须得是超高性价比的，要便宜还要能打的那种。在MicroPython官网提供了一些硬件模块，针对该网站学习量身定制的。可是价格也不太亲民，即使在某宝上，pyboard的套件也要大几十往上。

而同样支持MicroPython的ESP8266模块，ESP32的模块就比较便宜，并且该有的功能都有，就是想要这种便宜又能打的。

<img src="README.assets/ESP8266 Model  Item.jpg" alt="ESP8266 Model  Item" style="zoom:50%;" />

此处不是广告，笔者某宝买的ESP8266串口wifi模块才12.6元一个还免运费（这TM比STM 32 C8T6 还便宜） [链接在这需要自取](https://item.taobao.com/item.htm?spm=a230r.1.14.6.44c3c5fej8bdIo&id=531755241333&ns=1&abbucket=6#detail) 。

注意，此产品发货的时候，下方两排排针是不焊接的，需要到货之后自行焊接。嫌麻烦的同学可以询问店家是否可以提供焊接，或找有工具的同学帮忙，不焊接排针的情况下，板载上有一颗LED灯可以进行控制。

ESP8266基于MicroPython可以提供的外设资源和驱动有：

- Delay and timing
- Timers
- Pins and GPIO
- UART(serial bus)
- PWM(pulse width modulation)
- ADC(analog to digital conversion)
- Software SPI bus
- Hardware SPI bus
- I2C bus
- Real time clock(RTC)
- Deep-sleep mode
- OneWire driver
- NeoPixel driver
- APA102 driver
- DHT driver

这些外设和驱动都非常有用，若能将这些功能悉数收入囊中，也是收获颇丰了。

### 硬件准备

#### MicroUSB数据线

上述ESP8266模块烧录程序的方式是通过ESP82266板载的一组UART0 (GPIO1=TX, GPIO3=RX)，这组UART0在模块上连接了一个串口芯片 CH340 (也可能是其他的型号，电脑要安装对应型号的驱动)。因此需要MicroUSB的接口连接电脑USB，进行供电和数据传输。

![Interface](README.assets/Interface.png)

所需要的MicroUSB数据线（就是以前很多人说的安卓接口）接口示意见下图：

![MicroUSB Wire](README.assets/MicroUSB Wire.png)

#### 其他设备

有条件的同学，可以一同采购其他的外设。结合本系列后面的内容，会用到0.96inch的OLED屏幕，HC-SR501人体红外感应模块，DH11温湿度模块，SG90舵机等。

如果有其他驱动需求也可以酌情选择，有目的性驱动可以更好的督促学习。

这些设备也都是在上面的店铺采购的，价格也比较便宜。根据ESP8266的资源来驱动这些硬件，对进行MicroPython的学习很有帮助。

### 软件准备

#### 串口相关

[CH340的串口驱动程序]()，用于USB连接电脑之后，电脑识别到设备。

串口调试助手，用于使用Python REPL(交互式解释器，类似于CMD进入Python的交互界面)，使用终端显示器对程序进行仿真。

此时需要可以进行输入的串口调试助手，像常用带写入的串口调试助手都可以，包括下面要用的MicroPython File Uploader 也可以，笔者习惯使用 [Tera Term]()。

#### MicroPython File Uploader

这款软件用来读取或写入ESP8266模块中4M的Flash内的文件，比如内部的的boot.py和main.py等。

区别于REPL，可以在Windows中完成程序的编辑，再通过USB线缆传输到Flash中，接着复位，就会运行编写的程序。

#### 最好有个编辑器

编辑器要选自己习惯使用的，Notepad ++ 也好（这个得注意，Python对缩进要求严格，建议Tab一定要改成制表符），Sublime Text也好，Ultra Edit也好，怎么方便怎么来，笔者就使用个人熟悉的Atom。

### 环境准备

Windows端要自己安装Python 3，网上有很多教程，这里指路廖雪峰的Python教程之[安装Python](https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624) ；注意哦，安装目录可以选在`Customize installation` 选项自己选择，建议默认安装在`C:\Python3` 。

至此本系列的准备工作就做完了，接下来就可以开始真正的学习了。

## 手把手开始点灯

接着折腾，接着学。

### ESP82266通用信息

ESP8266是Espressif Systems推出的一种流行的，具有WiFi功能的片上系统（SoC）。相关的Datasheet可以在[这里下载]() 。

MicroPython for ESP8266库（）应该叫方法）中的Pin number都是基于ESP8266的芯片，而不是ESP8266模块引出的引脚（意思就是不是那焊接的两排排针的序号）。

为了后面使用方便，下里提供一些技术规格：

- CPU频率：80 MHz，可以超频至160 MHz；
- 总可用RAM：94KB（部分预留给系统）；
- 外部FlashROM：存放程序和数据，通过SPI烧录FLash，当前模块挂在的胃4 MB；
- GPIO：16 + 1（GPIOs 可复用为其他功能，包括外部FlashROM，UART，深睡唤醒等等）；
- UART：一组收发UART（无硬件握手协议），一组只有TX的UART；
- SPI：2组SPI接口（一组用于FlashROM）；
- I2C：无外部I2C（在任何引脚上均可以实现）；
- 编程：使用UART的BootROM引导程序。

#### 内部资源限制

ESP8266的片上资源非常有限（RAM），因此建议避免分配太多的容量给对象（list列表，dictionaries字典）。使用完文件系统，sockets等要注意及时关闭。

关于ESP8266启动进程，Real-time clock，Sockets 和 WiFi buffer 溢出，SSL/TLS限制的信息，可参考[官方文档](http://docs.micropython.org/en/latest/esp8266/general.html) 次出不再讲述。

### 开始使用MicroPython

将ESP8266模块通过MicroUSB线缆，与PC连接。默认此时已经完成了ESP8266模块的上电操作。

### 电脑识别串口

电脑端应该已经识别了ESP8266模块上的串口芯片，如果在资源管理器中看到对应的COM口出现感叹号，就必须要安装串口相关驱动了（这个之前有提到过）。下图所示的状态就是已经识别并成功安装驱动。

![1607255359510](README.assets/1607255359510.png)

或者可以在CMD控制台中输入`mode` 指令：

```bash
C:\Users\Administrator>mode
```

控制台中就会列举出已经连接的串口，如下图所示：

![1607255325264](README.assets/1607255325264.png)

#### 串口波特率修改方式

串口波特率如果不是115200，可以在设备管理器中进行修改，操作步骤如下（这个GIF制作的设置有点问题，不过不影响内容；）：

![COM config](README.assets/COM config.gif)

### 获取固件

固件（firmware）可以理解为电脑的系统，有三种版本，适配不同的外挂Flash大小；本系列ESP8266模块外挂Flash大小为4M，所以可以选用Stable firmware，[这里是下载地址](http://micropython.org/download/esp8266/) 。选择最新版的即可：

- esp8266-20200911-v1.13.bin (elf, map) (latest)

### 烧录固件

需要使用esptool来烧录刚才下载好的固件。

#### 安装esptool

在CMD控制台中使用`pip` 工具安装esptool。pip为Python解释器的工具，此处使用python 3，对应指令应修改为：

```bash
pip3 install esptool
```

安装好之后键入`esptool.py version` ，可以查看当前工具版本：

```bash
C:\Users\Administrator>esptool.py version
esptool.py v2.6
2.6
```

这样，就可以愉快的使用此工具进行ESP8266的固件烧录了。

#### 清除Flash

可以使用这样的命令清除ESP8266模块上flash内容（现在端口修改为COM8）：

```bash
esptool.py --port COM8 erase_flash
```

如果擦除成功会出现下面的状态：

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

#### 可以烧录了

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

而且， 烧录成功默认ESP8266处于AP状态，可以打开手机或电脑WIFI搜索，搜索到以MicroPython-xxxxxx形式存在的WIFI，这种连接方式作用于下一小节，通过WIFI连接REPL prompt。

如果未能成功安装，详细的排查方案参考这里[解决安装问题](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#troubleshooting-installation-problems) 。笔者提供两个检查方法：

1. 检查命令行格式是否正确；
2. 检查检查端口是否识别，可以先进行擦除，擦除成功后紧接着进行烧录；

### 使用REPL prompt

REPL(Read Evaluate Print Loop)，可以理解为循环读取评估板信息。ESP8266模块就可以通过这互动了解内部的MicroPython程序或者命令行操作。可以通过UART串口或者WIFI进行连接。

本系列只介绍UART连接，WIFI连接可自行查看[WebREPL - a prompt over WiFi](http://docs.micropython.org/en/latest/esp8266/tutorial/repl.html#webrepl-a-prompt-over-wifi) 。

#### UART prompt

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

![1607355166228](README.assets/1607355166228.png)

嗯嗯，可以在这里试一试Python相关的命令行操作，接下来就可以点灯啦！

### 点灯大法

ESP8266模块默认板载GPIO2连接了一颗LED灯（本系列是蓝色的灯）。可以控制GPIO2来改变灯的状态，键入如下Code：

```python
>>> import machine
>>> pin = machine.Pin(2, machine.Pin.OUT)
>>> pin.on()
>>> pin.off()
>>>
```

如果操作正常，就应该能看到ESP8266模块上的灯亮起；上述`pin.on() `和 `pin.off()` 的状态与本系列的LED灯的控制相反，这个不必过多纠结。

#### 循环点灯

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

![Blink](README.assets/Blink.gif)

这个时候肯定是极大的喜悦。这种命令行进行code编写，在学习的时候比较方便，之后会介绍通过跟新源文件的形式进行程序编写。

## 常用的类

已经会使用UART prompt进行MicroPython在ESP8266模块上的使用了，即将解锁众多玩法。

本系列是想通过ESP8266做IoT设备，就先来挖掘“物”的使用，学习ESP8266模块配合MicroPython常用的外设驱动。

### 核心时钟

可以通过模块machine，对CPU核心时钟进行修改：

```python
import machine

machine.freq()          # get the current frequency of the CPU
machine.freq(160000000) # set the CPU frequency to 160 MHz
```

一般情况下，当然是设定为160 MHz，速度快用起来才爽。

可以通过模块esp，打开或关闭调试信息重定向（此处默认应为打开）：

```python
import esp

esp.osdebug(None)       # turn off vendor O/S debugging messages
esp.osdebug(0)          # redirect vendor O/S debugging messages to UART(0)
```

### 网络连接

网络连接模块工作方式：

```python
import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('essid', 'password') # connect to an AP
wlan.config('mac')      # get the interface's MAC adddress
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)         # activate the interface
ap.config(essid='ESP-AP') # set the ESSID of the access point
```

可以通过下面这种方式连接到本地的WIFI网络：

```python
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('essid', 'password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
```

上述程序中需要替换essid为要连接的WIFI名称，替换password为要连接的WIFI密码。

一旦网络连接建立，`socket`模块就可以被创建使用。

### 延时和时间

可以使用`time`模块：

```python
import time

time.sleep(1)           # sleep for 1 second
time.sleep_ms(500)      # sleep for 500 milliseconds
time.sleep_us(10)       # sleep for 10 microseconds
start = time.ticks_ms() # get millisecond counter
delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
```

### 引脚和GPIO

可以使用`machine.Pin`类：

```python
from machine import Pin

p0 = Pin(0, Pin.OUT)    # create output pin on GPIO0
p0.on()                 # set pin to "on" (high) level
p0.off()                # set pin to "off" (low) level
p0.value(1)             # set pin to on/high

p2 = Pin(2, Pin.IN)     # create input pin on GPIO2
print(p2.value())       # get value, 0 or 1

p4 = Pin(4, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistor
p5 = Pin(5, Pin.OUT, value=1) # set pin high on creation
```

这个类就定义引脚输入和输出类型，仔细观察发现还可以设定内部上拉。

通过配置GPIO控制LED点亮和熄灭，在前面已经了解过了；能够配置GPIO高低电平，那么后面的操作就是锦上添花了。

### PWM

PWM可以在除了PIN（16）的所有Pin使用。所有通道都有一个频率，从1 Hz到1000 Hz，占空比从0 到 1023；

使用`machine.PWM`类：

```python
from machine import Pin, PWM

pwm0 = PWM(Pin(0))      # create PWM object from a pin
pwm0.freq()             # get current frequency
pwm0.freq(1000)         # set frequency
pwm0.duty()             # get current duty cycle
pwm0.duty(200)          # set duty cycle
pwm0.deinit()           # turn off PWM on the pin

pwm2 = PWM(Pin(2), freq=500, duty=512) # create and configure in one go
```

通过调节占空比，可以调整pin 2上连接的LED灯的亮度。如果进行合理的时间搭配，还可以达到呼吸灯的效果：

```python
import time, math, machine

led = machine.PWM(machine.Pin(2), freq=1000)

def pulse(l, t):
    for i in range(400):
        l.duty(int(math.sin(i / 200 * math.pi) * 500 + 523))
        time.sleep_ms(t)
        
def fading():
    for i in range(50):
    	pulse(led, 5)
```

可以看一下实际效果图GIF：

![Breath](README.assets/Breath.gif)

可以通过调整sin函数的系数，来调节呼吸的频率；通过调节占空比的基础数值（上述程序中为523），来调节亮，灭的时间范围；

### 其他

后面还有其他的类和方法，都是接口相关的，想要等到后面有小制作的时候，再结合实物，详细的说明。

如果感兴趣，可以根据官网的教程走一遍，内容有ADC，SPI bus，I2C bus，RTC，Deep-sleep mode，OneWire driver，NeoPixel driver，APA102 driver，DHT dirver等；[连接在此](http://docs.micropython.org/en/latest/esp8266/quickref.html#adc-analog-to-digital-conversion) 。

## 接入贝壳物联

本来计划先把所有的硬件介绍完，再介绍如何介入贝壳物联的。但是那样就比较枯燥，还是先尝试接入贝壳物联，来增加ESP8266模块的可玩性。

需要了解[贝壳物联平台通信协议]([贝壳物联平台通讯协议-贝壳物联，让你与智能设备沟通更方便的物联网云平台 (bigiot.net)](https://www.bigiot.net/help/1.html)) ，如果不想了解，可以跳过这3小节，不影响后面继续等到后面有疑问再来这3小节里面寻找。这里使用TCP(微博socket)长连接协议：

### 通讯地址

通讯方式：TCP或websocket

地址：www.bigiot.net

TCP端口：8181，还有其他的8282，8585

Websocket端口：8383，8484

若选用8181端口则，服务器不主动发送心跳包，靠客户端主动发送心跳包保持在线，心跳间隔以40~50s为佳；

换成人话，就是设备需要间隔40~50s向服务器发过去一个指令，用于通知服务器端，自己还活着，因为时间间隔非常有规律，所以拟称为心跳包。

其他情况，自行了解；

### 通讯数据格式

Json字符串 + 换行符，比如：

```json
{"M":"beat"}\n
```

这种形式叫做Json New Line。

### 命令列表

常用的命令有10种，分别是：

1. 设备登录（加密）；
2. 发送实时数据；
3. 用户和设备上线通知数据；
4. 用户或设备下线通知数据；
5. 用户与设备、设备与设备、用户与用户间沟通指令数据；
6. 查询设备或用户是否在线；
7. 查询当前设备状态；
8. 发送报警信息；
9. 查询服务器时间；
10. 强制目标设备下线；

命令，都是一句Json New Line的数据格式（有点类似于Python的字典），以包的形式，向服务器发出。

详细介绍**设备登录**和**发送实时数据**，熟悉了这两个就可以完成基本的想服务器发送指令的操作了。

#### 设备登录（加密）

**格式**：

```json
{"M":"checkin","ID":"xx1","K":"xx2"}\n
```

**说明**：
M —— 固定(Method)
checkin —— 固定，登录指令
ID —— 固定
xx1 —— 可变，设备ID，在会员中心查看
K —— 固定(apiKey)
xx2 —— 可变，设备apikey，在会员中心查看
设备登录后，如果在1分钟内无数据传送，连接将被自动关闭。
若保持设备长期在线，可每隔50秒向服务器发送一次信息，任何信息均可。

**返回结果（登录信息正确时返回，错误无任何返回，如果设备已登录，也将无任何返回信息，且不会登录成功）：**

```
{"M":"checkinok","ID":"xx1","NAME":"xx2","T":"xx3"}\n
```

说明：
M —— 固定(Method)
checkinok —— 固定，设备登录成功指令
ID —— 固定
xx1 —— 可变，设备登录成功后，用于通讯的唯一ID，其组成为字符“D"+设备ID，如D24

NAME —— 固定
xx2 —— 可变，该设备的名称
T —— 固定(time)
xx3 —— 可变，服务器发送信息时的时间戳，自从 Unix 纪元（格林威治时间 1970 年 1 月 1 日 00:00:00）到当前时间的秒数。

#### 发送实时数据

**格式**：

```json
{"M":"update","ID":"xx1","V":{"id1":"value1",...}}\n
```

**说明**：此命令无返回信息，两次发送间隔不得小于5s，发送数据前应确保该设备已登录在线。

M —— 固定(Method)
update —— 固定，实时更新数据指令（可用 u 代替 update，减小命令长度）
ID —— 固定
xx1 —— 可变，设备ID，在会员中心查看
V —— 固定(Value)
   id1 —— 可变，数据接口ID，在会员中心查看
   value1 —— 可变（数值型），本地数据（譬如：传感器测量数据）
   ... —— 可以更新该设备下多个数据接口的数据

**示例**

一次上传单个接口数据示例：

```json
{"M":"update","ID":"2","V":{"2":"120"}}\n
```

同时上传多个接口数据示例：

```json
{"M":"update","ID":"112","V":{"6":"1","36":"116"}}\n
```

实时上传定位接口数据示例：

```json
{"M":"update","ID":"112","V":{"36":"116,40"}}\n
```

其中116为经度值，40是为维度值，详见：[定位数据上传说明](http://www.bigiot.net/talk/92.html)。

贝壳物联的官方指导手册中也提供的了**PC端的模拟测试** ，可以通过软件，先对自己创建的设备进行便捷的联网访问。

PC模拟测试TCP长连接教程见：《[贝壳物联通讯协议TCP连接测试教程](http://www.bigiot.net/help/18.html)》

Windows测试工具见：https://www.bigiot.net/talk/1140.html

### 设备联网

接下来可就是真操实练了，先从ESP8266内部文件目录搞起。

#### 内部文件目录

通过MicroUSB连接ESP8266模块到PC，确保COM端口已经被识别到。PC端打开MicroPython File Uploader.exe工具。

选择COM口，Open。

在命令行中键入：`import os`, `os.listdir()`：

```python
>>> import os
>>> os.listdir()
['boot.py', 'main.py']
```

可以看到在ESP8266模块中，有两个特殊启动文件，boot.py 和 main.py。当设备启动，一旦文件系统被挂载上，boot.py将会首先执行，而后执行main.py。可以在main.py中创建用户代码，也可以创建自己的用户脚本，并且在main.py中建立关联，如在main.py中写入如下code：

```python
import my_app

my_app.main()
```

并创建my_app.py进行用户代码编写，也可以创建其他用户模块。

先在PC端创建，main.py和my_app.py，并按照上述编辑main.py，并且在my_app.py中进行如下编辑：

```python
from machine import Pin
import time

# 定义引脚2为输出
ledPin = Pin(2, Pin.OUT)

def main():
	while True:
		# 延时1000ms使ledPin进行数值反转
		ledPin.value(not ledPin.value())
		time.sleep_ms(1000)
```

通过文件传输到ESP8266模块上，

在MicroPython File Uploader工具中，选择main.py和my_app.py文件（逐个上传），之后点击send，REPL提示如下：

```bash
>>> os.listdir()
['boot.py']
Sending main.py...
SUCCESS: 52 bytes written
>>> 
MPY: soft reboot
MicroPython v1.13 on 2020-09-11; ESP module with ESP8266
Type "help()" for more information.
Sending my_app.py...
SUCCESS: 223 bytes written
MicroPython v1.13 on 2020-09-11; ESP module with ESP8266
Type "help()" for more information.
>>> import os
>>> os.listdir()
['boot.py', 'main.py', 'my_app.py']
```

上述操作，先查看了内部只有boot.py文件，而后送入main.py和my_app.py，再次查询文件存在，上传成功；

此时，ESP8266模块会按照my_app.py的设计，进行每隔1s闪烁一次；

#### 连接WIFI

接入贝壳物联之前，需要是的ESP8266模块通过WIFI的STA模式连接入网络，可以在my_app.py编辑：

```python
import network

SSID = "MEIZU 17"	# 这里为WIFI名称
PASSWORD = "123456.789" # 这里为WIFI密码

def connect_wifi():
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	if not wlan.isconnected():
		print('Connecting to network...')
		wlan.connect(SSID, PASSWORD)
		while not wlan.isconnected():
			pass
	print('Network config:', wlan.ifconfig())

def main():
	connect_wifi()
```

将该文件上传至ESP8266模块，RST之后，便可以接入WIFI，这里为手机开的移动热点，REPL会通过print打印出wifi的接口配置信息：

```bash
>>> 
MPY: soft reboot
network config: ('192.168.43.70', '255.255.255.0', '192.168.43.127', '192.168.43.127')
```

手机端也可以看到有ESP设备连接：

有个图；

#### 连接至贝壳物联

在贝壳物联个人中心，添加智能设备，输入设备名称为LED灯（还有一些详细文档可以自行添加），如果不公开设备可以设定为加密等。

返回到智能设备列表，可以获得此设备重要信息，如ID，APIKEY，在线状态以及控制模式等。

图片

比较重要的信息为ID和APIKEY，在my_app.py脚本中，将会被定义为常量。

```python
DEVICEID = "10471"
APIKEY = "2530067a3"
host = "www.bigiot.net"
port = 8181
```

而后，使用socket连接：

```python
import socket

def connect_bigiot():
	s = socket.socket()
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = socket.getaddrinfo(host, port)[0][-1]
	
	try:
		s.connect(addr)
	except:
		print('Waiting for connect bigiot.net')
		
	print('Connect bigiot success!')
	# 获取会话返回信息
	ans = s.recv(50)
	print(ans)
	
	# 连接至贝壳物联后，需要通过发送命令，使得设备上线
    checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n', 'utf8')
	s.sendall(checkinBytes)
	print('Check in OK!')
	ans = s.recv(50)
	print(ans)
    

def main():
	# 先连接WIFI
	connect_wifi()
	
	# 再连接贝壳物联
	connect_bigiot()
```

将my_app.py上传至ESP8266模块后，对应REPL显示为：

```bash
>>> 
MPY: soft reboot
Network config: ('192.168.43.70', '255.255.255.0', '192.168.43.127', '192.168.43.127')
Connect bigiot success!
b'{"M":"WELCOME TO BIGIOT"}\n'
Check in OK!
b'{"M":"checkinok","ID":"D10471","NAME":"LED\\u706f",'
```

通过上一节的内容可以了解到，返回的Json New Line信息为服务端返回的数据，通过上述ID和NAME，可以看到ESP8266设备已经登录成功，再贝壳物联智能设备列表中也能够观察到设备在线：

图片

这样，就完成了这个名称为LED灯的ESP8266模块，通过

1. 先连接网络；
2. 再连接贝壳物联，进行设备登陆

两步骤，完成了设备联网，接入服务器。

#### 通过Web/手机控制设备

根据设备入网需求，再8181端口需要设备每隔40~50s向服务器发送依次心跳包，这里先设定每隔40秒，发送一次check status：

```python
def keepOnline(s, t):
	if utime.time()-t > 40:
		sayBytes = bytes('{\"M\":\"status\"}\n', 'utf8')
		s.sendall(sayBytes)
		ans = s.recv(100)
		print('Check status : {}\n'.format(json.loads(str(ans, 'utf-8'))["M"]))
		return utime.time()
	else:
		return t
```

LED的状态有两种，设定最简单的开关方式：

```python
def toggle(pin):
	pin.value(not pin.value())
```

接下来的交给main()函数，使用轮询的方式，判断是否收到web端/或手机端的消息，来判断是否需要对本地的LED灯状态进行改变：

```python
def main():

	# 定义引脚2为输出
	ledPin = Pin(2, Pin.OUT)
	# 定义引脚的初始状态为关闭, 此ESP8266模块中on()为LED熄灭；
	ledPin.off()

	# 先连接WIFI
	connect_wifi()

	# 再连接贝壳物联
	s = socket.socket()
	# 设置超时
	s.settimeout(10)
	connect_bigiot(s)

	recvData = b''
	t = utime.time()
	print("The start time is :{}\n".format(t))

	while True:

		try:	# 在超时时间内是否接收到数据
			recvData = s.recv(100)
		except: # 如果接收不到，维持上线状态
			t = keepOnline(s, t)
			print("Keep online operate, The time now is {}\n".format(t))
		if recvData : # 接收到数据
			msg = json.loads(str(recvData, 'utf-8'))
			print("Received Data is : {}\n".format(msg["C"]))
			if msg["C"] == "offOn": # 接收到offOn的命令，执行操作
				toggle(ledPin)
```

















如果wifi连接不成功，会有什么信息提示？















## 驱动0.96 Inch OLED