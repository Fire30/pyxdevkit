# -*- coding: utf-8 -*-

"""
pyxdevkit.console
~~~~~~~~~~~~~

module that implements xdevkit's methods.
"""
class Console(object):
	"""object that contains the functions that implement xdevkit"""
	def __init__(self, ip_address):
		# Since sdk is not neccasrily installed we use ip address not name to connect
		self.ip_address = ip_address