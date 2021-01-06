import socket
import struct

MAC_ADDR = "A4-AE-12-2C-95-84"
BROADCAST_IP = "192.168.1.17"
DEFAULT_PORT = "9"

def create_magic_packet(macaddress):
	"""
	Create a magic packet.

	A magic packet is a packet that can be used with the for wake on lan
	protocol to wake up a computer. The packet is constructed from the
	mac address given as a parameter.

	Args:
		macaddress (str): the mac address that should be parsed into a
			magic packet.

	"""
	if len(macaddress) == 12:
		pass
	elif len(macaddress) == 17:
		sep = macaddress[2]
		macaddress = macaddress.replace(sep, '')
	else:
		raise ValueError('Incorrect MAC address format')

	# Pad the synchronization stream
	data = b'FFFFFFFFFFFF' + (macaddress * 16).encode()
	send_data = b''

	# Split up the hex values in pack
	for i in range(0, len(data), 2):
		send_data += struct.pack(b'B', int(data[i: i + 2], 16))
	return send_data


def send_magic_packet(mac, ip_address, port):
	"""
	Wake up computers having any of the given mac addresses.

	Wake on lan must be enabled on the host device.

	Args:
		macs (str): One or more macaddresses of machines to wake.

	Keyword Args:
		ip_address (str): the ip address of the host to send the magic packet
					 to (default "255.255.255.255")
		port (int): the port of the host to send the magic packet to
			   (default 9)

	"""
	ip = BROADCAST_IP
	port = int(DEFAULT_PORT)

	packet = create_magic_packet(mac)
	print(packet)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	addr = socket.getaddrinfo(ip, port)[0][-1]
	sock.connect(addr)
	sock.send(packet)

	sock.close()
	print('sent to '+ip)



def main():

	send_magic_packet(MAC_ADDR, BROADCAST_IP, DEFAULT_PORT)
