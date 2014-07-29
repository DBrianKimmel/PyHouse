"""
-*- test-case-name: PyHouse.src.Modules.drivers.test.test_interface -*-

@name: PyHouse/src/Modules/driveres/interface.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
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
from Modules.drivers.Ethernet import ethernet_xml
from Modules.drivers.Serial import serial_xml
from Modules.drivers.USB import usb_xml
from Modules.utils import xml_tools
from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Interface   ')

from Modules.drivers import VALID_INTERFACES
from Modules.drivers import VALID_PROTOCOLS


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def read_interface_xml(self, p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.
        """
        if p_controller_obj.InterfaceType == 'Ethernet':
            l_interface = ethernet_xml.ReadWriteConfigXml().read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'Serial':
            l_interface = serial_xml.ReadWriteConfigXml().read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'USB':
            l_interface = usb_xml.ReadWriteConfigXml().read_interface_xml(p_controller_xml)
        else:
            LOG.error('ERROR - Read - Unknown InterfaceType - {0:}'.format(p_controller_obj.InterfaceType))
            l_interface = None
        # Put the serial information into the controller object
        xml_tools.stuff_new_attrs(p_controller_obj, l_interface)

    def write_interface_xml(self, p_controller_obj, p_xml):
        if p_controller_obj.InterfaceType == 'Ethernet':
            ethernet_xml.ReadWriteConfigXml().write_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'Serial':
            serial_xml.ReadWriteConfigXml().write_interface_xml(p_xml, p_controller_obj)
        elif p_controller_obj.InterfaceType == 'USB':
            usb_xml.ReadWriteConfigXml().write_interface_xml(p_xml, p_controller_obj)
        else:
            LOG.error('ERROR - Write - Unknown InterfaceType - {0:}'.format(p_controller_obj.InterfaceType))

# ## END DBK
