import network
import utime
import json
import socket
from machine import Pin

# SSID = "Jack_phone"
# PASSWORD = "695874469"
SSID = "TM-Guest"
PASSWORD = "tianma3809"

# SSID = "Jack_room"
# PASSWORD = "GG179287"

DEVICEID = "10471"
APIKEY = "2530067a3"
host = "www.bigiot.net"
port = 8181

STRING = []

def lcd_init():
	global oled
	from machine import Pin, I2C
	from ssd1306 import SSD1306_I2C

	i2c = I2C(-1, sda = Pin(4), scl = Pin(5), freq = 400000)
	oled = SSD1306_I2C(128, 64, i2c)


def display_l(str, rowBias):
	rowNum = int(len(str)/16 + 1)
	for i in range(rowNum):
		oled.text(str[15*i:15*(i + 1)], 0, (i + rowBias)*8)
		# oled.show()

def display(str):
	global STRING
	ROWBIAS = 0
	STRING.append(str)
	if len(STRING) >= 6:
		STRING= STRING[1:]
	oled.fill(0)
	for i in range(len(STRING)):
		display_l(STRING[i], ROWBIAS)
		ROWBIAS += int(len(STRING[i])/16 + 1)
	utime.sleep(0.5)
	oled.show()


def connect_wifi():
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(True)
	if not wlan.isconnected():
		print('connecting to network...')
		display('connecting to network...')
	wlan.connect(SSID, PASSWORD)
	start = utime.time()
	while not wlan.isconnected():
		utime.sleep(1)
		if utime.time()-start > 5:
			print("connect timeout!")
			display('connect timeout!')
			break
	if wlan.isconnected():
		# ifconfig = wlan.ifconfig()
		print('network config:', wlan.ifconfig())
		display('network config:')
		display(wlan.ifconfig()[0])


def connect_bigiot(s):
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = socket.getaddrinfo(host, port)[0][-1]

	while True:
		try:
			s.connect((addr))
			break
		except:
			print('Waiting for connect bigiot.net')
			utime.sleep(5)
	print('Connect success!')
	display('Connect success')

	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n', 'utf8')
	s.sendall(checkinBytes)
	print('Check in OK!')
	display('Check in OK!')


def check_in(s):
	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n','utf8')
	s.sendall(checkinBytes)
	print('Check in OK!')



def keepOnline(s,t):
	if utime.time()-t>40:
		s.sendall(b'{\"M\":\"status\"}\n')
		print('Check status.')
		display('Check status.')
		return utime.time()
	else:
		return t


def say(s,id, content):
	sayBytes = bytes('{\"M\":\"say\",\"ID\":\"'+id+'\",\"C\":\"'+content+'\"}\n','utf8')
	s.sendall(sayBytes)


def process(s, msg, gpio, switchStatus):
	msg = json.loads(msg)
	if msg['M'] == 'connected':
		check_in(s)
	if msg['M'] == 'login':
		say(s, msg['ID'], 'Welcome! Your public ID is '+msg['ID'])
	if msg['M'] == 'say':
		if msg['C'] == "play":
			display("play!")
			say(s, msg['ID'],'LED turns on!')
			return control(gpio, 1, switchStatus)
		elif msg['C'] == "stop":
			display("stop!")
			say(s, msg['ID'],'LED turns off!')
			return control(gpio, 0, switchStatus)
		elif msg['C'] == "offOn":
			display('offOn!')
			say(s, msg['ID'], 'offOn!')
			switch(gpio)
		else:
			display(msg['C'])

def gpio_init(gpio):
	gpio.value(0)

def control(gpio, status, switchStatus):
	if  not switchStatus :
		if status:
			switch(gpio)
			display('Turn on!')
			return 1
		else:
			display('It\'s already turn off!')
			return 0
	else:
		if not status:
			switch(gpio)
			display('Turn off!')
			return 0
		else:
			display('It\'s already turn on!')
			return 1


def toggle(p):
	p.value(not p.value())

def switch(p):
	p.value(1)
	utime.sleep(0.2)
	p.value(0)

if __name__ == "__main__":
	lcd_init()
	display('Hello , Today is Thursday!')
	connect_wifi()

	#global switchStatus
	switchIO = Pin(14, Pin.OUT)
	# 设定IO为LOW为初始电平
	switchStatus = 0
	gpio_init(switchIO)

	recvData = b""
	recvFlag = True
	t = utime.time()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# the time of recv frequecy
	s.settimeout(4)
	connect_bigiot(s)
	while True:
		try:
			recvData = s.recv(100)
			recvFlag = True
			print("0recvFlag is :\t", recvFlag)
		except:
			recvFlag = False
			utime.sleep(1)
			t = keepOnline(s, t)
			print("1recvFlag is :\t", recvFlag)
		if recvFlag:
			msg = str(recvData, 'utf-8')
			switchStatus = process(s, msg, switchIO, switchStatus)
			print(msg)
			recvData = b''
			print("2recvFlag is :\t", recvFlag)