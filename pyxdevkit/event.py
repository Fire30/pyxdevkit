# -*- coding: utf-8 -*-

"""
pyxdevkit.event
~~~~~~~~~~~~~

module that implements the event object that is used in xdevkit
"""
from xbox_thread import XboxThread


class EventInfo(object):

    def __init__(self, properties, ip_addr):
        """
            Basically the event just holds information that we can use in our notify function
            Note: These are not all the parameters, since the parameters are always different
            They are instead some of the ones that are needed for other things.
        """
        self.properties = properties
        self.ip_addr = ip_addr
        self.is_stopped = False
        self.start = None
        self.addr = None
        for prop in properties:
            if 'thread=' in prop:
                # We create a thread object so we can get registers and stuff
                self.thread = XboxThread(
                    int(prop.replace('thread=', ''), 16), self.ip_addr)
            if 'stop' in prop:
                self.is_stopped = True
            if 'start=' in prop:
                self.start = int(prop.replace('start=', ''), 16)
            if 'addr=' in prop:
                self.addr = int(prop.replace('addr=', ''), 16)
