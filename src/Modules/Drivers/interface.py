"""
-*- test-case-name: PyHouse.src.Modules.Drivers.test.test_interface -*-

@name: PyHouse/src/Modules/Driveres/interface.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 21, 2013
@summary: Schedule events


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
from Modules.Drivers.Ethernet import Ethernet_xml
from Modules.Drivers.Serial import Serial_xml
from Modules.Drivers.USB import USB_xml
from Modules.Utilities.xml_tools import XmlConfigTools, stuff_new_attrs
from Modules.Computer import logging_pyh as Logger

g_debug = 0
LOG = Logger.getLogger('PyHouse.Interface         ')

from Modules.Drivers import VALID_INTERFACES
# from Modules.Drivers import VALID_PROTOCOLS


class Utility(object):
    """
    """

    def findXml(self, p_obj):
        try:
            l_interfaceType = p_obj.InterfaceType
        except AttributeError as e_err:
            LOG.error('Object has no InterfaceType {0:} - {1:}'.format(p_obj, e_err))
            return None
        for l_interface in VALID_INTERFACES:
            if l_interface == l_interfaceType:
                l_ret = l_interface.xml
                return l_ret
        return None


class ReadWriteConfigXml(XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def read_interface_xml(self, p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.
        """
        if p_controller_obj.InterfaceType == 'Ethernet':
            l_interface = Ethernet_xml.ReadWriteConfigXml().read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'Serial':
            l_interface = Serial_xml.ReadWriteConfigXml().read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'USB':
            l_interface = USB_xml.ReadWriteConfigXml().read_interface_xml(p_controller_xml)
        else:
            LOG.error('For {} - Unknown InterfaceType - {}'.format(p_controller_obj.Name, p_controller_obj.InterfaceType))
            l_interface = None
        # Put the serial information into the controller object
        stuff_new_attrs(p_controller_obj, l_interface)
        return l_interface  # for testing

    def write_interface_xml(self, p_controller_obj, p_xml):
        if p_controller_obj.InterfaceType == 'Ethernet':
            Ethernet_xml.ReadWriteConfigXml().write_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'Serial':
            Serial_xml.ReadWriteConfigXml().write_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'USB':
            USB_xml.ReadWriteConfigXml().write_interface_xml(p_xml, p_controller_obj)
        else:
            LOG.error('ERROR - Write - Unknown InterfaceType - {0:}'.format(p_controller_obj.InterfaceType))

# ## END DBK
