import dht
from machine import Pin
import utime
import socket
from machine import Timer


DEVICEID = "10471"
APIKEY = "2530067a3"
host = "www.bigiot.net"
port = 8181

DAT_ID = "9333"
DAT_ID2 = "18324"


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
	ans = s.recv(500)
	print(ans)

	# 连接至贝壳物联后，需要通过发送命令，使得设备上线
	checkinBytes = bytes('{\"M\":\"checkin\",\"ID\":\"' + DEVICEID + '\",\"K\":\"' + APIKEY + '\"}\n', 'utf8')
	s.sendall(checkinBytes)
	print('Send check in bytes OK!')
	ans = s.recv(500)
	print(ans)


def isOL(s):
	checkinBytes = bytes('{\"M\":\"isOL\",\"ID\": [\"D' + DEVICEID + '\"]}\n', 'utf8')
	s.sendall(checkinBytes)
	print('Check isOL!')
	ans = s.recv(500)
	print(ans)


def updateData(s, id, did, data):
	sayBytes = bytes('{\"M\":\"update\",\"ID\":\"' + id + '\",\"V\":{\"' + did + '\":\"' + data + '\"}}\n', 'utf8')
	s.sendall(sayBytes)


def updateData2(s, id, did1, data1, did2, data2):
	sayBytes = bytes(
		'{\"M\":\"update\",\"ID\":\"' + id + '\",\"V\":{\"' + did1 + '\":\"' + data1 + '\",\"' + did2 + '\":\"' + data2 + '\"}}\n',
		'utf8')
	s.sendall(sayBytes)


def IRQ_heartBear(s):
	"""设定中断函数，定时心跳与贝壳物联通信"""
	sayBytes = bytes('{\"M\":\"status\"}\n', 'utf8')
	s.sendall(sayBytes)
	print("Heart Beating!")


def dht_measure(dhtname):
	dhtname.measure()
	temperature = dhtname.temperature()
	humidity = dhtname.humidity()
	return temperature, humidity


def dht_updata(s, dhtname):
	utime.sleep(5)

	(temp, hudt) = dht_measure(dhtname)
	print("The temperature is : {: >2d} C".format(temp))
	print("The humidity    is : {: >2d} %".format(hudt))
	updateData2(s, DEVICEID, DAT_ID, str(temp), DAT_ID2, str(hudt))


def toggle(pin):
	pin.value(not pin.value())


def blink(ledPin, time_ms):
	while True:
	# 延时1000ms使ledPin进行数值反转
		ledPin.value(not ledPin.value())
		utime.sleep_ms(1000)


def main():
	# 定义引脚4为控制引脚
	dht0 = dht.DHT11(Pin(4))

	# 连接贝壳物联
	s = socket.socket()
	s.settimeout(10)

	connect_bigiot(s)

	# 中断设定回调心跳服务函数
	timer0 = Timer(-1)
	timer0.init(period=20000, mode=Timer.PERIODIC, callback=lambda t:IRQ_heartBear(s))

	timeNum = 0
	while True:
		utime.sleep_ms(1000)
		timeNum += 1
		print(timeNum)
		# dht_updata(s, dht0)
