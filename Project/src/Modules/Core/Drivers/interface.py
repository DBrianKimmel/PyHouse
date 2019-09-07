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

__updated__ = '2019-09-07'
__version_info__ = (19, 9, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Drivers.Serial import Serial_driver
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Interface      ')


class DriverInterfaceInformation:
    """
    ...Interface.xxxx
    """

    def __init__(self):
        self.Type = None  # Null, Ethernet, Serial, USB, HTML, Websockets,  ...
        self.Host = None
        self.Port = None
        self._DriverApi = None  # Serial_driver.API()
        # Type specific information follows


def _get_interface_type(p_device_obj):
    return p_device_obj.Interface.Type.lower()


def get_device_driver_API(p_pyhouse_obj, p_controller_obj):
    """
    Based on the InterfaceType of the controller, load the appropriate driver and get its API().
    @return: a pointer to the device driver or None
    """
    # LOG.debug(PrettyFormatAny.form(p_controller_obj, 'Controller'))
    # LOG.debug(PrettyFormatAny.form(p_controller_obj.Interface, 'Interface'))
    l_dev_name = p_controller_obj.Interface
    l_type = _get_interface_type(p_controller_obj)
    if l_type == 'serial':
        l_driver = Serial_driver.API(p_pyhouse_obj)

    elif l_type == 'ethernet':
        from Modules.Core.Drivers.Ethernet import Ethernet_driver
        l_driver = Ethernet_driver.API(p_pyhouse_obj)

    elif l_type == 'usb':
        from Modules.Core.Drivers.USB import USB_driver
        l_driver = USB_driver.API(p_pyhouse_obj)

    else:
        LOG.error('No driver for device: {} with interface type: {}'.format(
                l_dev_name, p_controller_obj.Interface.Type))
        from Modules.Core.Drivers.Null import Null_driver
        l_driver = Null_driver.API(p_pyhouse_obj)

    p_controller_obj.Interface._DriverApi = l_driver
    l_driver.Start(p_controller_obj)
    return l_driver


class Config:
    """ This abstracts the interface information.
    Used so far for lighting controllers.
    Allows for yaml config files to have a section for "Interface:" without defining the contents of that section;
     getting that information is the job of the particular driver XXX

    Interface:
       Type: Serial
       Host: pi-01-pp
       Port: /dev/ttyUSB0
       <Type specific information>
       ...
    """

    def load_interface(self, p_config):
        """
        """
        l_obj = DriverInterfaceInformation()
        l_required = ['Type', 'Host', 'Port']
        for l_key, l_value in p_config.items():
            # LOG.debug('Interface {}: = {}'.format(l_key, l_value))
            setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Controller Yaml is missing an entry for "{}"'.format(l_key))
        # Append the type specific data to the Object
        if l_obj.Type == 'Serial':
            Serial_driver.Config().load_serial_config(p_config, l_obj)
        return l_obj

# ## END DBK
