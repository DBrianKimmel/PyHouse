"""
-*- test-case-name: PyHouse.src.Modules.Drivers.test.test_interface -*-

@name:      PyHouse/src/Modules/Driveres/interface.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 21, 2013
@summary:   Schedule events


Controllers, which are attached to the server, communicate with the server via an interface.
There are three different interfaces at this point (2013-10-29):
    Serial
    USB - Includes HID variant
    Ethernet

This module reads and writes the XML for those controllers.

Reading the interface stuffs the interface XML data into the controller object.
"""

# Import system type stuff

# Import PyMh files
from Modules.Drivers.Ethernet.Ethernet_xml import Xml as ethernetXML
from Modules.Drivers.Serial.Serial_xml import Xml as serialXML
from Modules.Drivers.USB.USB_xml import Xml as usbXML
from Modules.Utilities.xml_tools import XmlConfigTools, stuff_new_attrs
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Interface         ')

from Modules.Drivers import VALID_INTERFACES
# from Modules.Drivers import VALID_PROTOCOLS


class Xml(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.
        """
        if p_controller_obj.InterfaceType == 'Ethernet':
            l_interface = ethernetXML.read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'Serial':
            l_interface = serialXML.read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'USB':
            l_interface = usbXML.read_interface_xml(p_controller_xml)
        else:
            LOG.error('Reading a controller driver interface section  For {} - Unknown InterfaceType - {}'.format(p_controller_obj.Name, p_controller_obj.InterfaceType))
            l_interface = None
        stuff_new_attrs(p_controller_obj, l_interface)
        return l_interface  # for testing

    @staticmethod
    def write_interface_xml(p_controller_obj, p_xml):
        if p_controller_obj.InterfaceType == 'Ethernet':
            p_xml = ethernetXML.write_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'Serial':
            p_xml = serialXML.write_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'USB':
            p_xml = usbXML.write_interface_xml(p_xml, p_controller_obj)
        else:
            LOG.error('ERROR - WriteDriverXml - Unknown InterfaceType - {} for {}'.format(p_controller_obj.InterfaceType, p_controller_obj.Name))
        p_xml  # for testing

# ## END DBK
