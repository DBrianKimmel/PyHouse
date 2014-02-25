"""
Created on Mar 21, 2013

@author: briank

Controllers, which are attached to the server, communicate with the server via an interface.
There are three different interfaces at this point (2013-10-29).
    Serial
    USB - Includes HID variant
    Ethernet
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools
# from src.utils.tools import PrintObject

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
        from src.lights import lighting_controllers
        lighting_controllers.ControllerData().__init__()
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
        # PrintObject('interface.reprJSON(1) ', self)
        # print "interface.SerialData.reprJSON(1)"
        from src.lights import lighting_controllers
        l_ret = lighting_controllers.ControllerData().reprJSON()
        l_ret.update(dict(
            InterfaceType = self.InterfaceType,
            BaudRate = self.BaudRate,
            ByteSize = self.ByteSize,
            DsrDtr = self.DsrDtr,
            Parity = self.Parity,
            RtsCts = self.RtsCts,
            StopBits = self.StopBits,
            Timeout = self.Timeout,
            XonXoff = self.XonXoff
        ))
        # print "interface.SerialData.reprJSON(2) {0:}".format(l_ret)
        return l_ret


class USBData(object):

    def __init__(self):
        self.InterfaceType = 'USB'
        self.Product = 0
        self.Vendor = 0

    def reprJSON(self):
        # print "interface.USBData.reprJSON(1)"
        l_ret = dict(
            InterfaceType = self.InterfaceType,
            Product = self.Product,
            Vendor = self.Vendor
        )
        # print "interface.USBData.reprJSON(2) {0:}".format(l_ret)
        return l_ret


class  EthernetData(object):

    def __init__(self):
        self.InterfaceType = 'Ethernet'
        self.PortNumber = 0
        self.Protocol = 'TCP'

    def reprJSON(self):
        # print "interface.EthernetData.reprJSON(1)"
        l_ret = dict(
            InterfaceType = self.InterfaceType,
            PortNumber = self.PortNumber,
            Protocol = self.Protocol
        )
        # print "interface.EthernetData.reprJSON(2) {0:}".format(l_ret)
        return l_ret


class ReadWriteConfig(xml_tools.ConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def extract_xml(self, p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.
        """
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
        xml_tools.stuff_new_attrs(p_controller_obj, l_serial)

    def _write_serial_xml(self, p_xml, p_controller_obj):
        try:
            ET.SubElement(p_xml, 'BaudRate').text = str(p_controller_obj.BaudRate)
        except AttributeError:
            ET.SubElement(p_xml, 'BaudRate').text = '19200'
        try:
            ET.SubElement(p_xml, 'ByteSize').text = str(p_controller_obj.ByteSize)
        except AttributeError:
            ET.SubElement(p_xml, 'ByteSize').text = '8'
        try:
            ET.SubElement(p_xml, 'Parity').text = str(p_controller_obj.Parity)
        except AttributeError:
            ET.SubElement(p_xml, 'Parity').text = 'N'
        try:
            ET.SubElement(p_xml, 'StopBits').text = str(p_controller_obj.StopBits)
        except AttributeError:
            ET.SubElement(p_xml, 'StopBits').text = '1.0'
        try:
            ET.SubElement(p_xml, 'Timeout').text = str(p_controller_obj.Timeout)
        except AttributeError:
            ET.SubElement(p_xml, 'Timeout').text = '1.0'
        try:
            ET.SubElement(p_xml, 'DsrDtr').text = str(p_controller_obj.DsrDtr)
        except AttributeError:
            ET.SubElement(p_xml, 'DsrDtr').text = False
        try:
            ET.SubElement(p_xml, 'RtsCts').text = str(p_controller_obj.RtsCts)
        except AttributeError:
            ET.SubElement(p_xml, 'RtsCts').text = False
        try:
            ET.SubElement(p_xml, 'XonXoff').text = str(p_controller_obj.XonXoff)
        except AttributeError:
            ET.SubElement(p_xml, 'XonXoff').text = False

    def _extract_usb_xml(self, p_controller_obj, p_controller_xml):
        l_usb = USBData()
        l_xml = p_controller_xml
        l_usb.Product = self.get_int_from_xml(l_xml, 'Product')
        l_usb.Vendor = self.get_int_from_xml(l_xml, 'Vendor')
        # Put the serial information into the controller object
        xml_tools.stuff_new_attrs(p_controller_obj, l_usb)

    def _write_usb_xml(self, p_xml, p_controller_obj):
        try:
            ET.SubElement(p_xml, 'Vendor').text = str(p_controller_obj.Vendor)
        except AttributeError:
            ET.SubElement(p_xml, 'Vendor').text = 0
        try:
            ET.SubElement(p_xml, 'Product').text = str(p_controller_obj.Product)
        except AttributeError:
            ET.SubElement(p_xml, 'Product').text = 0

    def _extract_ethernet_xml(self, p_controller_obj, p_controller_xml):
        l_ethernet = EthernetData()
        l_xml = p_controller_xml
        l_ethernet.PortNumber = self.get_int_from_xml(l_xml, 'PortNumber')
        l_ethernet.Protocol = self.get_int_from_xml(l_xml, 'Protocol')
        # Put the serial information into the controller object
        xml_tools.stuff_new_attrs(p_controller_obj, l_ethernet)

    def _write_ethernet_xml(self, p_xml, p_controller_obj):
        try:
            ET.SubElement(p_xml, 'PortNumber').text = str(p_controller_obj.PortNumber)
        except AttributeError:
            ET.SubElement(p_xml, 'PortNumber').text = 0
        try:
            ET.SubElement(p_xml, 'Protocol').text = str(p_controller_obj.Protocol)
        except AttributeError:
            ET.SubElement(p_xml, 'Protocol').text = 'TCP'

# ## END DBK
