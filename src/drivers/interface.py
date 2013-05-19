'''
Created on Mar 21, 2013

@author: briank
'''

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools

g_debug = 0

VALID_INTERFACES = ['Serial', 'USB', 'Ethernet']
# SERIAL_ATTRS = {'BaudRate': self.get_text_element,
#                'ByteSize': get_int_element,
#                'DsrDtr': get_bool_element,
#                'Parity': get_text_element,
#                'RtsCts': get_bool_element,
#                'StopBits': get_float_element,
#                'Timeout':get_float_element,
#                'XonXoff': get_bool_element}


class SerialData(object):
    """The additional data needed for serial interfaces.
    """

    def __init__(self):
        self.BaudRate = 9600
        self.ByteSize = 8
        self.DsrDtr = False
        self.Parity = 'N'
        self.RtsCts = False
        self.StopBits = 1.0
        self.Timeout = None
        self.XonXoff = False

    def __repr__(self):
        l_ret = "Serial:: Baud:{0:}, ByteSize:{1:}, Parity:{2:}, StopBits:{3:}; ".format(self.BaudRate, self.ByteSize, self.Parity, self.StopBits)
        return l_ret


class USBData(object):

    def __init__(self):
        self.Product = 0
        self.Vendor = 0

    def __repr__(self):
        l_ret = "USB:: Vendor:{0:#04X}, Product:{1:#04X}; ".format(self.Vendor, self.Product)
        return l_ret


class  EthernetData(object):

    def __init__(self):
        self.PortNumber = 0
        self.Protocol = 'TCP'

    def __repr__(self):
        l_ret = "Ethernet:: port:{0:}, Protocol:{1:#04X}; ".format(self.PortNumber, self.Protocol)
        return l_ret


class ReadWriteConfig(xml_tools.ConfigTools):

    def _shove_attrs(self, p_controller_obj, p_data):
        """Put the information from the data object into the controller object
        """
        l_attrs = filter(lambda aname: not aname.startswith('__'), dir(p_data))
        for l_attr in l_attrs:
            setattr(p_controller_obj, l_attr, getattr(p_data, l_attr))

    def extract_xml(self, p_controller_obj, p_controller_xml):
        l_if = (p_controller_obj.Interface)
        if l_if == 'Serial':
            self._extract_serial_xml(p_controller_obj, p_controller_xml)
        elif l_if == 'USB':
            self._extract_usb_xml(p_controller_obj, p_controller_xml)
        elif l_if == 'Ethernet':
            self._extract_ethernet_xml(p_controller_obj, p_controller_xml)

    def write_xml(self, p_entry, p_controller_obj):
            if p_controller_obj.Interface == 'Serial':
                self._write_serial_xml(p_entry, p_controller_obj)
            elif p_controller_obj.Interface == 'USB':
                self._write_usb_xml(p_entry, p_controller_obj)
            elif p_controller_obj.Interface == 'Ethernet':
                self._write_ethernet_xml(p_entry, p_controller_obj)

    def _extract_serial_xml(self, p_controller_obj, p_controller_xml):
        if g_debug >= 2:
            print "drivers.interface.extract_serial_xml() - Name:{0:}".format(p_controller_obj.Name)
        l_serial = SerialData()
        l_xml = p_controller_xml
        l_serial.BaudRate = self.get_text_element(l_xml, 'BaudRate')
        l_serial.ByteSize = self.get_int_element(l_xml, 'ByteSize')
        l_serial.Parity = self.get_text_element(l_xml, 'Parity')
        l_serial.StopBits = self.get_float_element(l_xml, 'StopBits')
        l_serial.Timeout = self.get_float_element(l_xml, 'Timeout')
        #
        l_serial.DsrDtr = self.get_bool_element(l_xml, 'DsrDtr')
        l_serial.RtsCts = self.get_bool_element(l_xml, 'RtsCts')
        l_serial.XonXoff = self.get_bool_element(l_xml, 'XonXoff')
        # Put the serial information into the controller object
        self._shove_attrs(p_controller_obj, l_serial)

    def _write_serial_xml(self, p_xml, p_controller_obj):
        if g_debug >= 1:
            print "drivers.interface.write_serial_xml()"
        ET.SubElement(p_xml, 'BaudRate').text = str(p_controller_obj.BaudRate)
        ET.SubElement(p_xml, 'ByteSize').text = str(p_controller_obj.ByteSize)
        ET.SubElement(p_xml, 'Parity').text = str(p_controller_obj.Parity)
        ET.SubElement(p_xml, 'StopBits').text = str(p_controller_obj.StopBits)
        ET.SubElement(p_xml, 'Timeout').text = str(p_controller_obj.Timeout)
        if g_debug >= 2:
            print "drivers.interface.write_serial_xml() - Wrote serial controller"

    def _extract_usb_xml(self, p_controller_obj, p_controller_xml):
        if g_debug >= 2:
            print "drivers.interface.extract_usb_xml() - Name:{0:}".format(p_controller_obj.Name)
        l_usb = USBData()
        l_xml = p_controller_xml
        l_usb.Product = self.get_int_element(l_xml, 'Product')
        l_usb.Vendor = self.get_int_element(l_xml, 'Vendor')
        self._shove_attrs(p_controller_obj, l_usb)

    def _write_usb_xml(self, p_xml, p_controller_obj):
        if g_debug >= 1:
            print "drivers.interface.write_usb_xml()"
        ET.SubElement(p_xml, 'Vendor').text = str(p_controller_obj.Vendor)
        ET.SubElement(p_xml, 'Product').text = str(p_controller_obj.Product)
        if g_debug >= 2:
            print "drivers.interface.write_serial_xml() - Wrote usb controller"

    def _extract_ethernet_xml(self, p_controller_obj, p_controller_xml):
        if g_debug >= 2:
            print "drivers.interface.extract_ethernet_xml() - Name:{0:}".format(p_controller_obj.Name)
        l_ethernet = EthernetData()
        l_xml = p_controller_xml
        l_ethernet.PortNumber = self.get_int_element(l_xml, 'PortNumber')
        l_ethernet.Protocol = self.get_int_element(l_xml, 'Protocol')
        self._shove_attrs(p_controller_obj, l_ethernet)

    def _write_ethernet_xml(self, p_xml, p_controller_obj):
        if g_debug >= 1:
            print "drivers.interface.write_usb_xml()"
        ET.SubElement(p_xml, 'PortNumber').text = str(p_controller_obj.PortNumber)
        ET.SubElement(p_xml, 'Protocol').text = str(p_controller_obj.Protocol)
        if g_debug >= 2:
            print "drivers.interface.write_ethernet_xml() - Wrote ethernet controller"

# ## END DBK
