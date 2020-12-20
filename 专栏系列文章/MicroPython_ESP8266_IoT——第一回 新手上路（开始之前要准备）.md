# 第一回 新手上路（开始之前要准备）

本系列涉及到使用的软件和硬件并不像以前那样繁琐、复杂。如果之前有这方面的了解，初学过Python或者用过80C51或STM32系列的MCU，那么这一回的内容就跟吃馍沾酱豆一样简单了。

学编程语言总是越学感觉越难，往往都是兴趣作为原始驱动，后面却变成了生产力里的驱动。

人生苦短，及时行乐，如果刚上手就能够方便地驱动硬件，初学即巅峰，岂不是美滋滋？那么MicroPython就比较容易上手，而且可以直观的操作UART，I2C，SPI，PWM，ADC等等外设。

想一想初学80C51的时候逐个寄存器读写，那个心态都是小纠结；再到初学STM32的时候使用固件库进行初始化，流程虽然清晰但过程依然繁琐。记得前两年开始，ST官方都在推CubeMx，通过可视化的界面，完成底层与外设接口的配置，能有效减少了项目开发前期的工作量，给人感觉就是用起来越简单越好。

现在都是在挤出时间来捣鼓些小玩意，那就要以最快的速度把东西搞出来，也算是降低了不少时间成本。

**如果只有可上网的浏览器，依然可以进行学习，详情参考本回最后惊喜。**

## MicroPython是啥

