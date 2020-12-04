import socket
import time
import json


DEVICEID = "10471"
APIKEY = "2530067a3"
host = "www.bigiot.net"
port = 8181

# {"M":"checkin","ID":"10471","K":"2530067a3"}
# {"M":"isOL","ID":"10471"}
# {"M":"status"}
# {"M":"time","F":"Y-m-d H:i:s"}
# {"M":"checkout","ID":"10471","K":"2530067a3"}

def http_get(url):
	# _, _, host, path = url.split('/', 3)
	addr = socket.getaddrinfo(url, 8181)[0][-1]
	s = socket.socket()
	s.connect(addr)

	s.send(bytes('GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % (url), 'utf8'))
	while True:
		data = s.recv(100)
		if data:
			print(str(data, 'utf8'), end='')
		else:
			break

	print("break")

	s.close()


def connect_test():
	#connect bigiot
	global s
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(0)
	while True:
		try:
			addr = socket.getaddrinfo(host,port)[0][-1]
			s.connect((addr))
			break
		except:
			print('waiting for connect bigiot.net...')
			time.sleep(2)
	#check in bigiot
	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n',encoding='utf8')
	s.sendall(checkinBytes)


def connect_bigiot1():
	# connect bigiot
	# 创建一个socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# s.settimeout(10)
	# 建立连接
	while True:
		try:
			s.connect((host,port))
			break
		except:
			print('Waiting for connect bigiot.net')
			time.sleep(2)

	print('Connect success!')

	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n',encoding='utf8')
	s.sendall(checkinBytes)
	# while True:
	# 	data = s.recv(1)
	# 	if data :
	# 		print(str(data, 'utf8'), end='')
	# 	else:
	# 		break
	print('Check in OK!')


def connect_bigiot(s):
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	while True:
		try:
			s.connect((host,port))
			break
		except:
			print('Waiting for connect bigiot.net')
			time.sleep(2)
	print('Connect success!')

	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n',encoding='utf8')
	s.sendall(checkinBytes)

	print('Check in OK!')


def check_in(s):
	checkinBytes=bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n',encoding='utf8')
	s.sendall(checkinBytes)
	print('Check in OK!')



def keepOnline(s,t):
	if time.time()-t>40:
		s.sendall(b'{\"M\":\"status\"}\n')
		print('check status')
		return time.time()
	else:
		return t


def say(s,id, content):
	sayBytes = bytes('{\"M\":\"say\",\"ID\":\"'+id+'\",\"C\":\"'+content+'\"}\n',encoding='utf8')
	s.sendall(sayBytes)


def process(s,msg):
	msg = json.loads(msg)
	if msg['M'] == 'connected':
		check_in(s)
	if msg['M'] == 'login':
		say(s, msg['ID'],'Welcome! Your public ID is '+msg['ID'])
	if msg['M'] == 'say':
		if msg['C'] == "play":
			print("play!")
			say(s, msg['ID'],'LED turns on!')
		if msg['C'] == "stop":
			print("stop!")
			say(s, msg['ID'],'LED turns off!')

if __name__ == "__main__":
	recvData = b''
	recvChar = b''
	recvFLag = True
	t = time.time()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# the time of recv frequecy
	s.settimeout(4)
	connect_bigiot(s)

	while True:

		try:
			recvChar = s.recv(1)
			recvFLag = True
			print("recvChar is:\t", recvChar)
		except:
			recvFLag = False
			time.sleep(1)
			t = keepOnline(s, t)
			print("1recvFlag is :\t1")

		if recvFLag :
			if recvChar != b'\n':
				recvData += recvChar
				print("recvData is:\t", recvData)
			else:
				msg = str(recvData, encoding='utf-8')
				process(s, msg)
				print("here is the msg:\t", msg)
				recvData = b''
				print("2recvFlag is :\t2")
