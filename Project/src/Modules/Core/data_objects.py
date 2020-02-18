"""
@Name:      Modules/Core/data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2014
@summary:   This module is the definition of major data objects.

self.Entry        This entry is stored in XML.
self._Entry       This entry in NOT saved in XML but is created in memory when PyHouse starts.

Specific data may be loaded into some attributes for unit testing.

"""

__updated__ = '2020-02-11'
__version_info__ = (20, 2, 3)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files


class BaseObject:
    """
    This is the base object.
    It is part of almost every entry in the PyHouse database.
    This data for non device data.
    Do not use this object, derive objects from it.
    """

    def __init__(self):
        self.Name = 'undefined baseobject'
        # self.Key = 0
        # self.Active = False
        self.Comment = ''
        self.LastUpdate = None


class NullControllerInformation:
    """ A lighting controller that is connected to the node via Nothing
    """

    def __init__(self):
        self.InterfaceType = 'Null'


class WebInformation:
    """ Information about the configuration and control web server

    ==> PyHouse.Computer.Web.xxx - as in the def below.
    """

    def __init__(self):
        self.WebPort = 8580
        self.WebServer = None
        self.WebSocketPort = 8581
        self.WebSocketServer = None
        self.SecurePort = 8588
        self.secureServer = None
        self.Logins = {}  # LoginData()


class BaseUUIDObject(BaseObject):
    """ Takes a base object and adds a Unique ID to it.
    """

    def __init__(self):
        super(BaseUUIDObject, self).__init__()
        self.UUID = None

"""
BaseObject dependent.
"""


class InternetConnectionInformation(BaseObject):
    """ Check our nodes external IP-v4 address
    """

    def __init__(self):
        self.ExternalIPv4 = '0.0.0.0'
        self.ExternalIPv6 = '2001:db8::dead:beef'
        self.LastChanged = None
        self.UpdateInterval = 86400  # Seconds
        self.LocateUrls = []
        self.UpdateUrls = []


class JsonHouseData(BaseObject):
    """ Simplified for JSON encoding.
    """

    def __init__(self):
        super(JsonHouseData, self).__init__()
        self.Buttons = {}
        self.Controllers = {}
        self.HVAC = {}
        self.Irrigation = {}
        self.Lighting = {}
        self.Location = {}
        self.Rooms = {}
        self.Schedules = {}
        # self.Thermostats = {}

"""
BaseUUIDObject dependent.
"""


class DeviceInformation(BaseUUIDObject):
    """ This data is in every other device object.
    Do not use this object, derive objects from it.
    """

    def __init__(self):
        super(DeviceInformation, self).__init__()
        # self.DeviceFamily = 'Null'
        self.DeviceType = None  # Controllers, Lighting, Hvac, Security, Bridge
        self.DeviceSubType = None
        self.RoomCoords = None  # of the device itself
        self.RoomName = ''
        self.RoomUUID = None


class LoginData(BaseUUIDObject):
    """ About the Logged in user

    ==> PyHouse.Computer.Web.Logins.xxx - as in the def below.
    """

    def __init__(self):
        super(LoginData, self).__init__()
        self.LoginFullName = 'Not logged in'
        self.LoginIP = None
        self.LoginPasswordChangeFlag = True
        self.LoginPasswordCurrent = None
        self.LoginPasswordNew = None
        self.LoginRole = 'None'
        self.IsLoggedIn = False
        self.ServerState = None


class NodeControllerInformation(BaseUUIDObject):
    """
    """

    def __init__(self):
        super(NodeControllerInformation, self).__init__()


class NodeInterfaceData(BaseUUIDObject):
    """ Holds information about each of the interfaces on the *local* node.

    ==> PyHouse.Computer.Nodes[x].NodeInterfaces[x].xxx - as in the def below.
    """

    def __init__(self):
        super(NodeInterfaceData, self).__init__()
        self.NodeInterfaceType = None  # Ethernet | Wireless | Loopback | Tunnel | Other
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class SensorData(BaseUUIDObject):
    """ This data is in almost every other Sensor object.
    Do not use this object, derive objects from it.
    """

    def __init__(self):
        super(SensorData, self).__init__()
        self.Sensor = None

"""
DeviceInformation dependent.
"""


class CoreLightingData(DeviceInformation):
    """ Basic information about some sort of lighting object.
    """

    def __init__(self):
        super(CoreLightingData, self).__init__()
        # self. Lighting Type = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller
        self.ControllerNode = None
        self.ControllerName = None

#  ## END DBK
