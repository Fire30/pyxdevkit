# -*- coding: utf-8 -*-

"""
pyxdevkit.exceptions
~~~~~~~~~~~~~

module that implements exceptions in xdevkit
"""
class XDevkitError(Exception):
	pass

class ConnectionError(XDevkitError):
	def __init__(self,ip_addr):
		msg = "Unable to Connect to %s" % (ip_addr)
		XDevkitError.__init__(self,msg)

class NotConnectedError(XDevkitError):
	def __init__(self):
		XDevkitError.__init__(self,"Console is currently not connected")