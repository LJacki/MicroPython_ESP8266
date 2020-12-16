import dht
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

DAT_ID = "9333"
DAT_ID2 = "18324"

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


def updateData(s, id, did, data):
	sayBytes = bytes('{\"M\":\"update\",\"ID\":\"' + id + '\",\"V\":{\"' + did + '\":\"' + data + '\"}}\n','utf8')
	s.sendall(sayBytes)


def updateData2(s, id, did1, data1, did2, data2):
	sayBytes = bytes('{\"M\":\"update\",\"ID\":\"' + id + '\",\"V\":{\"' + did1 + '\":\"' + data1 + '\",\"' + did2 + '\":\"' + data2 +'\"}}\n','utf8')
	s.sendall(sayBytes)


def toggle(pin):
	pin.value(not pin.value())


def blink(time_ms):
	while True:
		# 延时1000ms使ledPin进行数值反转
		ledPin.value(not ledPin.value())
		utime.sleep_ms(1000)


def main():

	# 定义引脚4为控制引脚
	d = dht.DHT11(Pin(4))
	# 先连接WIFI
	connect_wifi()
	# 再连接贝壳物联
	s = socket.socket()
	# 设置超时
	s.settimeout(10)
	connect_bigiot(s)


	while True:

		utime.sleep(2)

		d.measure()
		print("The temperature is : {}".format(d.temperature()))
		print("The humidity is : {}".format(d.humidity()))
		updateData2(s, DEVICEID, DAT_ID, str(d.temperature()), DAT_ID2, str(d.humidity()))
		utime.sleep(3)
