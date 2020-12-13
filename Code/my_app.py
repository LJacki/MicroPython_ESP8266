from machine import Pin
import time
import network
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
	if time.time()-t>30:
		s.sendall(b'{\"M\":\"status\"}\n')
		print('Check status.')
		return time.time()
	else:
		return t


def toggle(pin):
	pin.value(not pin.value())


def blink(time_ms):
	while True:
		# 延时1000ms使ledPin进行数值反转
		ledPin.value(not ledPin.value())
		time.sleep_ms(1000)


def main():

	# 定义引脚2为输出
	ledPin = Pin(2, Pin.OUT)
	# 定义引脚的初始状态为关闭, 此ESP8266模块中on()为LED熄灭；
	ledPin.off()
	
	# 先连接WIFI
	connect_wifi()
	
	# 再连接贝壳物联
	s = socket.socket()
	connect_bigiot(s)
	
	recvData = b''
	t = time.time()
	print("time is :{} ".format(t))
	
	while True:
		try:
			recvData = s.recv(100)
			# print("recvData is :{}\n".format(recvFlag))
			msg = str(recvData, 'utf-8')
			msg = json.loads(msg)
			print("Received Data is : {}".format(msg))
			if msg["C"] == "offOn":
				print("toggle1")
				toggle(ledPin)
				print("toggle2")
			time.sleep(1)
		except:
			pass
#			time.sleep(1)
#			t = keepOnline(s, t)
#			print("Keep Online. t = {}\n".format(t))