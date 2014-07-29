# -*- coding: utf-8 -*-

"""
pyxdevkit.debugger
~~~~~~~~~~~~~

module that implements the debugger features of xdevkit.
"""
import socket
import sys
from threading import Thread
import select
import threading

class Debugger(object):

	def __init__(self,ip_address,socket):
		self.ip_address = ip_address
		self.socket = socket
		self.on_std_notify_func = None
		self.thread = Thread(target=self.listen_for_notify)
		self.thread.setName('debug_thread')
		self.thread.start()

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

	def listen_for_notify(self):
		""" When the debugger is connected, the console periodically sends back 
			notifications that the used can handle. We just pass them to the 
			on_std_notify_func function.

			TODO: Create EventInfo and EventType objects that act like thier
			xdevkit equivalent.
		"""
		while True:
			for i in threading.enumerate():
   				if i.name == "MainThread" and not i.isAlive():
   					self.socket.close()
   					return
			self.socket.setblocking(0)
			ready = select.select([self.socket], [], [], .3)
			if ready[0]:
				data = self.socket.recv(2048)
				if self.on_std_notify_func:
					self.on_std_notify_func(data)

