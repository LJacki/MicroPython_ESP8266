# 第四回 初入联网（接入了贝壳物联）

本来计划先把所有的硬件介绍完，再介绍如何介入贝壳物联的。但是那样就比较枯燥，还是先尝试接入贝壳物联，来增加ESP8266模块的可玩性。

需要了解[贝壳物联平台通信协议]([贝壳物联平台通讯协议-贝壳物联，让你与智能设备沟通更方便的物联网云平台 (bigiot.net)](https://www.bigiot.net/help/1.html)) ，如果不想了解，可以跳过这3小节，不影响后面继续等到后面有疑问再来这3小节里面寻找。

## 通信协议

这里使用TCP(websocket)长连接协议：

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

这种形式也叫做Json New Line。

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

```json
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
xx3 —— 可变，服务器发送信息时的时间戳，自从 Unix 纪元（格林威治时间 1970 年 1 月 1 日 00:00:00）到当前时间的秒数。发送实时数据

### 发送实时数据

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
   id1 —— 可变，**数据接口ID**，在会员中心查看，
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

## 设备联网

接下来可就是真操实练了，先从ESP8266的内部文件目录搞起。

### 内部文件目录

通过MicroUSB连接ESP8266模块到PC，确保COM端口已经被识别到。PC端打开MicroPython File Uploader.exe工具。

选择COM口，Open。

在命令行中键入：`import os`, `os.listdir()`：

```python
>>> import os
>>> os.listdir()
['boot.py', 'main.py']
```

可以看到在ESP8266模块中，有两个特殊启动文件

- boot.py 
- main.py

当设备启动，一旦文件系统被挂载上，boot.py将会首先执行，而后执行main.py。可以在main.py中创建用户代码，也可以创建自己的用户脚本，并且在main.py中建立关联，如在main.py中写入如下code：

```python
import my_app

my_app.main()
```

并创建my_app.py进行用户代码编写，其中包含main()函数，也可以创建其他用户模块。

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

通过文件传输到ESP8266模块，在MicroPython File Uploader工具（就是第一回中介绍的文件是上传工具）中，选择main.py和my_app.py文件（逐个上传），之后点击send，REPL提示如下：

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

这说明，模块按照预期的那样，依次执行了boot.py，main.py和my_app.py。

## 连接WIFI

接入贝壳物联之前，需要是的ESP8266模块通过WIFI的STA模式连接入网络，可以在my_app.py编辑（一定要修改成自己的热点账号和密码啊）：

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

手机端有设备连接的消息；

### 连接至贝壳物联

在贝壳物联个人中心，添加智能设备，输入设备名称为LED灯（还有一些详细文档可以自行添加），如果不公开设备可以设定为加密等。

返回到智能设备列表，可以获得此设备重要信息，如ID，APIKEY，在线状态以及控制模式等。

==图片==

比较重要的信息为ID和APIKEY（要用自己申请的ID和APIKEY啊），在my_app.py脚本中，将会被定义为常量。

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

==图片==

这样，就完成了这个名称为LED灯的ESP8266模块，通过

1. 先连接网络；
2. 再连接贝壳物联，进行设备登陆

两步骤，完成了设备联网，接入服务器。

## 通过Web/手机控制设备

根据设备入网需求，再8181端口需要设备每隔40~50s向服务器发送依次心跳包，这里先设定每隔40秒（也可以用中断的方式），发送一次check status：

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
			print("Received Data is : {}\n".format(msg))
			if "C" in msg.keys(): # 接收到offOn的命令，执行操作
				if msg["C"] == "offOn":
					toggle(ledPin)
				else:
					print("The other C in msg : {}\n".format(msg["C"]))
			else:
				print("NO keys C in the msg!\n")
			recvData = b''
```

主函数中，先定义LED引脚为输出，再连接WIFI，后连接贝壳物联；通过接受贝壳物联返回的信息， 根据信息`offOn` ，控制LED反转；

通过贝壳物联Web端，或者是微信小程序，就可以控制这个名称为LED灯的设备开关了。延时效果如下：

==图片==

仔细观察开关按钮和ESP8266模块上蓝色的LED灯；

登录[贝壳物联微信小程序](https://www.bigiot.net/mobile.html) ，也可以看到名称为LED灯的设备在线，也同样支持相同的方式进行控制，界面效果如下：

==图片==

想必，细心的你已经发现控制面板上还有很多控制按钮（其实也可以自定义控件），那么就可以根据控件进行其他的控制了，emm后面的内容就更加丰富了。

至此，使用Micropython，配合ESP8266模块，接入贝壳物联这一路也就畅通了。

后面需要做的事情还有很多，比如：

- [ ] 使用中断进行间隔状态查询；
- [ ] 通过AP对wifi的SSID和PASSWORD进行设置；
- [ ] 丰富接收信息处理内容；
- [ ] 丰富ESP8266模块连接硬件的功能；
- [ ] OTA远程软件升级？
- [ ] 模块系统化，精致化等等；

道阻且长，向前进。