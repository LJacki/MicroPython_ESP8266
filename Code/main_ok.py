import network
import utime
import json
import socket
from machine import Pin

SSID = "jack_fafa"
PASSWORD = "lhy13167033600"

DEVICEID = "10471"
APIKEY = "2530067a3"
host = "www.bigiot.net"
port = 8181


def connect_wifi():
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(True)
	if not wlan.isconnected():
		print('connecting to network...')
		# display('connecting to network...')
	wlan.connect(SSID, PASSWORD)
	start = utime.time()
	while not wlan.isconnected():
		utime.sleep(1)
		if utime.time()-start > 5:
			print("connect timeout!")
			# display('connect timeout!')
			break
	if wlan.isconnected():
		# ifconfig = wlan.ifconfig()
		print('network config:', wlan.ifconfig())
		# display('network config:')
		# display(wlan.ifconfig()[0])


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
	print('Connect bigiot success!')
	# display('Connect success')

	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n', 'utf8')
	s.sendall(checkinBytes)
	print('Check in OK!')
	# display('Check in OK!')


def check_in(s):
	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n','utf8')
	s.sendall(checkinBytes)
	print('Check in OK!')



def keepOnline(s,t):
	if utime.time()-t>40:
		s.sendall(b'{\"M\":\"status\"}\n')
		print('Check status.')
		# display('Check status.')
		return utime.time()
	else:
		return t


def say(s,id, content):
	sayBytes = bytes('{\"M\":\"say\",\"ID\":\"'+id+'\",\"C\":\"'+content+'\"}\n','utf8')
	s.sendall(sayBytes)

def gpio_init(gpio):
	gpio.value(0)

def toggle(pin):
	pin.value(not pin.value())


def switch(pin):
	pin.value(1)
	utime.sleep(0.5)
	pin.value(0)

def process(s, msg, gpio, ioStatus):
	msg = json.loads(msg)
	if msg['M'] == 'connected':
		check_in(s)
	if msg['M'] == 'login':
		say(s, msg['ID'], 'Welcome! Your public ID is '+msg['ID'])
	if msg['M'] == 'say':
		if msg['C'] == "play":
			say(s, msg['ID'],'LED turns on!')
			return control(gpio, 1, ioStatus)
		elif msg['C'] == "stop":
			say(s, msg['ID'],'LED turns off!')
			return control(gpio, 0, ioStatus)
		elif msg['C'] == "offOn":
			say(s, msg['ID'], 'offOn!')
			toggle(gpio)
		else:
			print(msg['C'])


def control(gpio, status, ioStatus):
	if  not ioStatus :
		if status:
			switch(gpio)
			print('Turn on!')
			return 1
		else:
			print('It\'s already turn off!')
			return 0
	else:
		if not status:
			switch(gpio)
			print('Turn off!')
			return 0
		else:
			print('It\'s already turn on!')
			return 1


if __name__ == "__main__":
	# 首先需要连接WIFI
	connect_wifi()

	# IO控制
	ledIO = Pin(2, Pin.OUT)
	ioStatus = 1
	gpio_init(ledIO)

	t = utime.time()
	print("time is :{} ".format(t))

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(4)
	connect_bigiot(s)

	recvData = b''
	recvFlag = True

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
			print("received data is : {}".format(msg))
			ioStatus = process(s, msg, ledIO, ioStatus)
			recvData = b''
			print("2recvFlag is :\t", recvFlag)