本系列默认读者已经掌握基本的Python编程能力。如果是初学者需要自行学习， [廖雪峰](https://www.liaoxuefeng.com/wiki/1016959663602400/)， [菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html) 等Python 3教程都是容易上手的。

本系列前期能够使用到的语法也非常简单，只要理解能力不差（只要笔者描述的够明白），也可以继续学习下去，有关语法的疑问可以遇到之后再通过互联网解答。

MicroPython的相关信息可以通过[MicroPython官网](http://www.micropython.org/) 了解到，不想看官网的原文，可以参考下面谷歌翻译的简介：

> MicroPython是Python 3编程语言的一种精简而高效的实现，其中包括Python标准库的一小部分，并且经过优化可在微控制器和受限环境中运行。
>
> MicroPython pyboard是一种紧凑的电子电路板，可在裸机上运行MicroPython，从而为您提供了可用于控制各种电子项目的低级Python操作系统。
>
> MicroPython充满了高级功能，例如交互式提示，任意精度整数，闭包，列表理解，生成器，异常处理等。 但是它足够紧凑，可以在256 k的代码空间和16 k的RAM中运行。
>
> MicroPython的目标是与普通Python尽可能兼容，从而使您可以轻松地将代码从桌面传输到微控制器或嵌入式系统。

一句话概括，**MicroPython就是可以使用Python语言，方便快捷的完成MCU对外接设备驱动的方式**。

## ESP8266是啥

硬件（MCU的型号和外接设备）的选择本质上可以理解为坑多和坑少的尝试（别问我为什么知道的），总要面临着成本和性能的均衡。

大多数开发阶段，为了迅捷方便，可以买市场上设计成熟的模块。就像买电脑一样，买一台组装好的机器，而不是东市买内存，西市买主板，南市买显卡，北市买电源。

当然必须得是超高性价比的，即要便宜还要能打的那种。在MicroPython官网提供了一些硬件模块，针对该网站学习量身定制的。可是价格也不太亲民，即使在某宝上，pyboard的套件也要大几十往上。

而同样支持MicroPython的ESP8266模块，ESP32的模块就比较便宜，并且该有的功能都有，就是想要这种便宜又能打的。这玩意长这样：

<img src="https://gitee.com/sharewow/pic_repo/raw/master/img/ESP8266%20Model%20%20Item.jpg" alt="ESP8266 Model  Item" style="zoom: 50%;" />

先声明**这里不是广告**，笔者某宝买的ESP8266串口WIFI模块才12.6元一个，还免运费（这TM比STM32C8T6还便宜啊），实在是觉得非常合算，[链接在这需要自取](https://item.taobao.com/item.htm?spm=a230r.1.14.6.44c3c5fej8bdIo&id=531755241333&ns=1&abbucket=6#detail) 。

需要注意，此产品发货的时候，下方两排排针是不焊接的，需要到货这后自行焊接。嫌麻烦的同学可以咨询店家是否可以提供焊接，或找有工具的同学进行帮忙。如果不焊接的情况下，板载上有一颗LED灯可以进行控制。

该ESP8266模块基于MicroPython可以提供的内部功能和外设资源驱动有：

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

这些功能，外设驱动都非常有用，仔细探索一下，若能将这些功能悉数收入囊中，也是收获颇丰了。

## 硬件准备

需要的材料也相当少。

### MicroUSB数据线

上述ESP8266模块，烧录程序的方式是通过ESP8266板载的一组UART0 (GPIO1=TX, GPIO3=RX)。

这组UART0在模块上连接了一个串口芯片 CH340 (也可能是其他的型号，电脑要安装对应型号的驱动)。因此需要MicroUSB的接口连接电脑USB，进行供电和数据传输，示意图如下：

![Interface](https://gitee.com/sharewow/pic_repo/raw/master/img/Interface.png)

所需要的MicroUSB数据线（就是以前很多人说的安卓接口）接口示意见下图：

![MicroUSB Wire](https://gitee.com/sharewow/pic_repo/raw/master/img/MicroUSB%20Wire.png)

如果手头有这根MicroUSB数据线，一定要确定**是否能够进行数据传输**。有些线材原始功能是做充电使用的，可能不能进行数据传输。

### 其他设备

有条件，有基础，有想法的同学，可以一同采购其他的外设。结合本系列后面的内容，可能会用到0.96inch的OLED屏幕，HC-SR501人体红外感应模块，DHT11温湿度模块，SG90舵机等。

如果有其他驱动需求也可以酌情选择，有目的性驱动可以更好的督促学习。

这些设备也都是在上面的店铺采购的，价格也比较便宜。根据ESP8266的资源来驱动这些硬件，对进行MicroPython的学习很有帮助。

## 软件准备

主要使用的软件为串口相关作为调试的接口，配合工具进行脚本上传。

**声明**：由于部分软件下载，可能会受到网络不可抗力约束，所以后续使用到的软件工具会统一使用[LZ网盘](https://sharewow.lanzous.com/b00u1gt5c) 进行上传和下载：

**链接**：https://sharewow.lanzous.com/b00u1gt5c

**密码**：本来设定的是密码在公众号：`sharewow`后台回复**micropython**获取；现在也可以私信回复；

### 串口相关

[CH340的串口驱动程序](https://sharewow.lanzous.com/b00u1gt5c)，也有可能你需要的是PL2102的驱动（取决于购买的ESP8266模块上的串口芯片型号）。用于USB连接电脑之后，电脑识别到设备。新版本的Win10应该都可以插入设备，自动搜索相关驱动了。

串口调试助手，用于使用Python REPL(交互式解释器，类似于CMD进入Python的交互界面)，使用终端显示器对程序进行仿真。

此时需要可以进行输入的串口调试助手，像常用带写入的串口调试助手都可以，包括下面要用的MicroPython File Uploader 也可以，笔者习惯使用 [Tera Term](https://sharewow.lanzous.com/b00u1gt5c)。

### MicroPython File Uploader

这款软件用来读取或写入ESP8266模块中4M的Flash内的文件，比如内部的的boot.py和main.py等。

区别于REPL，可以在Windows中完成程序的编辑，再通过USB线缆传输到Flash中，接着复位，就会运行编写的程序。

软件界面展示：

![MicroPython File Uploader](https://gitee.com/sharewow/pic_repo/raw/master/img/MicroPython%20File%20Uploader.png)

软件下载地址：[MicroPython File Uploader](https://sharewow.lanzous.com/b00u1gt5c) 。

### 最好有个编译器

编辑器要选自己习惯使用的，Notepad3 也好（这个得注意，Python对缩进要求严格，建议Tab一定要改成制表符），Sublime Text也好，Ultra Edit也好，怎么方便怎么来，笔者就使用个人熟悉的[Atom](https://atom.io/) 。

## 环境准备

Windows端要自己安装Python 3，网上有很多教程，这里指路廖雪峰的Python教程之[安装Python](https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624) ；注意哦，安装目录可以选在`Customize installation` 选项自己选择，建议默认安装在`C:\Python3` 。

至此准备工作就做完了，接下来就可以开始学习了。

## 惊喜

如果等不及买来硬件，就想学习新知识怎么办？

那么，**仅需要有一台可以上网的电脑**，就可以进行MicroPython的学习了，官方给出了一个网页版的操作平台，叫做unicorn，笔者查过了中文名叫独角兽。

地址为：[MicroPython的在线操作平台unicorn](https://micropython.org/unicorn/) 

该平台上，你可以实现基于pyboard的MicroPython的学习和及外设驱动，提供的外设模拟设备也非常多，可视化做的非常棒，详情界面如下：

![unicorn](https://gitee.com/sharewow/pic_repo/raw/master/img/unicorn.png)

可以直接选择一个Demo，比如SERVO，运行脚本就可以观察到舵机运动的动画：

这个GIF制作的有问题，后期再补上。。。

非常直观的学习方式，甚至还省去了硬件连接带来的繁琐，是一个非常棒的操作平台。

## 结束语

第一回就这样结束了。

第二回，将学习在ESP8266模块上点亮LED灯，致敬经典。

如果迫不及待，赶紧接着下一回继续学习吧！

2020-12-20；