"""
-*- test-case-name: PyHouse/src/Modules/Housing/Entertainment/entertainment_data.py -*-

@name:      PyHouse/src/Modules/Housing/Entertainment/entertainment_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Mar 18, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2018-08-25'

# Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseObject


class EntertainmentData:
    """ This is the PyHouse.House.Entertainment node of the master object.
    It is a dynamic structure for the various entertainment devices in a house.

    ==> PyHouse.House.Entertainment.xxx as in the def below.
    """

    def __init__(self):
        self.Active = False
        self.Count = 0
        self.Plugins = {}  # EntertainmentPluginData()


class EntertainmentPluginData:
    """ This is filled in for every xxxSection under the EntertainmentSection of the XML file

    ==> PyHouse.House.Entertainment.Plugins[name].xxx

    Valid Types:
        Service is a provided service such as Pandora, Netflix, Hulu, etc.
        Component is a device such as a TV, DVD Player, Receiver, etc.
    """

    def __init__(self):
        self.Active = False
        self.API = None  # The API pointer for this class of plugin
        self.Count = 0
        self.Devices = {}  # EntertainmentDeviceData()
        self.Module = None
        self.Name = None
        self.Type = 'Missing Type'  # Service: Component


class EntertainmentDeviceData(BaseObject):
    """ This is a skeleton entry.
    Other device parameters are placed in here by the specific entertainment device.
    """

    def __init__(self):
        super(EntertainmentDeviceData, self).__init__()
        self.DeviceCount = 0
        self._Factory = None  # The factory pointer for this device of an entertainment sub-section
        self._Transport = None
        self._Connector = None


class EntertainmentDeviceControl:
    """ Used to control a device.
    All defaults are None - Only fill in what you need so inadvertent controls are not done.
    """

    def __init__(self):
        self.Channel = None  # '01'
        self.Device = None  #   The name and Key for the device
        self.Direction = None  # F or R  - Foreward, Reverse (think Video play)
        self.Input = None  # '01'  # Input ID
        self.Power = None  # 'Off'  # On or Off which is standby
        self.Volume = None  # '0'  # 0-100 - Percent
        self.Zone = None  # '1'  # For multi zone output

# ## END DBK
