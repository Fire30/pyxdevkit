# -*- coding: utf-8 -*-

"""
pyxdevkit.console
~~~~~~~~~~~~~

module that implements xdevkit's methods.
"""
import socket
from debugger import Debugger

class Console(object):
	"""object that contains the functions that implement xdevkit"""
	def __init__(self, ip_address):
		# Since sdk is not neccasrily installed we use ip address not name to connect
		self.ip_address = ip_address
		self.debugger = None

	def get_name(self):
		"""Gets the name of the connected console"""
		# Set up the socket and connect
		HOST, PORT = self.ip_address, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# This is the cmd that we send to the console
		sock.send("DBGNAME\r\n")
		#First recv just says that we are connected
		sock.recv(1024)
		name = sock.recv(1024)
		return name[5:]

	def get_mem(self,addr,length):
		"""Returns the length amount of memory from addr"""
		# Set up the socket and connect
		HOST, PORT = self.ip_address, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# This is the cmd that we send to the console
		sock.send("GETMEMEX ADDR=0x%x LENGTH=0x%x\r\n" % (addr,length))
		# The first response is always 201-connected
		# This is weird because when I do it using C# and xdevkit this doesn't happen
		sock.recv(1024)
		# The first thing returned will be 203- binary response follows\r\n, + the data.
		# If the length is small it will be returned all in one recv.
		# If it is larger it will take multiple.
		# Note: The first two bytes of the binary response are not part of the memory
		sock.settimeout(.2)
		received = sock.recv(4096 + length)
		received = received.replace('203- binary response follows\r\n','')[2:]
		while len(received) < length:
			try:
				data = sock.recv(1026)
				received += data[2:]
			except:
				sock.close()
				return received
		sock.close()
		return received

	def set_mem(self,addr,data):
		""" Sets the memory at addr to data
			The value in data has to be a string of hexadecimal characters
			so for example data = 'DEADBEEF' is fine
		"""
		# Set up the socket and connect
		HOST, PORT = self.ip_address, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# This is the cmd that we send to the consoles
		sock.send("SETMEM ADDR=0x%x DATA=%s\r\n" % (addr,data))
		sock.close()

	def connect_as_debugger(self, name):
		""" Connects as a debugger so you can do things such as setting breakpoints.
			There is also a flags parameter in the C# dll
			but it does not seem to change the request when I monitor the requests.
			So it has been ommited
		"""
		# Set up the socket and connect
		HOST, PORT = self.ip_address, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# Connecting as a debugger actually takes two requests.
		# First you have to specify a reconnect port
		# Then you actually have to connect
		sock.send("NOTIFY RECONNECTPORT=51523 reverse\r\n")
		# Create the consoles debugger
		# Now we are able to do things such as set breakpoints 
		self.debugger = Debugger(self.ip_address,sock)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		sock.send('DEBUGGER CONNECT PORT=0x0000C901 override user=WINCTRL-TQMC306 name="%s"\r\n' % name)

	def reboot(self):
		""" Reboots the console. """
		HOST, PORT = self.ip_address, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		sock.send("magicboot COLD\r\n")
