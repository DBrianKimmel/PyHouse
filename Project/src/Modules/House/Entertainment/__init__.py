"""
@name:      Modules/House/Entertainment/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
"""

__updated__ = '2020-01-28'
__version_info__ = (20, 1, 26)
__version__ = '.'.join(map(str, __version_info__))

MODULES = [  # All modules for the Entertainment system must be listed here.  They will be loaded if configured.
    'Firestick',
    'Onkyo',
    'Panasonic',
    'Pandora',
    'Pioneer',
    'Samsung',
    'Sharp',
    'Sony'
    ]


class EntertainmentPluginInformation:
    """
    ==> PyHouse.House.Entertainment.Plugins[PluginName].xxx
    The family is the PluginName - onkyo, pandora, etc. - Always lower case.

    Valid Types:
        Service is a provided service such as Pandora, Netflix, Hulu, etc.
        Device is a Component such as a TV, DVD Player, A/V Receiver, etc.
    """

    def __init__(self):
        self.Name = None  # Name of the plugin
        self.Type = 'Missing Type'  # Service: Component (a device):
        # Devices are indexed by the device number 0..x
        self.DeviceCount = 0
        self.Devices = {}  # EntertainmentDeviceInformation()
        # Services are indexed by the service number 0..x
        self.ServiceCount = 0
        self.Services = {}  # EntertainmentServiceInformation()
        self._Api = None  # The Api pointer for this class of plugin (Pioneer, onkyo, ,,,)
        self._Module = None
        self._OpenSessions = 0


class EntertainmentDeviceInformation:
    """ This is a skeleton entry.
    Other device parameters are placed in here by the specific entertainment device.
    This should be augmented by every device.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self._Endpoint = None
        self._Factory = None  # The factory pointer for this device of an entertainment sub-section
        self._Transport = None
        self._Connector = None
        self._Protocol = None
        self._Queue = None  # A queue to hold commands fro the device.
        self._Yaml = None
        self._isControlling = False
        self._isRunning = False
        #
        self.CommandSet = None  # Command sets change over the years.
        self.Host = None  # HostInformation()  ## See core.data_objects
        self.Model = None
        self.Room = None  # RoomLoc??
        self.Type = None
        self.Volume = None
        self.ZoneCount = 0
        self.Zones = {}


class EntertainmentServiceInformation:
    """ This is a skeleton entry.
    Other device parameters are placed in here by the specific entertainment device.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self._Factory = None  # The factory pointer for this device of an entertainment sub-section
        self._Transport = None
        self._Connector = None

        self.Host = None  # HostInformation()
        self.ConnectionFamily = None  # pioneer, onkyo
        self.ConnectionModel = None  # Model
        self.InputName = None
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
        self.Family = None  # The device family we are controlling (onkyo, pioneer, ...)
        self.Model = None  # the model name
        self.Channel = None  # '01'
        self.Direction = None  # F or R  - Forward, Reverse (think Video play)
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
        self.Family = None  # The device family we are controlling (onkyo, pioneer, ...)
        self.Model = None
        self.Channel = None  # '01'
        self.Direction = None  # F or R  - Forward, Reverse (think Video play)
        self.From = None  # The sending module
        self.HostName = None  # name of computer holding definitions
        self.InputName = None  # 'Game'  # Input Name
        self.Power = None  # 'Off'  # On or Off which is standby
        self.Skip = None  # skip the rest of this song.
        self.Volume = None  # '0'  # 0-100 - Percent
        self.Zone = None  # '1'  # For multi zone output


class EntertainmentDeviceStatus:
    """
    The device family is part of the topic.
    """

    def __init__(self):
        self.Type = None
        self.ControllingNode = None
        self.Connected = False
        self.Family = None
        self.Model = None
        self.Node = None


class EntertainmentServiceStatus:
    """ This is the base class for Service Status messages.
    """

    def __init__(self):
        self.Type = None
        self.Name = None

# ## END DBK
