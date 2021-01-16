# MicroPython_ESP8266_IoT——（工具篇）Pycharm + Micropython

> 工欲善其事，必先利其器。

之前，使用官网推荐的REPL和Files Download工具，估计都已经熟悉了，不熟悉的同学可以根据前五回的内容进行复习。

想必学习Python的时候，会选择一款功能强大的IDE；而Pycharm就是一款功能强大的Python编辑器，之前学习使用过Pycharm，使用起来着实顺手。

前几天在Github上闲逛，发现有大神release了一款Micropython的插件，可以在Pycharm上使用该插件，进行ESP8266的开发，功能涵盖REPL和Files Download。经过一番使用，觉得非常赞，那就分享给大家，希望可以提高大家的开发效率。

网上已经有非常详细的教程了，这里就转载一篇[MICROPYTHON教程2 - PYCHARM + MICROPYTHON配置](https://singtown.com/learn/48860/)，并对某些内容进行补充。

## 安装Pycharm Community

首先到 https://www.jetbrains.com/pycharm/download 安装社区版本的PyCharm 。Professional是专业版，Community为社区版，推荐安装社区版，以杂家的开发程度，社区版完全可以应对。

![img](https://cdn.singtown.com/2018/04/QQ20180410-0.png)

然后就是同意条款下一步下一步安装完成。

提示：可以修改安装目录，

## 安装插件

Mac用户点击Preferences，Windows用户点击setting。

![img](https://cdn.singtown.com/2018/04/QQ20180410-1.jpg)

选中左侧Plugins选项，在右侧搜索栏中输入micropython，之后点击Search in repositories或者Install JetBrains plugin；

![img](https://cdn.singtown.com/2018/04/QQ20180410-2.jpg)

点击绿色的大大的Install；

![img](https://cdn.singtown.com/2018/04/QQ20180410-3.jpg)

再点击大大的Restart PyCharm重启软件来生效。

![img](https://cdn.singtown.com/2018/04/QQ20180410-4.jpg)

同样，在Preference中的Language & Frameworks里面的 MciroPython 中点击，勾选Enalbe MicroPython support，并且选择相应的设备，图片中选择的是Pyboard，杂家使用ESP8266，所以要下拉选出ESP8266。

![image-20210116114927917](https://gitee.com/sharewow/pic_repo/raw/master/img/image-20210116114927917.png)

点击Detect可以自动检测设备，杂家使用的时候是可以的（需要USB接上MicroPython 模块）。如果不好用，需要手动输入，Mac下是：/dev/ttyxxxxx，Windows下是COMxxxx。

## 新建项目

可以都按照默认：

![img](https://cdn.singtown.com/2018/04/QQ20180410-7.jpg)

新建一个main.py，可能会提示缺少pyserial，直接点击Install requirements安装即可：

![img](https://cdn.singtown.com/2018/04/QQ20180410-8.jpg)

输入内容：

```python
print("hello micropython in PyCharm")
```

## 配置项目

### 下载单个py文件

在main.py右键，可以看到Run ‘Flash main.py’，点击一下，就把main.py下载进去。

<img src="https://cdn.singtown.com/2018/04/4F784ABE4372BB1FB3C2065C988E174F.jpg" alt="img" style="zoom: 33%;" />



### 配置下载整个项目

点击Edit Configurations，新增一个运行配置：

![img](https://cdn.singtown.com/2018/04/QQ20180410-9.jpg)

点击 + 加号，选择MicroPython；

![img](https://cdn.singtown.com/2018/04/QQ20180410-10.jpeg)

<img src="https://cdn.singtown.com/2018/04/QQ20180410-10.jpg" alt="img" style="zoom:50%;" />

填写Name和Path，Path就是项目的目录，点击OK。

注意，同样在Preferences中吧.idea加入Excluded Floders，这样就可以确保.idea这个文件夹不会下载到板子里：

![img](https://cdn.singtown.com/2018/04/DC439BAD57B58795368CFB6214AFC6F6.jpg)

## REPL模式

在菜单栏Tools中选择MicroPython -> MicroPython REPL：

![img](https://cdn.singtown.com/2018/04/QQ20180410-11.jpg)

在Terminal窗口就会增加Local的REPL窗口：

![img](https://cdn.singtown.com/2018/04/QQ20180410-12.jpg)

需注意上面的提示：

```bash
Quit: Ctrl + ] 
Stop program : Ctrl + C
Reset : Ctrl + D
```

使用REPL之后，要下载文件到ESP8266设备上，需要先Ctrl + ]推出REPL模式，否则会提示串口占用。

## 结束语



## 参考链接

- Pycharm安装教程：https://blog.csdn.net/c_shell_python/article/details/79647627

- MICROPYTHON教程2-PYCHARM+MICROPYTHON配置：https://singtown.com/learn/48860/

2021-01-16；