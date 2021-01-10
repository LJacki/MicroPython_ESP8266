# MicroPython_ESP8266_IoT——第五回 网页配置（局域网连接WiFi）

参考官方手册中，对network库的介绍：[`network`——network configuration](http://docs.micropython.org/en/latest/library/network.html) 。

建议在REPL中，通过命令行逐个熟悉提示到的方法，加深理解。

## network模块介绍

此模块提供网络连接的驱动，以及路由配置。配置网络后，可以通过`usocket`模块获取网络服务。使用起来非常方便，官网教程中也给了例子：

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

### 网络适配接口

这里描述的`network`接口针对不同的MicroPython硬件有不同的实例。提供的WiFi网络处理驱动，示例如下：

```python
import network
# enable station interface and connect to WiFi access point
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('your-ssid', 'your-password')
# now use sockets as usual
```

其中适用于ESP8266的为`class WLAN`，那就以`class WLAN`[control built-in WiFi interfaces](http://docs.micropython.org/en/latest/library/network.WLAN.html#class-wln-control-built-in-wifi-interfaces) 为例，看看有哪些方法。

### 创建对象

WLAN 网络接口对象有两种：

1. `network.STA_IF`（station，也叫做client，是连接到上游WiFi接入点）；
2. `network.AP_IF`（access point，允许其他WiFi clients连接）；

下面提到的方法是否可用取决于接口的类型，比如只有STA接口支持`WLAN.connect()`来接入access point。如下列举此类中的方法：

- WLAN.active([is_active])
- WLAN.connect(ssid=None, password=None, *, bssid=None)
- WLAN.disconnect()
- WLAN.scan()
- WLAN.status([param])
- WLAN.isconnected()
- WLAN.ifconfig([(ip, subnet, gateway, dns)])
- WLAN.config(‘param’)
- WLAN.config(param=value,…)

这些都比较好理解，根据方法的名称基本就能了解个大概，详细说明可参考官方手册中的[WLAN.()介绍](http://docs.micropython.org/en/latest/library/network.WLAN.html)。

### 关键方法WLAN.scan()

此处主要介绍`WLAN.scan()`，用于扫描可用的无线网络（类似于手机打开WiFi之后，就开始搜索附近可用的无线网络）。

扫描方法只适用于`STA接口`，会返回包含WiFi接入点的信息元组组成的列表，内容如下：

> ssid（WiFi ID）, bssid（MAC）, channel（信道）；
>
> RSSI（信号强度）, authmode（加密模式）, hidden（隐藏）；

其中，`bssid`为接入点硬件地址，为二进制格式，返回为`bytes`对象。可以使用`ubinascii.hexlify()` 转换为ASCII格式。

`authmode`加密方（没有过多了解这些方式的区别，又兴趣可自行探索）有5个值：

- 0 - 不加密；
- 1 - WEP；
- 2 - WPA-PSK；
- 3 - WPA2-PSK；
- 4 - WPA/WPA2-PSK;

`hidden`的值也有两种：

- 0 - visible；
- 1 - hidden；

看过了这些方法，可以在`REPL`中挨个使用，加深对这些方法的理解（务必学会现在REPL中调试，再向ESP8266中传输文件）；

## WiFi Manager Works

这一部分内容并非本人原创，[这里为Github仓库地址](https://github.com/tayfunulu/WiFiManager) 。使用tayfunuln的WiFiManager，可以使用MicroPython配合ESP32或ESP8266等硬件，进行Wi-Fi连接的管理。

可以理解为手机打开WiFi的开关后，自动搜索周围的WiFi，选中需要连接的WiFi名称，输入对应密码即可连接。此外，还支持记住网络，将WiFi名称自动保存在ESP8266等Flash中，方便复位之后自动连接。

### 使用场景

方便在更换使用环境的时候，不需要重新在code中修改SSID和PASSWORD，重新烧录程序。

可以想象这么个场景，花时间和心思DIY了一个好玩的，想要分享给女朋友，难道还想要女朋友自己在源码中修改WiFi的账号和密码，再烧录到板子中吗？（如果你不使用Wi-Fi Manager，那么也就只能提前将源码修改好再给女朋友了）

使用ESP8266建立Access Point，之后同通过web配置网络信息，而且可以自动连接已经保存的网络，使用界面如下：

![Wi-Fi Client Setup WiFi Manager MicroPython](https://i2.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/11/wifi-manager-esp32-micropython-show-available-networks.png?resize=375%2C389&quality=100&strip=all&ssl=1)

看起来跟手机直连WiFi差不多操作了。

### 工作原理

WiFi管理模块是这样工作的：

- EPS8266模块第一次重启，会建立Access Point（名称和密码再源码中设定的）；
- 连接至上述Access Point后，在浏览器中输入IP地址`192.168.4.1`；
- 通过显示出的网页，选择一个SSID，并输入密码，点击`submit`;
- ESP8266保存网络的SSID和输入的PASSWORD，转换为Station mode连接入对应的WiFi网络；
- 当新的SSID和PASSWORD设定，ESP8266每次重启，都会被设定为Station mode并尝试连接之前保存的WiFi网络；
- 建立连接后，此模块操作就完成了。否则就回到第一步需要重新配置WiFi网络；

在[仓库WiFiManager](https://github.com/tayfunulu/WiFiManager)的主页中README中，可以找到工作原理的框图：

![alt text](https://github.com/tayfunulu/WiFiManager/raw/master/WiFi_Manager.png)

## WiFi Manager MicroPython 源码

因为是非官方的库，所以需要将源码保存到ESP8266设备上保存文件名称为`wifimgr.py`，方便在`main.py`中调用，源码如下：

```python
import network
import socket
import ure
import time

ap_ssid = "WifiManager"
ap_password = "tayfunulu"
ap_authmode = 3  # WPA2

NETWORK_PROFILES = 'wifi.dat'

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None


def get_connection():
    """return a working WLAN(STA_IF) instance or None"""

    # First check if there already is any connection:
    if wlan_sta.isconnected():
        return wlan_sta

    connected = False
    try:
        # ESP connecting to WiFi takes time, wait a bit and try again:
        time.sleep(3)
        if wlan_sta.isconnected():
            return wlan_sta

        # Read known network profiles from file
        profiles = read_profiles()

        # Search WiFis in range
        wlan_sta.active(True)
        networks = wlan_sta.scan()

        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            print("ssid: %s chan: %d rssi: %d authmode: %s" % (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
            if encrypted:
                if ssid in profiles:
                    password = profiles[ssid]
                    connected = do_connect(ssid, password)
                else:
                    print("skipping unknown encrypted network")
            else:  # open
                connected = do_connect(ssid, None)
            if connected:
                break

    except OSError as e:
        print("exception", str(e))

    # start web server for connection manager:
    if not connected:
        connected = start()

    return wlan_sta if connected else None


def read_profiles():
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles


def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))


def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(100):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected


def send_header(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")


def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()


def handle_root(client):
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    send_header(client)
    client.sendall("""\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Wi-Fi Client Setup
                </span>
            </h1>
            <form action="configure" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
    """)
    while len(ssids):
        ssid = ssids.pop(0)
        client.sendall("""\
                        <tr>
                            <td colspan="2">
                                <input type="radio" name="ssid" value="{0}" />{0}
                            </td>
                        </tr>
        """.format(ssid))
    client.sendall("""\
                        <tr>
                            <td>Password:</td>
                            <td><input name="password" type="password" /></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            <p>&nbsp;</p>
            <hr />
            <h5>
                <span style="color: #ff0000;">
                    Your ssid and password information will be saved into the
                    "%(filename)s" file in your ESP module for future usage.
                    Be careful about security!
                </span>
            </h5>
            <hr />
            <h2 style="color: #2e6c80;">
                Some useful infos:
            </h2>
            <ul>
                <li>
                    Original code from <a href="https://github.com/cpopp/MicroPythonSamples"
                        target="_blank" rel="noopener">cpopp/MicroPythonSamples</a>.
                </li>
                <li>
                    This code available at <a href="https://github.com/tayfunulu/WiFiManager"
                        target="_blank" rel="noopener">tayfunulu/WiFiManager</a>.
                </li>
            </ul>
        </html>
    """ % dict(filename=NETWORK_PROFILES))
    client.close()


def handle_configure(client, request):
    match = ure.search("ssid=([^&]*)&password=(.*)", request)

    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return False
    # version 1.9 compatibility
    try:
        ssid = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
        password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
    except Exception:
        ssid = match.group(1).replace("%3F", "?").replace("%21", "!")
        password = match.group(2).replace("%3F", "?").replace("%21", "!")

    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return False

    if do_connect(ssid, password):
        response = """\
            <html>
                <center>
                    <br><br>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP successfully connected to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                </center>
            </html>
        """ % dict(ssid=ssid)
        send_response(client, response)
        try:
            profiles = read_profiles()
        except OSError:
            profiles = {}
        profiles[ssid] = password
        write_profiles(profiles)

        time.sleep(5)

        return True
    else:
        response = """\
            <html>
                <center>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP could not connect to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                    <form>
                        <input type="button" value="Go back!" onclick="history.back()"></input>
                    </form>
                </center>
            </html>
        """ % dict(ssid=ssid)
        send_response(client, response)
        return False


def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)


def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None


def start(port=80):
    global server_socket

    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

    stop()

    wlan_sta.active(True)
    wlan_ap.active(True)

    wlan_ap.config(essid=ap_ssid, password=ap_password, authmode=ap_authmode)

    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)

    print('Connect to WiFi ssid ' + ap_ssid + ', default password: ' + ap_password)
    print('and access the ESP via your favorite web browser at 192.168.4.1.')
    print('Listening on:', addr)

    while True:
        if wlan_sta.isconnected():
            return True

        client, addr = server_socket.accept()
        print('client connected from', addr)
        try:
            client.settimeout(5.0)

            request = b""
            try:
                while "\r\n\r\n" not in request:
                    request += client.recv(512)
            except OSError:
                pass

            print("Request is: {}".format(request))
            if "HTTP" not in request:  # skip invalid requests
                continue

            # version 1.9 compatibility
            try:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
            except Exception:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
            print("URL is {}".format(url))

            if url == "":
                handle_root(client)
            elif url == "configure":
                handle_configure(client, request)
            else:
                handle_not_found(client, url)

        finally:
            client.close()
```

 需要自定义的宏为：

```python
ap_ssid = "WifiManager"			# 这是ESP8266 接入点的名称
ap_password = "tayfunulu"		# 这是ESP8266 接入点的密码
ap_authmode = 3  # WPA2`		# 这是协议类型，可默认为3
```

### main.py

配合模块使用需要修改main.py的源码为：

```python
import wifimgr # 这个模块名称务必要与上述WiFiManager模块文件名一致

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")
```

**这个import的模块名称务必要与上述WiFiManager模块文件名一致** 。

## WiFi Manger模块测试

通过[系列文章第四回](https://github.com/LJacki/MicroPython_ESP8266/blob/main/%E4%B8%93%E6%A0%8F%E7%B3%BB%E5%88%97%E6%96%87%E7%AB%A0/MicroPython_ESP8266_IoT%E2%80%94%E2%80%94%E7%AC%AC%E5%9B%9B%E5%9B%9E%20%E5%88%9D%E5%85%A5%E8%81%94%E7%BD%91%EF%BC%88%E6%8E%A5%E5%85%A5%E4%BA%86%E8%B4%9D%E5%A3%B3%E7%89%A9%E8%81%94%EF%BC%89.md)中介绍的方式，将main.py和wifimgr.py烧录至ESP8266的Flash中，并进行**复位**操作，就可以在REPL中看到相应的串口信息提示：

```bash
Connect to WiFi ssid WifiManager, default password: tayfunulu and access the ESP via your favourite web browser at 192.168.4.1.
Listening on:('0.0.0', 80)
```

按照上述提示，使用手机或者有WiFi的电脑，接入Access Point：WifiManager，密码：tayfunulu（如果修改过，请输入自己修改后的密码）：

![Connect to WiFiManager Network ESP32 MicroPython](https://i1.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/11/connect-to-wifimanager-network.png?resize=375%2C475&quality=100&strip=all&ssl=1)

当连接WiFiManager网络成功后，在浏览器地址栏输入IP`192.268.4.1`，就会返回得到如下网页：

![Selecting Wi-Fi Network - WiFiManager MicroPython ESP32](https://i1.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/11/selecting-wi-fi-network-wifimanager.png?resize=750%2C525&quality=100&strip=all&ssl=1)

选择你的网络，并输入PASSWORD，点击`Submit`，加载完成后可以跳转到连接成功界面：

![ESP32 successfully connected to Wifi Network - WiFiManager](https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/11/successfully-connected-to-network-wifimanager.png?resize=747%2C245&quality=100&strip=all&ssl=1)

同时，REPL也会出现接入WiFi的提示：

![ESP32 Station IP Address - WiFiManager MicroPython](https://i2.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/11/wifi-manager-esp32-station-ip.png?resize=707%2C221&quality=100&strip=all&ssl=1)

显示已经接入WiFi，以及相应的IP，掩码，网关等；

最主要的是，在REPL中显示：

```bash
ESP OK
```

这就说明，在main.py中，已经运行到了最后一句。也就是说已经成功完成了配置WiFi的操作，如果后续有什么功能，就可以继续下去。

## 结束语

通过Web配置WIFI肯定不是唯一的方法。相对于再源码里面修改WIFI的配置信息来说，这样显得更加人性化，毕竟不是每个人都喜欢捣鼓这些玩意儿。

笔者对HTML不熟悉，有兴趣页面应该可以做的更好看点。

还有，切勿拿来主义，只有学习的态度是不能够的，更重要的是真的去学习。

## 参考连接

1. https://randomnerdtutorials.com/micropython-wi-fi-manager-esp32-esp8266/
2. https://github.com/tayfunulu/WiFiManager

