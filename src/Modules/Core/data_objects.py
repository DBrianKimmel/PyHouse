"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_data_objects -*-

@Name:      PyHouse/src/Modules/Core/data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2014
@summary:   This module is the definition of major data objects.

self.Entry        This entry is stored in XML.
self._Entry       This entry in NOT saved in XML but is created in memory when PyHouse starts.

Specific data may be loaded into some attributes for unit testing.

"""

__version_info__ = (1, 7, 1)
__version__ = '.'.join(map(str, __version_info__))


class PyHouseData(object):
    """
    ==> PyHouse.xxx as in the def below.

    The master object, contains all other 'configuration' objects.

    NOTE that the data entries need to be dicts so json encoding of the data works properly.
    """
    def __init__(self):
        self.APIs = None  # PyHouseAPIs()
        self.Computer = None  # ComputerInformation()
        self.House = None  # HouseInformation()
        self.Services = None  # CoreServicesInformation()
        self.Twisted = None  # TwistedInformation()
        self.Xml = None  # XmlInformation()


class BaseObject(object):
    """
    This data for non device data.
    Do not use this object, derive objects from it.
    """
    def __init__(self):
        self.Name = 'undefined baseobject'
        self.Key = 0
        self.Active = False


class ComputerAPIs(object):
    """
    ==> PyHouse.APIs.Computer.xxx as in the def below.
    """
    def __init__(self):
        self.ComputerAPI = None
        #
        self.CommunicationsAPI = None
        self.EmailAPI = None
        self.InternetAPI = None
        self.MqttAPI = None
        self.NodesAPI = None
        self.WeatherAPI = None
        self.WebAPI = None


class CoordinateData(object):
    """
    If applied to components of a house (facing the 'Front' of a house:
        X or the distance to the Right from the rooms Left side.
        Y or the distance back from the Front of the room.
        Z or the Height above the floor.
    Preferably the distance is kept in Meters but for you die hard Imperial measurement people in Decimal feet (no inches)!

    In case you need some hints:
        Light switches are about 1.0 meters above the floor.
        Outlets are about 0.2 meters above the floor.
    """
    def __init__(self):
        self.X_Easting = 0.0
        self.Y_Northing = 0.0
        self.Z_Height = 0.0


class CoreServicesInformation(object):
    """Various twisted services in PyHouse
    """
    def __init__(self):
        self.NodeDiscoveryService = None
        self.NodeDomainService = None
        self.InterNodeComm = None
        self.InternetDiscoveryService = None
        self.InternetUpdateService = None
        self.IrControlService = None
        self.WebServerService = None


class EmailData(object):
    """Email information.
    """
    def __init__(self):
        self.EmailFromAddress = ''
        self.EmailToAddress = ''
        self.GmailLogin = ''
        self.GmailPassword = ''


class EthernetControllerData(object):
    """A lighting controller that is connected to the node via Ethernet
    """
    def __init__(self):
        self.InterfaceType = 'Ethernet'
        self.PortNumber = 0
        self.Protocol = 'TCP'


class HouseAPIs(object):
    """
==> PyHouse.APIs.House
    """
    def __init__(self):
        self.HouseAPI = None
        #
        self.EntertainmentAPI = None
        self.FamilyAPI = None
        self.HvacAPI = None
        self.IrrigationAPI = None
        self.LightingAPI = None
        self.PoolAPI = None
        self.ScheduleAPI = None
        self.SecurityAPI = None
        self.SunRiseSetAPI = None


class HvacData(object):
    """
==> PyHouse.House.Hvac.xxx as in the def below
    """
    def __init__(self):
        self.Thermostats = {}  # ThermostatData()


class InternetConnectionData(object):
    """Check our nodes external IP-v4 address
    """
    def __init__(self):
        self.ExternalIPv4 = None
        self.ExternalIPv6 = None
        self.LastChanged = None
        self.LocateUrls = {}
        self.UpdateUrls = {}


class LightingData(object):
    """
==> PyHouse.House.Lighting.xxx as in the def below
    """
    def __init__(self):
        self.Buttons = {}  # ButtonData()
        self.Controllers = {}  # ControllerData()
        self.Lights = {}  # LightData()


class LocationData(object):
    """Location of the houses
    Latitude and Longitude allow the computation of local sunrise and sunset
    """
    def __init__(self):
        self.Street = ''
        self.City = ''
        self.State = ''  # 'FL'
        self.ZipCode = ''  # '12345'
        self.Region = ''  # 'America'
        self.Latitude = 0.0  # 28.938448
        self.Longitude = 0.0  # 82.517208
        self.Elevation = 0.0  # 30
        self.Phone = ''
        self.TimeZoneName = 'America/New_York'  # 'America/New_York'
        #
        self._name = ''  # 'Greenwich'
        self._region = ''  # 'England'
        self.DomainID = None
        self.RiseSet = RiseSetData()  # RiseSetData()
        self._TimeZoneOffset = '-5:00'
        self._IsDaylightSavingsTime = False
        #  Computed at startup (refreshed periodically)
        #  self._Sunrise = None
        #  self._Sunset = None


class MqttInformation(object):
    """
==> PyHouse.Computer.Mqtt.xxx as in the def below
    """
    def __init__(self):
        self.Prefix = ''
        self.Brokers = {}  # MqttBrokerData()
        self.ClientID = ''


class MqttJson(object):
    """
    """
    def __init__(self):
        self.Sender = ''  # The Mqtt name of the sending device.
        self.DateTime = None  # The time on the sending device


class NullControllerData(object):
    """A lighting controller that is connected to the node via Nothing
    """
    def __init__(self):
        self.InterfaceType = 'Null'


class PyHouseAPIs(object):
    """
    ==> PyHouse.APIs

    Most of these have a single entry.
    """

    def __init__(self):
        self.Computer = None  # ComputerAPIs()
        self.House = None  # HouseAPIs()
        self.CoreSetupAPI = None
        self.PyHouseMainAPI = None


class RiseSetData(object):
    """
    These fields are each a datetime.datetime
    They were calculated by the sunrisesunset module for the house's location and timezone.
    They are therefore, the local time of sunrise and sunset.
    """
    def __init__(self):
        self.Dawn = None
        self.SunRise = None
        self.Noon = None
        self.SunSet = None
        self.Dusk = None


class ScheduleLightData(object):
    """A schedule piece for lighting events.
    """
    def __init__(self):
        self.Level = 0
        self.LightName = None
        self.LightUUID = None
        self.Rate = 0
        self.RoomName = None
        self.ScheduleType = 'Lighting'  # For future expansion into scenes, entertainment etc.


class ScheduleThermostatData(object):
    """
    """
    def __init__(self):
        self.HeatSetting = None
        self.CoolSetting = None


class SerialControllerData(object):
    """The additional data needed for serial interfaces.
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


class TwistedInformation(object):
    """Twisted info is kept in this class
    """
    def __init__(self):
        self.Application = None  # Application('PyHouse')
        self.Reactor = None  # reactor


class USBControllerData(object):
    """A lighting controller that is plugged into one of the nodes USB ports
    """
    def __init__(self):
        self.InterfaceType = 'USB'
        self.Product = 0
        self.Vendor = 0


class UuidData(object):
    """
    """
    def __init__(self):
        self.UuidType = None


class WeatherData(object):
    """
    """
    def __init__(self):
        self.Temperature = 0  # Degrees C
        self.Humidity = 0  # Percent
        self.DewPoint = 0  # Degrees C
        self.WindSpeed = 0  # Meters / Second
        self.WindDirection = 0  # Degreed


class WebData(object):
    """Information about the configuration and control web server
    """
    def __init__(self):
        self.WebPort = 8580
        self.SecurePort = 8588
        self.Logins = {}  # LoginData()


class XmlInformation(object):
    """A collection of XLM data used for Configuration
    """
    def __init__(self):
        self.XmlFileName = None
        self.XmlRoot = None
        self.XmlVersion = __version__  # Version from this module.
        self.XmlOldVersion = None  # Version of the file read in at program start.


"""
BaseObject dependent.
"""


class ComputerInformation(BaseObject):
    """
    ==> PyHouse.Computer.xxx - as in the def below.
    """
    def __init__(self):
        super(ComputerInformation, self).__init__()
        self.Communication = None
        self.Email = None  # EmailData()
        self.InternetConnection = None  # InternetConnectionData()
        self.Mqtt = None  # MqttInformation()
        self.Nodes = None  # NodeData()
        self.Primary = False
        self.Web = None  # WebData()


class DeviceData(BaseObject):
    """
    This data is in every other device object.
    Do not use this object, derive objects from it.
    """
    def __init__(self):
        super(DeviceData, self).__init__()
        self.Comment = ''
        self.DeviceFamily = 'Null'
        self.DeviceType = 0
        self.DeviceSubType = 0
        self.RoomCoords = None  # CoordinateData()
        self.RoomName = ''
        self.UUID = None


class FamilyData(BaseObject):
    """A container for every family that has been defined in modules.
    """
    def __init__(self):
        super(FamilyData, self).__init__()
        self.FamilyModuleAPI = None  # Insteon_device.API()
        self.FamilyDeviceModuleName = None  # Insteon_device
        self.FamilyXmlModuleName = None  # Insteon_xml
        self.FamilyXmlModuleAPI = None  # Address of Insteon_xml
        self.FamilyPackageName = None  # Modules.Families.Insteon


class HouseInformation(BaseObject):
    """The collection of information about a house.
    Causes JSON errors due to API type data methinks.

    ==> PyHouse.House.xxx as in the def below.
    """
    def __init__(self):
        super(HouseInformation, self).__init__()
        self.FamilyData = {}  # FamilyData('FamilyName')
        self.Hvac = None  # HvacData()
        self.Irrigation = None  # IrrigationData()
        self.Lighting = {}  # LightingData()
        self.Location = {}  # LocationData() - one location per house.
        self.Pools = {}  # PoolData()
        self.Rooms = {}  # RoomData()
        self.Rules = {}  # RulesData()
        self.Schedules = None  # ScheduleBaseData()


class JsonHouseData(BaseObject):
    """Simplified for JSON encoding.
    """
    def __init__(self):
        super(JsonHouseData, self).__init__()
        self.Buttons = {}
        self.Controllers = {}
        self.Lighting = {}
        self.Location = {}
        self.Rooms = {}
        self.Schedules = {}
        self.Thermostats = {}


class LoginData(BaseObject):
    """ bout the Logged in user
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


class MqttBrokerData(BaseObject):
    """ 0-N
    """
    def __init__(self):
        super(MqttBrokerData, self).__init__()
        self.BrokerAddress = None
        self.BrokerPort = None
        self.UserName = ''
        self.Password = None
        self._ClientAPI = None
        self._ProtocolAPI = None
        self._isTLS = False


class NodeData(BaseObject):
    """Information about a single node.
    Name is the Node's HostName
    The interface info is only for the local node.
    Node[0] is always the local node (Myself)

    ==> PyHouse.Computer.Nodes[x].xxx - as in the def below.
    """
    def __init__(self):
        super(NodeData, self).__init__()
        self.Comment = None
        self.ConnectionAddr_IPv4 = None
        self.ConnectionAddr_IPv6 = None
        self.ControllerTypes = []  # A list of controller types attached to this node
        self.ControllerCount = 0  # Number of USB controllers attached
        self.NodeId = None
        self.NodeRole = None
        self.NodeInterfaces = {}  # NodeInterfaceData()


class NodeInterfaceData(BaseObject):
    """
    Holds information about each of the interfaces on the *local* node.

    ==> PyHouse.Computer.Nodes[x].NodeInterfaces[x].xxx - as in the def below.
    """
    def __init__(self):
        super(NodeInterfaceData, self).__init__()
        self.NodeInterfaceType = None  # Ethernet | Wireless | Loop | Tunnel | Other
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class PoolData(BaseObject):
    """
    """
    def __init__(self):
        super(PoolData, self).__init__()
        self.Comment = None
        self.PoolType = None  # 'Pool', 'Pond', 'HotTub'


class RoomData(BaseObject):
    """A room of the house.
    Used to draw pictures of the house
    Used to define the location of switches, lights etc.
    """
    def __init__(self):
        super(RoomData, self).__init__()
        self.Comment = ''
        self.Corner = ''
        self.Floor = '1st'  # Outside | Basement | 1st | 2nd | 3rd | 4th | Attic | Roof
        self.Size = ''
        self.RoomType = 'Room'


class RulesData(BaseObject):
    """
    """
    def __init__(self):
        self.Device = None
        self.Condition = None
        self.Action = None


class ScheduleBaseData(BaseObject):
    """A schedule of when events happen.
    """
    def __init__(self):
        super(ScheduleBaseData, self).__init__()
        self.ScheduleType = ''
        self.Time = None
        self.DOW = None
        self.Mode = 0
        #  for use by web browser - not saved in xml
        self._DeleteFlag = False


class SensorData(BaseObject):
    """
    This data is in almost every other Sensor object.
    Do not use this object, derive objects from it.
    """
    def __init__(self):
        super(SensorData, self).__init__()
        self.UUID = None


"""
DeviceData dependent.
"""


class CoreLightingData(DeviceData):
    """Basic information about some sort of lighting object.
    """

    def __init__(self):
        super(CoreLightingData, self).__init__()
        self.DeviceFamily = 'Null'
        self.LightingType = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller


class IrrigationData(DeviceData):
    """Info about irrigation systems for a house.
    """
    def __init__(self):
        super(IrrigationData, self).__init__()
        self.Systems = None


class IrrigationSystemData(DeviceData):
    """Info about an irrigation system (may have many zones).
    """
    def __init__(self):
        super(IrrigationSystemData, self).__init__()
        self.UsesMasterValve = False  # Master valve and/or Pump Relay
        self.Zones = {}


class IrrigationZoneData(DeviceData):
    """Info about an irrigation zone
    """
    def __init__(self):
        super(IrrigationZoneData, self).__init__()
        self.Duration = 0  # On time in seconds


class ThermostatData(DeviceData):
    """
    ==> PyHouse.House.Hvac.Thermostats.xxx as in the def below
    """
    def __init__(self):
        super(ThermostatData, self).__init__()
        self.CoolSetPoint = 0
        self.CurrentTemperature = 0
        self.HeatSetPoint = 0
        self.ThermostatMode = 'Cool'  # Cool | Heat | Auto | EHeat
        self.ThermostatScale = 'F'  # F | C
        self.ThermostatStatus = 'Off'  # On


"""
CoreLightingData dependent.
"""


class ButtonData(CoreLightingData):
    """A Lighting button.
    This is the wall switch and may control more than one light
    Also may control scenes.
    """
    def __init__(self):
        super(ButtonData, self).__init__()
        #  self.LightingType = 'Button'
        pass


class ControllerData(CoreLightingData):
    """This data is common to all lighting controllers.

==> PyHouse.House.Lighting.Controllers.xxx as in the def below
    """
    def __init__(self):
        super(ControllerData, self).__init__()
        self.InterfaceType = ''  # Serial | USB | Ethernet
        self.Port = ''
        #  The following are not in XML config file
        self._DriverAPI = None  # InterfaceType API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        self._Data = None  # InterfaceType specific data
        self._Message = ''
        self._Queue = None


class LightData(CoreLightingData):
    """This is the light info.
    """
    def __init__(self):
        super(LightData, self).__init__()
        self.CurLevel = 0
        self.IsDimmable = False
        #  self.LightingType = 'Light'


#  ## END DBK
