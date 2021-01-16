# MicroPython_ESP8266_IoT——（工具篇）Pycharm + Micropython

> 工欲善其事，必先利其器。

之前，使用官网推荐的`REPL`和`Files Download`工具，估计都已经熟悉了，不熟悉的同学可以根据前五回的内容进行复习。

想必学习Python的时候，会选择一款功能强大的IDE；而Pycharm就是一款功能强大的Python编辑器，之前学习使用过Pycharm，使用起来着实顺手。

前几天在Github上闲逛，发现有大神release了一款Micropython的插件，可以在Pycharm上使用该插件，进行ESP8266的开发，功能涵盖`REPL`和`Files Download`。经过一番使用，觉得非常赞，那就分享给大家，希望可以提高大家的开发效率。

网上已经有非常详细的教程了，这里就转载一篇[MICROPYTHON教程2 - PYCHARM + MICROPYTHON配置](https://singtown.com/learn/48860/)，并对某些内容进行补充。

## 安装Pycharm Community

首先到 https://www.jetbrains.com/pycharm/download 安装社区版本的PyCharm 。`Professional`是专业版，`Community`为社区版，推荐安装社区版，以这里的开发程度，社区版完全可以应对。

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-0.png)

然后就是同意条款下一步下一步安装完成。

提示：可以修改安装目录。

## 安装插件

Mac用户点击`Preferences`，Windows用户点击`Setting`。

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-1.jpg)

选中左侧`Plugins`选项，在右侧搜索栏中输入micropython，之后点击`Search in repositories`或者`Install JetBrains plugin`；

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-2.jpg)

点击绿色的大大的`Install`；

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-3.jpg)

再点击大大的`Restart PyCharm`重启软件来生效。

![img](https://cdn.singtown.com/2018/04/QQ20180410-4.jpg)

同样，在`Preference`中的`Language & Frameworks`里面的 MciroPython 点击，勾选`Enalbe MicroPython support`，并且选择相应的设备，图片中选择的是Pyboard，这里要下拉选中`ESP8266`。

![image-20210116114927917](https://gitee.com/sharewow/pic_repo/raw/master/img/image-20210116114927917.png)

点击`Detect`可以自动检测设备，这里使用的时候是可以的（需要USB接上MicroPython 模块）。如果不好用，需要手动输入，Mac下是：`/dev/ttyxxxxx`，Windows下是`COMxxxx`。

## 新建项目

可以都按照默认：

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-7.jpg)

新建一个main.py，可能会提示缺少pyserial，直接点击`Install requirements`安装即可：

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-8.jpg)

代码编辑区就可以输入内容了，如下:

```python
print("hello micropython in PyCharm")
```

按照后面操作可以在`REPL`中有输出结果。

## 配置项目

### 下载单个py文件

在main.py右键，可以看到`Run ‘Flash main.py’`，点击一下，就把main.py下载进去。

<img src="https://gitee.com/sharewow/pic_repo/raw/master/img/4F784ABE4372BB1FB3C2065C988E174F.jpg" alt="img" style="zoom: 33%;" />



### 配置下载整个项目

点击`Edit Configurations`，新增一个运行配置：

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-9.jpg)

点击` + `加号，选择`MicroPython`；

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-10.jpeg)

<img src="https://cdn.singtown.com/2018/04/QQ20180410-10.jpg" alt="img" style="zoom:50%;" />

填写`Name`和`Path`，`Path`就是项目的目录，点击OK。

注意，同样在`Preferences`中把`.idea`加入`Excluded Floders`，这样就可以确保`.idea`这个文件夹不会下载到板子里：

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/DC439BAD57B58795368CFB6214AFC6F6.jpg)

## REPL模式

在菜单栏`Tools`中依次选择`MicroPython` -> `MicroPython REPL`：

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-11.jpg)

在`Terminal`窗口就会增加Local的`REPL`窗口：

![img](https://gitee.com/sharewow/pic_repo/raw/master/img/QQ20180410-12.jpg)

需注意上面的提示：

```bash
Quit: Ctrl + ] 
Stop program : Ctrl + C
Reset : Ctrl + D
```

使用`REPL`之后，要下载文件到ESP8266设备上，需要先`Ctrl + ]`退出`REPL`模式，否则会提示串口占用。

## 结束语

这篇文章原本是本系列文章中没有的，刚好遇到了好的东西，那就现学现用，拿来分享了。

个人而言，这种方式比之前的文件传输和调试方式，可以提高不少效率。

## 参考链接

- Pycharm安装教程：https://blog.csdn.net/c_shell_python/article/details/79647627

- MICROPYTHON教程2-PYCHARM+MICROPYTHON配置：https://singtown.com/learn/48860/
- 插件Github仓库地址：https://github.com/vlasovskikh/intellij-micropython

2021-01-16；