"""
@name:      Modules/Drivers/interface.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 21, 2013
@summary:


Controllers, which are attached to the server, communicate with the server via an interface.
There are several different interfaces at this point (2013-10-29):
    Serial
    USB - Includes HID variant
    Ethernet (Tcp)
    Null

This module reads and writes the Config for those controllers.
"""

__updated__ = '2019-07-23'

# Import system type stuff

# Import PyMh files
from Modules.Drivers.Ethernet.Ethernet_xml import XML as ethernetXML
from Modules.Drivers.Null.Null_xml import XML as nullXML
from Modules.Drivers.Serial.Serial_config import Config as serialConfig
from Modules.Drivers.USB.USB_xml import XML as usbXML
from Modules.Core.Utilities.xml_tools import stuff_new_attrs

from Modules.Computer import logging_pyh as Logging
LOG = Logging.getLogger('PyHouse.Interface      ')


class DriverInterfaceInformation():
    """
    ...Interface.xxxx
    """

    def __init__(self):
        self.Name = None
        self.Type = None  # Null, Ethernet, Serial, USB, HTML, Websockets,  ...


class DriverStatus():
    """
    """

    def __init__(self):
        self.Node = None
        self.Status = None  # Open, Died, Closed


class Config:
    """
    """

    def load_interface(self, p_config):
        """
        """
        l_obj = DriverInterfaceInformation()
        l_required = ['Type']
        for l_key, l_value in p_config.items():
            # print('Interface Key: {}; Value: {}'.format(l_key, l_value))
            setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Controller Yaml is missing an entry for "{}"'.format(l_key))
        if l_obj.Type == 'Serial':
            serialConfig().load_config(p_config, l_obj)
        return l_obj


class Xml:
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.

        This is basically a dispatcher.

        @param p_controller_obj: This is the object we are going to stuff the interface info into.
        """
        if p_controller_obj.InterfaceType == 'Ethernet':
            l_interface = ethernetXML.read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'Serial':
            l_interface = serialXML.read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'USB':
            l_interface = usbXML.read_interface_xml(p_controller_xml)
        elif p_controller_obj.InterfaceType == 'Null':
            l_interface = nullXML.read_interface_xml(p_controller_xml)
        else:
            LOG.error('Reading a controller driver interface section  For {} - Unknown InterfaceType - {}'
                      .format(p_controller_obj.Name, p_controller_obj.InterfaceType))
            l_interface = None
        stuff_new_attrs(p_controller_obj, l_interface)
        return l_interface  # for testing

    @staticmethod
    def write_interface_xml(p_controller_obj):
        if p_controller_obj.InterfaceType == 'Ethernet':
            l_xml = ethernetXML.write_interface_xml(p_controller_obj)
        elif p_controller_obj.InterfaceType == 'Serial':
            l_xml = serialXML.write_interface_xml(p_controller_obj)
        elif p_controller_obj.InterfaceType == 'USB':
            l_xml = usbXML.write_interface_xml(p_controller_obj)
        elif p_controller_obj.InterfaceType == 'Null':
            l_xml = nullXML.write_interface_xml(p_controller_obj)
        else:
            LOG.error('ERROR - WriteDriverXml - Unknown InterfaceType - {} for {}'.format(p_controller_obj.InterfaceType, p_controller_obj.Name))
        return l_xml

# ## END DBK
