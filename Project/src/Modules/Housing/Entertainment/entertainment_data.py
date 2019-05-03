"""
-*- test-case-name: PyHouse/src/Modules/Housing/Entertainment/entertainment_data.py -*-

@name:      PyHouse/src/Modules/Housing/Entertainment/entertainment_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@note:      Created on Mar 18, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2019-05-02'

# Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseObject


class EntertainmentData:
    """ This is the PyHouse.House.Entertainment node of the master object.
    It is a dynamic structure for the various entertainment devices in a house.

    Top level

    ==> PyHouse.House.Entertainment.xxx as in the def below.
    """

    def __init__(self):
        self.Active = False
        self.PluginCount = 0
        self.Plugins = {}  # EntertainmentPluginData()


class EntertainmentPluginData:
    """ This is filled in for every xxxSection under the EntertainmentSection of the XML file

    ==> PyHouse.House.Entertainment.Plugins[name].xxx

    Valid Types:
        Service is a provided service such as Pandora, Netflix, Hulu, etc.
        Device is a Component such as a TV, DVD Player, Receiver, etc.
    """

    def __init__(self):
        self.Active = False
        self.DeviceCount = 0
        self.Devices = {}  # EntertainmentDeviceData()
        self.ServiceCount = 0
        self.Services = {}  # EntertainmentServiceData()
        self.Name = None
        self.Type = 'Missing Type'  # Service: Component (a device):
        #
        self._API = None  # The API pointer for this class of plugin (Pioneer, onkyo, ,,,)
        self._Module = None
        self._OpenSessions = 0


class EntertainmentDeviceData(BaseObject):
    """ This is a skeleton entry.
    Other device parameters are placed in here by the specific entertainment device.
    """

    def __init__(self):
        super(EntertainmentDeviceData, self).__init__()
        self._Endpoint = None
        self._Factory = None  # The factory pointer for this device of an entertainment sub-section
        self._Transport = None
        self._Connector = None
        self._Protocol = None
        #
        self.CommandSet = None  # Command sets change over the years.
        self.IPv4 = None  # IPv4 if No  FQDN or IPv6
        self.IPv6 = None  # IPv6 addr of the device if no FQDN
        self.Host = None  # FQDN of the device
        self.Model = None
        self.Model = None
        self.Port = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None
        self.Volume = None
        self._isConnected = False
        self._isRunning = False


class EntertainmentServiceData(BaseObject):
    """ This is a skeleton entry.
    Other device parameters are placed in here by the specific entertainment device.
    """

    def __init__(self):
        super(EntertainmentServiceData, self).__init__()
        self.ServiceCount = 0
        self._Factory = None  # The factory pointer for this device of an entertainment sub-section
        self._Transport = None
        self._Connector = None

        self.Host = '1.2.3.4'
        self.ConnectionFamily = None  # pioneer, onkyo
        self.ConnectionName = None  # Device Name
        self.InputName = None
        self.InputCode = None
        self.Type = 'service'
        self.Volume = 0  # Default volume
        self.MaxPlayTime = 12 * 60 * 60  # Seconds
        self.MaxConnections = 1
        self._isRunning = False


class EntertainmentDeviceControl:
    """ Used to control a device.
    All defaults are None - Only fill in what you need so inadvertent controls are not done.
    """

    def __init__(self):
        self.Channel = None  # '01'
        self.Device = None  #   The name and Key for the device
        self.Direction = None  # F or R  - Forward, Reverse (think Video play)
        self.Family = None  # The device family we are controlling (onkyo, pioneer, ...)
        self.From = None  # The sending module
        self.HostName = None  # name of computer holding definitions
        self.InputName = None  # '01'  # Input ID
        self.Power = None  # 'Off'  # On or Off which is standby
        self.Skip = None  # skip tracks, skip ahead
        self.Volume = None  # '0'  # 0-100 - Percent
        self.Zone = None  # '1' or '2'  # For multi zone output


class EntertainmentServiceControl:
    """ Used to control a device.
    All defaults are None - Only fill in what you need so inadvertent controls are not done.
    """

    def __init__(self):
        self.Channel = None  # '01'
        self.Device = None  #   The name and Key for the device
        self.Direction = None  # F or R  - Forward, Reverse (think Video play)
        self.Family = None  # The device family we are controlling (onkyo, pioneer, ...)
        self.From = None  # The sending module
        self.HostName = None  # name of computer holding definitions
        self.InputName = None  # '01'  # Input ID
        self.Power = None  # 'Off'  # On or Off which is standby
        self.Skip = None  # skip tracks, skip ahead
        self.Volume = None  # '0'  # 0-100 - Percent
        self.Zone = None  # '1'  # For multi zone output

# ## END DBK
