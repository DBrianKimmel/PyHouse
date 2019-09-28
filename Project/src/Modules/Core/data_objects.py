"""
@Name:      Modules/Core/data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2014
@summary:   This module is the definition of major data objects.

self.Entry        This entry is stored in XML.
self._Entry       This entry in NOT saved in XML but is created in memory when PyHouse starts.

Specific data may be loaded into some attributes for unit testing.

"""

__updated__ = '2019-09-26'
__version_info__ = (19, 9, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files


class PyHouseInformation:
    """
    ==> PyHouse.xxx as in the def below.

    The master object, contains all other 'configuration' objects.

    NOTE that the data entries need to be dicts so json encoding of the data works properly.

    The APIs are kept separate as they should not be a part of the data sent to the browser.
    """

    def __init__(self):
        self.Core = None  # CoreInformation()
        self.Computer = None  # ComputerInformation()
        self.House = None  # HouseInformation()
        # The rest are "Core" components
        self._APIs = None  # PyHouseAPIs()
        self._Config = None  # ConfigInformation()
        self._Parameters = None  # ParameterInformation()
        self._Twisted = None  # TwistedInformation()
        self._Uuids = None  # UuidInformation()


class CoreInformation:
    """
    ==> PyHouse.Core.xxx

    """

    def __init__(self):
        self.Mqtt = {}  # MqttInformation()


class PyHouseAPIs:
    """
    ==> PyHouse._APIs.xxx

    Most of these have a single entry.
    """

    def __init__(self):
        self.Core = None  # CoreAPIs()
        self.Computer = None  # ComputerAPIs()
        self.House = None  # HouseAPIs()
        # self.CoreSetupAPI = None
        # self.PyHouseMainAPI = None


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


class CommunicationAPIs:
    """
    ==> PyHouse._APIs.Computer.CommAPIs.xxx as in the def below.

    """

    def __init__(self):
        self.BluetoothAPI = None
        self.EmailAPI = None
        self.PhoneAPI = None
        self.TwitterAPI = None


class CoreAPIs:
    """
    """

    def __init__(self):
        self.MqttAPI = None
        self.CoreSetupAPI = None
        self.PyHouseMainAPI = None


class DriverStatus:
    """
    """

    def __init__(self):
        self.Name = None
        self.Node = None
        self.Status = None  # Open, Died, Closed


class CommunicationInformation:
    """Email information.
    """

    def __init__(self):
        self.Email = None  # EmailData()
        self.Twitter = None  # TwitterData()


class EmailData:
    """Email information.
    """

    def __init__(self):
        self.EmailFromAddress = ''
        self.EmailToAddress = ''
        self.GmailLogin = ''
        self.GmailPassword = ''


class EthernetControllerInformation:
    """A lighting controller that is connected to the node via Ethernet
    """

    def __init__(self):
        self.InterfaceType = 'Ethernet'
        self.PortNumber = 0
        self.Protocol = 'TCP'


class HostInformation:
    """ Used for all host related information
    This is usually not completely filled in.
    Twisted kinda likes hostnames instead of IP addresses.
    """

    def __init__(self):
        self.Name = None
        self.Port = None
        self.IPv4 = None
        self.IPv6 = None


class HouseAPIs:
    """ These are all the sub-systems of House.

    ==> PyHouse._APIs.House
    """

    def __init__(self):
        # self.EntertainmentAPI = None  # Uses Plugins
        self.FamilyAPI = None  # Uses Plugins
        self.HouseAPI = None
        # self.HvacAPI = None
        # self.IrrigationAPI = None
        # self.LightingAPI = None
        # self.PoolAPI = None
        # self.ScheduleAPI = None
        # self.SecurityAPI = None
        # self.SunRiseSetAPI = None
        # self.SyncAPI = None

# class HvacData():

    """
    DeviceType = 2

    ==> PyHouse.House.Hvac.xxx as in the def below
    """

#    def __init__(self):
#        self.Thermostats = {}  # ThermostatData()  Sub = 1


class ModuleObject:
    """
    """

    def __init__(self):
        # self.Active = False
        pass


class NullControllerInformation:
    """ A lighting controller that is connected to the node via Nothing
    """

    def __init__(self):
        self.InterfaceType = 'Null'


class RiseSetData:
    """ These fields are each a datetime.datetime
    They were calculated by the sunrisesunset module for the house's location and timezone.
    They are therefore, the local time of sunrise and sunset.
    """

    def __init__(self):
        self.Dawn = None
        self.SunRise = None
        self.Noon = None
        self.SunSet = None
        self.Dusk = None


class ScheduleThermostatData:
    """
    """

    def __init__(self):
        self.HeatSetting = None
        self.CoolSetting = None


class SerialControllerInformation:
    """ The additional data needed for serial interfaces.
    """

    def __init__(self):
        self.InterfaceType = 'Serial'
        self.BaudRate = 9600
        self.ByteSize = 8
        self.DsrDtr = False
        self.Parity = 'N'
        self.RtsCts = False
        self.StopBits = 1.0
        self.Timeout = None
        self.XonXoff = False


class TwistedInformation:
    """ Twisted info is kept in this class
    """

    def __init__(self):
        self.Application = None  # Application('PyHouse')
        self.Reactor = None  # reactor
        self.Site = None


class TwitterData:
    """ Email information.
    """

    def __init__(self):
        self.TwitterConsumerKey = ''
        self.TwitterConsumerSecret = ''
        self.TwitterAccessKey = ''
        self.TwitterAccessSecret = ''


class USBControllerInformation:
    """ A lighting controller that is plugged into one of the nodes USB ports
    """

    def __init__(self):
        self.InterfaceType = 'USB'
        self.Product = 0
        self.Vendor = 0


class UuidInformation:
    """

    ==> PyHouse._Uuids.xxx as in the def below
    """

    def __init__(self):
        self.All = {}  # UuidData()
        self.ComputerUuid = None
        self.DomainUuid = None
        self.HouseUuid = None


class UuidData:
    """ a dict with the key = UUID and values of ...

    ==> PyHouse._Uuids.All.{} as in the def below
    """

    def __init__(self):
        self.UUID = None
        self.UuidType = None  # Light, Thermostat, Room ...


class WeatherData:
    """
    """

    def __init__(self):
        self.Temperature = 0  # Degrees C
        self.Humidity = 0  # Percent
        self.DewPoint = 0  # Degrees C
        self.WindSpeed = 0  # Meters / Second
        self.WindDirection = 0  # Degrees


class WeatherInformation:
    """
    """

    def __init__(self):
        self.stationID = None


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
        self.RoomCoords = None  # CoordinateInformation() of the device itself
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


class NodeInformation:
    """ Information about a single node.
    Name is the Node's HostName
    The interface info is only for the local node.

    ==> PyHouse.Computer.Nodes[x].xxx - as in the def below.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.ConnectionAddr_IPv4 = None
        self.ConnectionAddr_IPv6 = None
        self.ControllerTypes = []  # A list of devce controller types attached to this node
        self.ControllerCount = 0  # Number of USB devce controllers attached
        self.Controllers = {}
        self.MasterNode = None
        self.NodeId = None
        self.NodeRole = None
        self.NodeInterfaces = {}  # NodeInterfaceData()


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


class RoomInformation(BaseUUIDObject):
    """ A room of the house.
    Used to draw pictures of the house
    Used to define the location of switches, lights etc.

    ==> PyHouse.House.Rooms.xxx as in the def below
    """

    def __init__(self):
        super(RoomInformation, self).__init__()
        self.Corner = ''  # CoordinateInformation()
        self.Floor = '1st'  # Outside | Basement | 1st | 2nd | 3rd | 4th | Attic | Roof
        # self.LastUpdate = None
        self.Size = ''  # CoordinateInformation()
        self.RoomType = 'Room'
        self._AddFlag = False
        self._DeleteFlag = False


class RulesData(BaseUUIDObject):
    """
    ==> PyHouse.House.Rules.xxx as in the def below
    """

    def __init__(self):
        self.DeviceUUID = None
        self.Condition = None
        self.Time = None
        self.Action = None


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

"""
CoreLightingData dependent.
"""


class XXXGarageDoorData(CoreLightingData):
    """

    ==> PyHouse.House.Security.GarageDoors.xxx as in the def below
    """

    def __init__(self):
        super(XXXGarageDoorData, self).__init__()
        self.Status = None  # Open | Closed


class XXXMotionSensorData(CoreLightingData):
    """ This is the motion sensor data

    SubType = 5
    ==> PyHouse.House.Security.Motion.xxx as in the def below
    """

    def __init__(self):
        super(XXXMotionSensorData, self).__init__()
        self.Motion = None
        self.Timeout = 0

#  ## END DBK
