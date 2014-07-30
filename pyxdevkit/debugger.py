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
from event import EventInfo

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
		sock.send("GO\r\n")
		sock.close()

	def listen_for_notify(self):
		""" When the debugger is connected, the console periodically sends back 
			notifications that the used can handle. We just pass them to the 
			on_std_notify_func function.
		"""
		while True:
			# We need to make sure that the main thread is still running
			# If it is not then we need to stop
			for i in threading.enumerate():
   				if i.name == "MainThread" and not i.isAlive():
   					self.socket.close()
   					return
   			# We just wait until there is something to recieve
			self.socket.setblocking(0)
			ready = select.select([self.socket], [], [], .3)
			if ready[0]:
				# We pass the data of the notification to our function
				# Not that our function takes a string and an EventInfo parameter
				data = self.socket.recv(4096)
				if self.on_std_notify_func:
					for cmd in data.split('\r\n'):
						if cmd:
							e_type = cmd.split(' ')[0]
							e_info = cmd.split(' ')[1:]
							self.on_std_notify_func(e_type,EventInfo(e_info,self.ip_address))

