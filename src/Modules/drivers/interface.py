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
from Modules.Core.data_objects import USBControllerData, EthernetControllerData
from Modules.drivers import Driver_Serial
from Modules.utils import xml_tools
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Interface   ')

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

    def _read_usb_intrface_xml(self, p_controller_obj, p_controller_xml):
        l_usb = USBControllerData()
        l_xml = p_controller_xml
        l_usb.Product = self.get_int_from_xml(l_xml, 'Product')
        l_usb.Vendor = self.get_int_from_xml(l_xml, 'Vendor')
        # Put the serial information into the controller object
        # xml_tools.stuff_new_attrs(p_controller_obj, l_usb)
        return l_usb

    def _write_usb_interface_xml(self, p_xml, p_controller_obj):
        self.put_int_element(p_xml, 'Vendor', p_controller_obj.Vendor)
        self.put_int_element(p_xml, 'Product', p_controller_obj.Product)
        return p_xml


    def _read_ethernet_internet_xml(self, p_controller_obj, p_controller_xml):
        l_ethernet = EthernetControllerData()
        l_xml = p_controller_xml
        l_ethernet.PortNumber = self.get_int_from_xml(l_xml, 'PortNumber')
        l_ethernet.Protocol = self.get_text_from_xml(l_xml, 'Protocol')
        # Put the serial information into the controller object
        # xml_tools.stuff_new_attrs(p_controller_obj, l_ethernet)
        return l_ethernet

    def _write_ethernet_interface_xml(self, p_xml, p_controller_obj):
        self.put_int_element(p_xml, 'PortNumber', p_controller_obj.PortNumber)
        self.put_text_element(p_xml, 'Protocol', p_controller_obj.Protocol)
        return p_xml


    def extract_xml(self, p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.
        """
        l_interface = None
        l_if = (p_controller_obj.InterfaceType)
        if l_if == 'Serial':
            l_interface = Driver_Serial.API()._read_serial_interface_xml(p_controller_obj, p_controller_xml)
        elif l_if == 'USB':
            l_interface = self._read_usb_interface_xml(p_controller_obj, p_controller_xml)
        elif l_if == 'Ethernet':
            l_interface = self._read_ethernet_interface_xml(p_controller_obj, p_controller_xml)
        # Put the serial information into the controller object
        # PrettyPrintAny(l_interface, 'Interface', 120)
        xml_tools.stuff_new_attrs(p_controller_obj, l_interface)

    def write_interface_xml(self, p_controller_obj, p_xml):
        if p_controller_obj.InterfaceType == 'Serial':
            Driver_Serial.API()._write_serial_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'USB':
            self._write_usb_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'Ethernet':
            self._write_ethernet_interface_xml(p_xml, p_controller_obj)

# ## END DBK
