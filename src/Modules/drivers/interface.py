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
from Modules.Core.data_objects import SerialControllerData, USBControllerData, EthernetControllerData
from Modules.utils import xml_tools
from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Controller  ')

"""Note:
There must be a 'Data' class for each valid interface.
The class name must be the interface name + 'Data'.
Be careful since the name will be generated and is case sensitive.
"""
from Modules.drivers import VALID_INTERFACES
from Modules.drivers import VALID_PROTOCOLS


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def extract_xml(self, p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.
        """
        l_if = (p_controller_obj.InterfaceType)
        if l_if == 'Serial':
            self._extract_serial_xml(p_controller_obj, p_controller_xml)
        elif l_if == 'USB':
            self._extract_usb_xml(p_controller_obj, p_controller_xml)
        elif l_if == 'Ethernet':
            self._extract_ethernet_xml(p_controller_obj, p_controller_xml)

    def write_interface_xml(self, p_controller_obj, p_xml):
            if p_controller_obj.InterfaceType == 'Serial':
                self._write_serial_xml(p_xml, p_controller_obj)
            elif p_controller_obj.InterfaceType == 'USB':
                self._write_usb_xml(p_xml, p_controller_obj)
            elif p_controller_obj.InterfaceType == 'Ethernet':
                self._write_ethernet_xml(p_xml, p_controller_obj)

    def _extract_serial_xml(self, p_controller_obj, p_controller_xml):
        l_serial = SerialControllerData()
        l_xml = p_controller_xml
        l_serial.BaudRate = self.get_int_from_xml(l_xml, 'BaudRate')
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
        l_usb = USBControllerData()
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
        l_ethernet = EthernetControllerData()
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
