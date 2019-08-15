"""
@name:      Modules/Core/Drivers/interface.py
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

__updated__ = '2019-08-15'

# Import system type stuff

# Import PyMh files
from Modules.Core.Drivers.Ethernet.Ethernet_xml import XML as ethernetXML
from Modules.Core.Drivers.Null.Null_xml import XML as nullXML
from Modules.Core.Drivers.Serial.Serial_driver import Config as serialConfig
from Modules.Core.Drivers.USB.USB_xml import XML as usbXML
from Modules.Core.Utilities.xml_tools import stuff_new_attrs

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Interface      ')


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
        self.Name = None
        self.Node = None
        self.Status = None  # Open, Died, Closed


class Config:
    """ This abstracts the interface information.
    Used so far for lighting controllers.
    Allows for yaml config files to have a section for "Interface:" without defining the contents of that section;
     getting that information is the job of the particular driver XXX

    Interface:
       Type: XXX
       ...
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
            serialConfig().load_serial_config(p_config, l_obj)
        return l_obj

# ## END DBK
