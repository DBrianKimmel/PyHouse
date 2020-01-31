"""
@name:       Modules/House/Entertainment/Pandora/__init__.py
@author:     D. Brian Kimmel
@contact:    D.BrianKimmel@gmail.com
@copyright:  (c)2014-2020 by D. Brian Kimmel
@note:       Created on Feb 27, 2014
@license:    MIT License
"""

__updated__ = '2020-01-30'
__version_info__ = (20, 1, 28)
__version__ = '.'.join(map(str, __version_info__))

#  Import PyMh files and modules.
from Modules.House.Entertainment import \
    EntertainmentPluginInformation, \
    EntertainmentServiceInformation, \
    EntertainmentServiceControl, \
    EntertainmentDeviceControl, \
    EntertainmentServiceStatus

MOD_NAME = 'Pandora'


class PandoraPluginInformation(EntertainmentPluginInformation):
    """
    """

    def __init__(self):
        super(PandoraPluginInformation, self).__init__()
        self._OpenSessions = 0


class PandoraServiceInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.Connection = None  # PandoraServiceConnectionInformation()
        self.Host = None  # HostInformation()
        self.Access = None  # AccessInformation()
        #
        self._Factory = None  # The factory pointer for this device of an entertainment sub-section
        self._Transport = None
        self._Connector = None


class PandoraDeviceConnectionInformation:
    """ This is how the pandora computer connects to the AV system

    Only one connection is allowed
    """

    def __init__(self):
        self.Type = None  # Wire, Bluetooth, Optical
        self.Family = None  # The family of the AV device - Panasonic, Pioneer, Onkyo, etc
        self.Model = None  # The model of the AV device - FamilyModel must be defined in a Yaml config file
        self.Input = None  # The name if the input - Must be in the device config file


class PandoraServiceStatus(EntertainmentServiceStatus):

    def __init__(self):
        super(PandoraServiceStatus, self).__init__()
        self.Album = ''
        self.Artist = ''
        self.Song = ''
        self.Station = ''
        self.Status = 'Idle'  # Device if service is in use.
        #
        self.DateTimePlayed = None  # Time the latest song started.
        self.DateTimeStarted = None  # Time service connected to pandora.com
        self.Error = None  # If some error occurred
        self.From = None  # This host id to identify the computer node connecting to pandora.
        self.inUseDevice = None
        self.Likability = None
        self.TimeTotal = None
        self.TimeLeft = None


class PandoraServiceControlInformation(EntertainmentServiceControl):
    """ Node-red interface allows some control of Pandora and hence the playback.
    This is it.
    """

    def __init__(self):
        super(PandoraServiceControlInformation, self).__init__()
        self.Like = None
        self.Dislike = None
        self.Skip = None


class PandoraDeviceControl(EntertainmentDeviceControl):
    """ Pandora needs to control A/V devices.
    This is it.
    """

    def __init__(self):
        super(PandoraDeviceControl, self).__init__()
        self.Power = None
        self.Input = None
        self.Volume = None
        self.Zone = None

