"""
@name:      Modules/House/Entertainment/entertainment_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@note:      Created on Mar 18, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2019-08-18'

# Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseObject


class EntertainmentDeviceInformation(BaseObject):
    """ This is a skeleton entry.
    Other device parameters are placed in here by the specific entertainment device.
    This should be augmented by every device.
    """

    def __init__(self):
        super(EntertainmentDeviceInformation, self).__init__()
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
        self.Host = None  # HostInformation()
        self.Model = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None
        self.Volume = None
        self.ZoneCount = 0
        self.Zones = {}


class EntertainmentServiceInformation(BaseObject):
    """ This is a skeleton entry.
    Other device parameters are placed in here by the specific entertainment device.
    """

    def __init__(self):
        super(EntertainmentServiceInformation, self).__init__()
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


class EntertainmentDeviceControl():
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


class EntertainmentServiceControl():
    """ Used to control a device.
    All defaults are None - Only fill in what you need so inadvertent controls are not done.
    """

    def __init__(self):
        self.Family = None  # The device family we are controlling (onkyo, pioneer, ...)
        self.Model = None
        # self.Device = None  #   The name and Key for the device
        #
        self.Channel = None  # '01'
        self.Direction = None  # F or R  - Forward, Reverse (think Video play)
        self.From = None  # The sending module
        self.HostName = None  # name of computer holding definitions
        self.InputName = None  # 'Game'  # Input Name
        self.Power = None  # 'Off'  # On or Off which is standby
        self.Skip = None  # skip the rest of this song.
        self.Volume = None  # '0'  # 0-100 - Percent
        self.Zone = None  # '1'  # For multi zone output


class EntertainmentDeviceStatus():
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


class EntertainmentServiceStatus():
    """ This is the base class for Service Status messages.
    """

    def __init__(self):
        self.Type = None
        self.Name = None

# ## END DBK