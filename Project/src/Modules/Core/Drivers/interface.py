"""
@name:      Modules/Core/Drivers/interface.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 21, 2013
@summary:

There is no need to pre-load any interfaces.
The necessary interfaces are discovered when loading the "devices" that are controlled by PyHouse.

Controllers, which are attached to the server, communicate with the server via an interface.
"""

__updated__ = '2019-12-23'
__version_info__ = (19, 11, 2)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
from typing import Optional

# Import PyMh files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Drivers.Serial import Serial_driver

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Interface      ')


class DriverInterfaceInformation:
    """
    ...Interface.xxxx
    """

    def __init__(self) -> None:
        self.Type: Optional[str] = None  # Null, Ethernet, Serial, USB, HTML, Websockets,  ...
        self.Host: Optional[str] = None
        self.Port: Optional[int] = None
        self._DriverApi = None  # Serial_driver.Api()
        self._isLocal = False
        # Type specific information follows


def _get_interface_type(p_device_obj):
    return p_device_obj.Interface.Type.lower()


def get_device_driver_Api(p_pyhouse_obj, p_interface_obj):
    """
    Based on the InterfaceType of the controller, load the appropriate driver and get its Api().
    @return: a pointer to the device driver or None
    """
    # LOG.debug(PrettyFormatAny.form(p_interface_obj, 'DriverInterface'))
    l_type = p_interface_obj.Type.lower()
    if l_type == 'serial':
        # LOG.debug('Getting Serial Interface')
        l_driver = Serial_driver.Api(p_pyhouse_obj)

    elif l_type == 'ethernet':
        from Modules.Core.Drivers.Ethernet import Ethernet_driver
        l_driver = Ethernet_driver.Api(p_pyhouse_obj)

    elif l_type == 'usb':
        from Modules.Core.Drivers.USB import USB_driver
        l_driver = USB_driver.Api(p_pyhouse_obj)

    else:
        LOG.error('No driver for device: {} with interface type: {}'.format(
                l_type, p_interface_obj.Type))
        from Modules.Core.Drivers.Null import Null_driver
        l_driver = Null_driver.Api(p_pyhouse_obj)

    p_interface_obj._DriverApi = l_driver
    # l_driver.Start(p_controller_obj)
    return l_driver


class LocalConfig:
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

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

# ## END DBK
