# -*- coding: utf-8 -*-

"""
pyxdevkit.console
~~~~~~~~~~~~~

module that implements the debugger features of xdevkit.
"""
import socket
import sys

class Debugger(object):

	def __init__(self,ip_address,socket):
		self.ip_address = addr
		self.socket = socket

	def set_breakpoint(self, addr):
		""" Sets a breakpoint at addr. 
			addr must be a 32 bit integer.
			ex addr = 0x83C88AC4
		"""
		# Set up the socket and connect
		HOST, PORT = self.ip_address, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# This is the cmd that we send to the console
		sock.send("BREAK ADDR=0x%x\r\n" % addr)
		sock.close()

	def go(self):
		""" If a console is currently stopped, eg a breakpoint was hit, 
			it will start the execution again
		"""
		HOST, PORT = self.ip_address, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# This is the cmd that we send to the console
		sock.send("GO\r\n" % addr)
		sock.close()