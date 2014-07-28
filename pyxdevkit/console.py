# -*- coding: utf-8 -*-

"""
pyxdevkit.console
~~~~~~~~~~~~~

module that implements xdevkit's methods.
"""
import socket
import sys

class Console(object):
	"""object that contains the functions that implement xdevkit"""
	def __init__(self, ip_address):
		# Since sdk is not neccasrily installed we use ip address not name to connect
		self.ip_address = ip_address
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
		received = sock.recv(4096 + length)
		received = received.split('\r\n')[1][2:]
		while len(received) < length:
			received += sock.recv(length)[2:]
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
		# This is the cmd that we send to the console
		sock.send("SETMEM ADDR=0x%x DATA=%s\r\n" % (addr,data))