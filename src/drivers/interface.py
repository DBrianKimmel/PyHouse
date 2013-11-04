"""
Created on Mar 21, 2013

@author: briank

Controllers, which are attached to the server, communicate with the server via an interface.
There are three different interfaces at this point (2013-10-29).
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools

g_debug = 0

"""Note:
There must be a 'Data' class for each valid interface.
The class name must be the interface name + 'Data'.
Be careful since the name will be generated and is case sensitive.
"""
from src.drivers import VALID_INTERFACES
from src.drivers import VALID_PROTOCOLS


class SerialData(object):
    """The additional data needed for serial interfaces.
    """

    def __init__(self):
        self.InterfaceType = 'Serial'
        self.BaudRate = 9600
        self.ByteSize = 8
        self.DsrDtr = False
        self.Parity = 'N'
        self.RtsCts = False
        self.StopBits = 1.0
        self.Timeout = None
        self.XonXoff = False

    def reprJSON(self):
        """interface().
        """
        print "interface.SerialData.reprJSON(1)"
        l_ret = dict(
            InterfaceType = self.InterfaceType,
            BaudRate = self.BaudRate,
            ByteSize = self.ByteSize,
            DsrDtr = self.DsrDtr,
            Parity = self.Parity,
            RtsCts = self.RtsCts,
            StopBits = self.StopBits,
            Timeout = self.Timeout,
            XonXoff = self.XonXoff
        )
        print "interface.SerialData.reprJSON(2) {0:}".format(l_ret)
        return l_ret


class USBData(object):

    def __init__(self):
        self.Product = 0
        self.Vendor = 0

    def XX__str__(self):
        l_ret = "USB:: Vendor:{0:#04X}, Product:{1:#04X}; ".format(self.Vendor, self.Product)
        return l_ret

    def reprJSON(self):
        print "interface.USBData.reprJSON(1)"
        l_ret = dict(
            Product = self.Product, Vendor = self.Vendor
        )
        print "interface.USBData.reprJSON(2) {0:}".format(l_ret)
        return l_ret


class  EthernetData(object):

    def __init__(self):
        self.PortNumber = 0
        self.Protocol = 'TCP'

    def XX__str__(self):
        l_ret = "Ethernet:: port:{0:}, Protocol:{1:#04X}; ".format(self.PortNumber, self.Protocol)
        return l_ret

    def reprJSON(self):
        print "interface.EthernetData.reprJSON(1)"
        l_ret = dict(
            PortNumber = self.PortNumber, Protocol = self.Protocol
        )
        print "interface.EthernetData.reprJSON(2) {0:}".format(l_ret)
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
        l_serial.BaudRate = self.get_text_from_xml(l_xml, 'BaudRate')
        l_serial.ByteSize = self.get_int_from_xml(l_xml, 'ByteSize')
        l_serial.Parity = self.get_text_from_xml(l_xml, 'Parity')
        l_serial.StopBits = self.get_float_from_xml(l_xml, 'StopBits')
        l_serial.Timeout = self.get_float_from_xml(l_xml, 'Timeout')
        l_serial.DsrDtr = self.get_bool_from_xml(l_xml, 'DsrDtr')
        l_serial.RtsCts = self.get_bool_from_xml(l_xml, 'RtsCts')
        l_serial.XonXoff = self.get_bool_from_xml(l_xml, 'XonXoff')
        # Put the serial information into the controller object
        self._shove_attrs(p_controller_obj, l_serial)

    def _write_serial_xml(self, p_xml, p_controller_obj):
        try:
            ET.SubElement(p_xml, 'BaudRate').text = str(p_controller_obj.BaudRate)
            ET.SubElement(p_xml, 'ByteSize').text = str(p_controller_obj.ByteSize)
            ET.SubElement(p_xml, 'Parity').text = str(p_controller_obj.Parity)
            ET.SubElement(p_xml, 'StopBits').text = str(p_controller_obj.StopBits)
            ET.SubElement(p_xml, 'Timeout').text = str(p_controller_obj.Timeout)
        except AttributeError:
            ET.SubElement(p_xml, 'BaudRate').text = '19200'
            ET.SubElement(p_xml, 'ByteSize').text = '8'
            ET.SubElement(p_xml, 'Parity').text = 'N'
            ET.SubElement(p_xml, 'StopBits').text = '1.0'
            ET.SubElement(p_xml, 'Timeout').text = '1.0'

    def _extract_usb_xml(self, p_controller_obj, p_controller_xml):
        if g_debug >= 2:
            print "drivers.interface.extract_usb_xml() - Name:{0:}".format(p_controller_obj.Name)
        l_usb = USBData()
        l_xml = p_controller_xml
        l_usb.Product = self.get_int_from_xml(l_xml, 'Product')
        l_usb.Vendor = self.get_int_from_xml(l_xml, 'Vendor')
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
        l_ethernet.PortNumber = self.get_int_from_xml(l_xml, 'PortNumber')
        l_ethernet.Protocol = self.get_int_from_xml(l_xml, 'Protocol')
        self._shove_attrs(p_controller_obj, l_ethernet)

    def _write_ethernet_xml(self, p_xml, p_controller_obj):
        if g_debug >= 1:
            print "drivers.interface.write_usb_xml()"
        ET.SubElement(p_xml, 'PortNumber').text = str(p_controller_obj.PortNumber)
        ET.SubElement(p_xml, 'Protocol').text = str(p_controller_obj.Protocol)
        if g_debug >= 2:
            print "drivers.interface.write_ethernet_xml() - Wrote ethernet controller"

# ## END DBK
