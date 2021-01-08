# MicroPython_ESP8266_IoT——第五回 网页配置（局域网连接WIFI）

参考官方手册中，对network库的介绍：[`network`-network configuration](http://docs.micropython.org/en/latest/library/network.html) 。

## network模块介绍

此模块提供网络连接的驱动，以及路由配置。配置网络后，可以通过`usocket`模块获取网络服务。

举个例子：

```python
# connect/ show IP config a specific network interface
# see below for examples of specific drivers
import network
import utime
nic = network.Driver(...)
if not nic.isconnected():
    nic.connect()
    print("Waiting for connection...")
    while not nic.isconnected():
        utime.sleep(1)
print(nic.ifconfig())

# now use usocket as usual
import usocket as socket
addr = socket.getaddrinfo('micropython.org', 80)[0][-1]
s = socket.socket()
s.connect(addr)
s.send(b'GET / HTTP/1.1\r\nHost: micropython.org\r\n\r\n')
data = s.recv(1000)
s.close()
```

网络适配接口

这里描述的network接口针对不同的MicroPython硬件有不同的实例。其中适用于ESP8266的为`class WLAN`，就以`class WLAN`[control built-in WiFi interfaces](http://docs.micropython.org/en/latest/library/network.WLAN.html#class-wln-control-built-in-wifi-interfaces) 为例，看一下都有哪些好用的方法。

提供的WiFi网络处理驱动，示例如下：

```python
import network
# enable station interface and connect to WiFi access point
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('your-ssid', 'your-password')
# now use sockets as usual
```

创建对象

WLAN 网络接口对象有两种：

1. `network.STA_IF`（station，也叫做client，连接到上游WiFi接入点）；
2. `network.AP_IF`（access point, 允许其他WiFi clients连接）；

下面提到的方法对否可用取决于接口的类型，比如只有STA接口支持`WLAN.connect()`来接入access point。

方法

此类中的方法有：

- WLAN.active([is_active])
- WLAN.connect(ssid=None, password=None, *, bssid=None)
- WLAN.disconnect()
- WLAN.scan()
- WLAN.status([param])
- WLAN.isconnected()
- WLAN.ifconfig([(ip, subnet, gateway, dns)])
- WLAN.config(‘param’)
- WLAN.config(param=value,…)

这些都比较好理解，详细说明可参考官方手册中的介绍。

主要介绍`WLAN.scan()`，用于扫描可用的无线网络（类似于手机打开WIFI之后，就开始搜索附件可用的无线网络）。

扫描方法只适用于STA接口，会返回包含WiFi接入点的信息元组组成的列表。包含内容如下：

ssid（WIFI ID）, bssid（MAC）, channel（信道）, RSSI（信号强度）, authmode（加密模式）, hidden（隐藏）

其中，`bssid`为接入点硬件地址，为二进制格式，返回为`bytes`对象。可以使用`ubinascii.hexlify()` 转换为ASCII格式。

authmode加密方（没有过多了解这些方式的区别，又兴趣可自行探索）有5个值：

- 0 - 不加密；
- 1 - WEP；
- 2 - WPA-PSK；
- 3 - WPA2-PSK；
- 4 - WPA/WPA2-PSK;

hidden的值也有两种：

- 0 - visible；
- 1 - hidden；

看过了这些方法，可以在REPL中挨个使用，加深对这些方法的理解；

Wi-Fi Manager Works

这一部分内容并非本人原创，[这里为Github仓库地址](https://github.com/tayfunulu/WiFiManager) 。使用tayfunuln的WiFiManager，可以使用MicroPython配合ESP32或ESP8266等硬件，进行Wi-Fi连接的管理。

可以理解为手机打开WiFi的开关后，自动搜索周围的WiFi，选中需要连接的WiFi名称，输入对应密码即可连接。此外，还支持记住网络，将WiFi名称自动保存在ESP8266等Flash中，方便复位之后自动连接。



