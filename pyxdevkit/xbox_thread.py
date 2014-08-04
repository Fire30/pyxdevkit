# -*- coding: utf-8 -*-

"""
pyxdevkit.xbox_thread
~~~~~~~~~~~~~

holds functions that an XboxThread can do
"""
import socket

class XboxThread(object):
	def __init__(self,addr,ip_addr):
		self.addr = addr
		self.ip_addr = ip_addr

	def t_continue(self):
		"""
			Tells the xbox to make the thread continue
			Thread has to be a 32 bit integer
		"""
		HOST, PORT = self.ip_addr, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# This is the cmd that we send to the console
		sock.send("CONTINUE THREAD=0x%x EXCEPTION\r\n" % self.addr)
		sock.close()
		['Cr', 'Ctr', 'Fpr0', 'Fpr1', 'Fpr10', 'Fpr11', 'Fpr12', 'Fpr13', 'Fpr14', 'Fpr15', 'Fpr16', 'Fpr17', 'Fpr18', 'Fpr19', 'Fpr2', 'Fpr20', 'Fpr21', 'Fpr22', 'Fpr23', 'Fpr24', 'Fpr25', 'Fpr26', 'Fpr27', 'Fpr28', 'Fpr29', 'Fpr3', 'Fpr30', 'Fpr31', 'Fpr4', 'Fpr5', 'Fpr6', 'Fpr7', 'Fpr8', 'Fpr9', 'Fpscr', 'Gpr0', 'Gpr1', 'Gpr10', 'Gpr11', 'Gpr12', 'Gpr13', 'Gpr14', 'Gpr15', 'Gpr16', 'Gpr17', 'Gpr18', 'Gpr19', 'Gpr2', 'Gpr20', 'Gpr21', 'Gpr22', 'Gpr23', 'Gpr24', 'Gpr25', 'Gpr26', 'Gpr27', 'Gpr28', 'Gpr29', 'Gpr3', 'Gpr30', 'Gpr31', 'Gpr4', 'Gpr5', 'Gpr6', 'Gpr7', 'Gpr8', 'Gpr9', 'Iar', 'Lr', 'Msr', 'Vr0', 'Vr1', 'Vr10', 'Vr100', 'Vr101', 'Vr102', 'Vr103', 'Vr104', 'Vr105', 'Vr106', 'Vr107', 'Vr108', 'Vr109', 'Vr11', 'Vr110', 'Vr111', 'Vr112', 'Vr113', 'Vr114', 'Vr115', 'Vr116', 'Vr117', 'Vr118', 'Vr119', 'Vr12', 'Vr120', 'Vr121', 'Vr122', 'Vr123', 'Vr124', 'Vr125', 'Vr126', 'Vr127', 'Vr13', 'Vr14', 'Vr15', 'Vr16', 'Vr17', 'Vr18', 'Vr19', 'Vr2', 'Vr20', 'Vr21', 'Vr22', 'Vr23', 'Vr24', 'Vr25', 'Vr26', 'Vr27', 'Vr28', 'Vr29', 'Vr3', 'Vr30', 'Vr31', 'Vr32', 'Vr33', 'Vr34', 'Vr35', 'Vr36', 'Vr37', 'Vr38', 'Vr39', 'Vr4', 'Vr40', 'Vr41', 'Vr42', 'Vr43', 'Vr44', 'Vr45', 'Vr46', 'Vr47', 'Vr48', 'Vr49', 'Vr5', 'Vr50', 'Vr51', 'Vr52', 'Vr53', 'Vr54', 'Vr55', 'Vr56', 'Vr57', 'Vr58', 'Vr59', 'Vr6', 'Vr60', 'Vr61', 'Vr62', 'Vr63', 'Vr64', 'Vr65', 'Vr66', 'Vr67', 'Vr68', 'Vr69', 'Vr7', 'Vr70', 'Vr71', 'Vr72', 'Vr73', 'Vr74', 'Vr75', 'Vr76', 'Vr77', 'Vr78', 'Vr79', 'Vr8', 'Vr80', 'Vr81', 'Vr82', 'Vr83', 'Vr84', 'Vr85', 'Vr86', 'Vr87', 'Vr88', 'Vr89', 'Vr9', 'Vr90', 'Vr91', 'Vr92', 'Vr93', 'Vr94', 'Vr95', 'Vr96', 'Vr97', 'Vr98', 'Vr99', 'Vscr', 'Xer']
	def get_registers(self):
		"""	Returns a dict of all the registers in the xbox
			Register keys are:
				Fpr0-31
				Gpr0-31
				Vr0-127
				Cr
				Ctr
				Fpscr
				Iar
				Lr
				Msr
				Vscr
				Xer
		"""
		HOST, PORT = self.ip_addr, 730
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		# This is the cmd that we send to the console
		sock.send("GETCONTEXT THREAD=0x%x CONTROL INT FP VR\r\n" % self.addr)
		data = ''
		# The character that is sent when everything is done is '.'
		while '.' not in data:
			data += sock.recv(8092)
		sock.close()
		# The general purpose registers all have 0q followed by a 64 bit int
		# It is still in hex so I have to replace it with 0x so that python will understanf
		data = data.replace('0q','0x')
		registers = {}
		data = data.split('\r\n')
		for register in data:
			#ex register will look like 'gpr5=0x000XX...'
			register_split = register.split('=')
			if len(register_split) > 1:
				registers[register_split[0]] = eval(register_split[1])
		return registers
