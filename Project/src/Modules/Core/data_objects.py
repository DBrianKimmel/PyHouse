"""
@Name:      PyHouse/Project/src/Modules/Core/data_objects.py
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

__updated__ = '2019-08-02'
__version_info__ = (19, 6, 0)
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
        self._Families = None  # FamilyInformation()
        self._Parameters = None  # ParameterInformation()
        self._Twisted = None  # TwistedInformation()
        self._Uuids = None  # UuidInformation()


class CoreInformation:
    """
    ==> PyHouse.Core.xxx

    """

    def __init__(self):
        self.Mqtt = {}  # MqttInformation()


class ParameterInformation:
    """
    ==> PyHouse._Parameters.xxx

    These are filled in first and hold things needed for early initialization.
    """

    def __init__(self):
        self.Name = None
        self.UnitSystem = None
        self.ConfigVersion = 2.0


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


class XXXComputerAPIs:
    """
    ==> PyHouse._APIs.Computer.xxx as in the def below.

    """

    def __init__(self):
        # self.BridgesAPI = None
        self.ComputerAPI = None
        self.CommAPIs = None  # CommunicationAPIs()
        self.InternetAPI = None
        self.NodesAPI = None
        # self.WeatherAPI = None
        # self.WebAPI = None
        # self.WebSocketAPI = None


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


class XXLightingInformation:
    """
    DeviceType = 1

    ==> PyHouse.House.Lighting.xxx as in the def below
    """

    def __init__(self):
        self.Buttons = {}  # ButtonData()  DeviceSubType = 3
        self.Controllers = {}  # ControllerInformation()  DeviceSubType = 1
        self.Lights = {}  # LightData()  DeviceSubType = 2
        self.Outlets = {}


class LoginInformation:
    """ Used for all Login related information
    Either UserName or Name may be given - they are then set to be the same.
    This is done to make it easier to edit the yaml config files.
    """

    def __init__(self):
        self.UserName = None
        self.Name = None
        self.Password = None


class ModuleObject:
    """
    """

    def __init__(self):
        self.Active = False


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


class SecurityData:
    """
    DeviceType = 3
    ==> PyHouse.House.Security.xxx as in the def below
    """

    def __init__(self):
        self.GarageDoors = {}  # DeviceSubtype = 1
        self.MotionSensors = {}  # DeviceSubtype = 2


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


class XXXFamilyInformation(BaseObject):
    """ A container for every family that has been defined in modules.
    """

    def __init__(self):
        super(XXXFamilyInformation, self).__init__()
        self.FamilyDevice_ModuleAPI = None  # Insteon_device.API()
        self.FamilyDevice_ModuleName = None  # Insteon_device
        self.FamilyPackageName = None  # Modules.Families.Insteon
        self.FamilyXml_ModuleName = None  # Insteon_xml
        self.FamilyXml_ModuleAPI = None  # Address of Insteon_xml
        self.FamilyYaml_ModuleName = None
        self.FamilyConfigAPI = None


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


class XXXComputerInformation(BaseUUIDObject):
    """

    ==> PyHouse.Computer.xxx - as in the def below.
    """

    def __init__(self):
        super(XXXComputerInformation, self).__init__()
        self.Primary = False
        self.Priority = 99
        self.Bridges = {}  # BridgeInformation() in Modules.Computer.Bridges.bridge_data
        self.Communication = {}  # CommunicationInformation()
        self.InternetConnection = {}  # InternetConnectionInformation()
        self.Nodes = {}  # NodeInformation()
        self.Weather = {}  # WeatherInformation()
        self.Web = {}  # WebInformation()


class DeviceInformation(BaseUUIDObject):
    """ This data is in every other device object.
    Do not use this object, derive objects from it.
    """

    def __init__(self):
        super(DeviceInformation, self).__init__()
        self.DeviceFamily = 'Null'
        self.DeviceType = None  # Controllers, Lighting, Hvac, Security, Bridge
        self.DeviceSubType = None
        self.RoomCoords = None  # CoordinateInformation() of the device itself
        self.RoomName = ''
        self.RoomUUID = None


class XXXHouseInformation(BaseUUIDObject):
    """ The collection of information about a house.
    Causes JSON errors due to API type data methinks.

    ==> PyHouse.House.xxx as in the def below.
    """

    def __init__(self):
        super(XXXHouseInformation, self).__init__()
        self.HouseMode = 'Home'  # Home, Away, Vacation,
        self.Entertainment = {}  # EntertainmentInformation() in Entertainment/entertainment_data.py
        self.Hvac = {}  # HvacData()
        self.Irrigation = {}  # IrrigationData()
        self.Lighting = {}  # LightingInformation()
        self.Location = {}  # LocationInformation() - one location per house.
        self.Pools = {}  # PoolData()
        self.Rooms = {}  # RoomInformation()
        self.Rules = {}  # RulesData()
        self.Schedules = {}  # ScheduleBaseData()
        self.Security = {}  # SecurityData()
        self._Commands = {}  # Module dependent


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


class NodeInformation(BaseUUIDObject):
    """ Information about a single node.
    Name is the Node's HostName
    The interface info is only for the local node.

    ==> PyHouse.Computer.Nodes[x].xxx - as in the def below.
    """

    def __init__(self):
        super(NodeInformation, self).__init__()
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


class ScheduleBaseData(BaseUUIDObject):
    """ A schedule of when events happen.

    ==> PyHouse.House.Schedules.xxx as in the def below

    See schedule.ScheduleExecution().dispatch_one_schedule() for all the valid types.

    DayOfWeek is a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
            0 is no days of the week
            1 is valid on Monday
            2 is valid on Tuesday
            64 is valid on Sunday
    """

    def __init__(self):
        super(ScheduleBaseData, self).__init__()
        self.DayOfWeek = None  # a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
        self.ScheduleMode = 'Always'  # Always, Home, Away, Vacation, ...
        self.ScheduleType = ''  # Valid Schedule Type
        self.Time = None
        #  for use by web browser - not saved in xml
        self._AddFlag = False
        self._DeleteFlag = False


class SensorData(BaseUUIDObject):
    """ This data is in almost every other Sensor object.
    Do not use this object, derive objects from it.
    """

    def __init__(self):
        super(SensorData, self).__init__()
        self.Sensor = None

"""
ScheduleBaseData dependent
"""


class ScheduleHvacData(ScheduleBaseData):
    """
    """

    def __init__(self):
        super(ScheduleHvacData, self).__init__()
        self.ScheduleType = 'Hvac'


class ScheduleIrrigationData(ScheduleBaseData):
    """
    """

    def __init__(self):
        super(ScheduleIrrigationData, self).__init__()
        self.ScheduleType = 'Irrigation'
        self.Duration = None
        self.System = None
        self.SystemUUID = None
        self.Zone = None


class ScheduleLightData(ScheduleBaseData):
    """ A schedule piece for lighting events.
    """

    def __init__(self):
        super(ScheduleLightData, self).__init__()
        self.Level = 0
        self.LightName = None
        self.LightUUID = None
        self.Rate = 0
        self.RoomName = None
        self.RoomUUID = None
        self.ScheduleType = 'Lighting'  # For future expansion into scenes, entertainment etc.

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


class XXXButtonData(CoreLightingData):
    """ A Lighting button.
    This is the wall switch and may control more than one light
    Also may control scenes.
    """

    def __init__(self):
        super(XXXButtonData, self).__init__()


class XXControllerInformation(CoreLightingData):
    """ This data is common to all lighting controllers.

    _isFunctional is used to disable the controller for the current run.
    It remains an active in the XML so it restarts when problem is solved with device.

    ==> PyHouse.House.Lighting.Controllers.xxx as in the def below
    """

    def __init__(self):
        super(XXControllerInformation, self).__init__()
        self.InterfaceType = ''  # Serial | USB | Ethernet
        # self.LasuUsed = None  # Date time of successful start
        self.Node = None  # node the controller is connected to
        self.Port = ''
        self.Ret = None  # Return Code
        #  The following are not in XML config file
        self._isFunctional = True  # if controller is not working currently
        self._DriverAPI = None  # InterfaceType API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        self._Data = bytearray()  # Rx InterfaceType specific data
        self._Message = bytearray()
        self._Queue = None


class GarageDoorData(CoreLightingData):
    """

    ==> PyHouse.House.Security.GarageDoors.xxx as in the def below
    """

    def __init__(self):
        super(GarageDoorData, self).__init__()
        self.Status = None  # Open | Closed


class MotionSensorData(CoreLightingData):
    """ This is the motion sensor data

    SubType = 5
    ==> PyHouse.House.Security.Motion.xxx as in the def below
    """

    def __init__(self):
        super(MotionSensorData, self).__init__()
        self.Motion = None
        self.Timeout = 0

#  ## END DBK
