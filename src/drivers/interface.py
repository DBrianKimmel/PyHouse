'''
Created on Mar 21, 2013

@author: briank
'''

__version_info__ = (1, 1, 0)
__version__ = '.' . join(map(str, __version_info__))


# Import PyMh files
from utils import xml_tools

g_debug = 9

VALID_INTERFACES = ['Serial', 'USB', 'Ethernet']
#SERIAL_ATTRS = {'BaudRate': self.get_text_element,
#                'ByteSize': get_int_element,
#                'DsrDtr': get_bool_element,
#                'Parity': get_text_element,
#                'RtsCts': get_bool_element,
#                'StopBits': get_float_element,
#                'Timeout':get_float_element,
#                'XonXoff': get_bool_element}


class SerialData(object):

    def __init__(self):
        self.BaudRate = 9600
        self.ByteSize = 8
        self.DsrDtr = False
        self.Parity = 'N'
        self.RtsCts = False
        self.StopBits = 1.0
        self.Timeout = None
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


class ReadWriteConfig(xml_tools.ConfigTools):

    def _get_attrs(self, p_obj):
        l_attrs = filter(lambda aname: not aname.startswith('__'), dir(p_obj))
        return l_attrs

    def extract_serial_xml(self, p_controller_obj, p_controller_xml):
        if g_debug >= 2:
            print "extract_serial_xml() "
        #for l_attr, l_method in SERIAL_ATTRS:
        #    setattr(p_controller_obj, l_attr, l_method(p_controller_xml, l_attr))
        l_serial = SerialData()
        l_xml = p_controller_xml
        l_serial.BaudRate = self.get_text_element(l_xml, 'BaudRate')
        l_serial.ByteSize = self.get_int_element(l_xml, 'ByteSize')
        l_serial.DsrDtr = self.get_bool_element(l_xml, 'DsrDtr')
        l_serial.Parity = self.get_text_element(l_xml, 'Parity')
        l_serial.RtsCts = self.get_bool_element(l_xml, 'RtsCts')
        l_serial.StopBits = self.get_float_element(l_xml, 'StopBits')
        l_serial.Timeout = self.get_float_element(l_xml, 'Timeout')
        l_serial.XonXoff = self.get_bool_element(l_xml, 'XonXoff')
        l_attrs = self._get_attrs(l_serial)
        for l_attr in l_attrs:
            setattr(p_controller_obj, l_attr, getattr(l_serial, l_attr))

    def extract_usb_xml(self, p_controller_obj, p_controller_xml):
        if g_debug >= 2:
            print "extract_usb_xml() "
        l_usb = USBData()
        l_xml = p_controller_xml
        l_usb.NetworkID = self.get_int_element(l_xml, 'Network')
        l_usb.UnitID = self.get_int_element(l_xml, 'UnitID')
        l_usb.Password = self.get_int_element(l_xml, 'Password')
        l_usb.Product = self.get_int_element(l_xml, 'Product')
        l_usb.Vendor = self.get_int_element(l_xml, 'Vendor')
        l_attrs = self._get_attrs(l_usb)
        for l_attr in l_attrs:
            setattr(p_controller_obj, l_attr, getattr(l_usb, l_attr))

# ## END
