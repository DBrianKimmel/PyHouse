'''
Created on Mar 21, 2013

@author: briank
'''

__version_info__ = (1, 1, 0)
__version__ = '.' . join(map(str, __version_info__))

import serial
import serial.tools.list_ports

VALID_INTERFACES = ['Serial', 'USB', 'Ethernet']

g_debug = 0

class SerialData(object):

    def __init__(self):
        self.BaudRate = 9600
        self.ByteSize = 8
        self.DsrDtr = False
        self.InterCharTimeout = 0
        self.Parity = 'N'
        self.RtsCts = False
        self.StopBits = 1.0
        self.Timeout = None
        self.WriteTimeout = None
        self.XonXoff = False

    def __str__(self):
        l_ret = "Serial:: Baud:{0:}, ByteSize:{1:}, Parity:{2:}, StopBits:{3:}; ".format(self.BaudRate, self.ByteSize, self.Parity, self.StopBits)
        return l_ret


class USBData(object):

    def __init__(self):
        self.Product = 0
        self.Vendor = 0

    def __str__(self):
        l_ret = "USB:: Vendor:{0:#04X}, Product:{1:#04X}; ".format(self.Vendor, self.Product)
        return l_ret


class  EthernetData(object):

    def __init__(self):
        pass

# ## END
