from machine import Pin
import utime
import network
import json
import socket

SSID = "MEIZU 17"	# 这里为WIFI名称
PASSWORD = "123456.789" # 这里为WIFI密码

DEVICEID = "10471"
APIKEY = "2530067a3"
host = "www.bigiot.net"
port = 8181

def connect_wifi():
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	if not wlan.isconnected():
		print('\nConnecting to network...')
		wlan.connect(SSID, PASSWORD)
		while not wlan.isconnected():
			pass
	print('Network config:', wlan.ifconfig())


def connect_bigiot(s):
	# s = socket.socket()
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = socket.getaddrinfo(host, port)[0][-1]

	try:
		s.connect(addr)
	except:
		print('Waiting for connect bigiot.net')

	print('Connect bigiot success!')
	# 获取会话返回信息
	ans = s.recv(100)
	print(ans)

	# 连接至贝壳物联后，需要通过发送命令，使得设备上线
	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n', 'utf8')
	s.sendall(checkinBytes)
	print('Send check in bytes OK!')
	ans = s.recv(100)
	print(ans)


def keepOnline(s, t):
	if utime.time()-t>40:
		sayBytes = bytes('{\"M\":\"status\"}\n', 'utf8')
		s.sendall(sayBytes)
		ans = s.recv(100)
		print('Check status : {}\n'.format(json.loads(str(ans, 'utf-8'))["M"]))
		return utime.time()
	else:
		return t


def toggle(pin):
	pin.value(not pin.value())


def blink(time_ms):
	while True:
		# 延时1000ms使ledPin进行数值反转
		ledPin.value(not ledPin.value())
		utime.sleep_ms(1000)


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
