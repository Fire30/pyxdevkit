# -*- coding: utf-8 -*-

"""
pyxdevkit.xbox_thread
~~~~~~~~~~~~~

holds functions that an XboxThread can do
"""
import socket


class XboxThread(object):

    def __init__(self, addr, ip_addr):
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
        # It is still in hex so I have to replace it with 0x so that python
        # will understanf
        data = data.replace('0q', '0x')
        registers = {}
        data = data.split('\r\n')
        for register in data:
            # ex register will look like 'gpr5=0x000XX...'
            register_split = register.split('=')
            if len(register_split) > 1:
                registers[register_split[0]] = eval(register_split[1])
        return registers
