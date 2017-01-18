"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_data_objects -*-

@Name:      PyHouse/src/Modules/Core/data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2014
@summary:   This module is the definition of major data objects.

self.Entry        This entry is stored in XML.
self._Entry       This entry in NOT saved in XML but is created in memory when PyHouse starts.

Specific data may be loaded into some attributes for unit testing.

"""

__updated__ = '2017-01-16'
__version_info__ = (1, 7, 5)
__version__ = '.'.join(map(str, __version_info__))


class PyHouseData(object):
    """
    ==> PyHouse.xxx as in the def below.

    The master object, contains all other 'configuration' objects.

    NOTE that the data entries need to be dicts so json encoding of the data works properly.

    The APIs are kept seperate as they should not be a part of the data sent to the browser.
    """
    def __init__(self):
        self.APIs = None  # PyHouseAPIs()
        self.Computer = None  # ComputerInformation()
        self.House = None  # HouseInformation()
        self.Twisted = None  # TwistedInformation()
        self.Uuids = None  # AllUuids()
        self.Xml = None  # XmlInformation()


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


class BaseObject(object):
    """
    This data for non device data.
    Do not use this object, derive objects from it.
    """
    def __init__(self):
        self.Name = 'undefined baseobject'
        self.Key = 0
        self.Active = False


class CommunicationAPIs(object):
    """

    ==> PyHouse.APIs.Computer.Communication as in the def below.
    """
    def __init__(self):
        self.BluetoothAPI = None
        self.EmailAPI = None
        self.PhoneAPI = None
        self.TwitterAPI = None


class ComputerAPIs(object):
    """

    ==> PyHouse.APIs.Computer.xxx as in the def below.
    """
    def __init__(self):
        self.ComputerAPI = None
        self.Communication = None  # CommunicationAPIs()
        self.InternetAPI = None
        self.MqttAPI = None
        self.NodesAPI = None
        self.WeatherAPI = None
        self.WebAPI = None


class CoordinateData(object):
    """
    If applied to components of a house (facing the 'Front' of a house:
        X or the distance to the Right from the room's Left side.
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


class CommunicationData(object):
    """Email information.
    """
    def __init__(self):
        self.Email = None  # EmailData()
        self.Twitter = None  # TwitterData()


class EmailData(object):
    """Email information.
    """
    def __init__(self):
        self.EmailFromAddress = ''
        self.EmailToAddress = ''
        self.GmailLogin = ''
        self.GmailPassword = ''



class EntertainmentData(object):
    """

    ==> PyHouse.House.Entertainment.xxx as in the def below.
    """
    def __init__(self):
        self.Onkyo = None
        self.Panasonic = None
        self.Pioneer = None
        self.Samsung = None
        self.Sharp = None
        self.Sony = None


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
        self.EntertainmentAPI = None
        self.FamilyAPI = None
        self.HouseAPI = None
        self.HvacAPI = None
        self.IrrigationAPI = None
        self.LightingAPI = None
        self.PoolAPI = None
        self.ScheduleAPI = None
        self.SecurityAPI = None
        self.SunRiseSetAPI = None


class HvacData(object):
    """
    DeviceType = 2

    ==> PyHouse.House.Hvac.xxx as in the def below
    """
    def __init__(self):
        self.Thermostats = {}  # ThermostatData()  Sub = 1


class LightingData(object):
    """
    DeviceType = 1

    ==> PyHouse.House.Lighting.xxx as in the def below
    """
    def __init__(self):
        self.Buttons = {}  # ButtonData()  Sub = 3
        self.Controllers = {}  # ControllerData()  Sub = 1
        self.Lights = {}  # LightData()  Sub = 2


class LocationData(object):
    """ Location of the houses
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


class ModuleObject(object):
    """
    """
    def __init__(self):
        self.Active = False


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
    """ A lighting controller that is connected to the node via Nothing
    """
    def __init__(self):
        self.InterfaceType = 'Null'


class RiseSetData(object):
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


class ScheduleThermostatData(object):
    """
    """
    def __init__(self):
        self.HeatSetting = None
        self.CoolSetting = None


class SecurityData(object):
    """
    DeviceType = 3
    ==> PyHouse.House.Security.xxx as in the def below
    """
    def __init__(self):
        self.GarageDoors = {}  # DeviceSubtype = 1
        self.MotionSensors = {}  # DeviceSubtype = 2


class SerialControllerData(object):
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


class TwistedInformation(object):
    """ Twisted info is kept in this class
    """
    def __init__(self):
        self.Application = None  # Application('PyHouse')
        self.Reactor = None  # reactor


class TwitterData(object):
    """ Email information.
    """
    def __init__(self):
        self.TwitterConsumerKey = ''
        self.TwitterConsumerSecret = ''
        self.TwitterAccessKey = ''
        self.TwitterAccessSecret = ''


class USBControllerData(object):
    """ A lighting controller that is plugged into one of the nodes USB ports
    """
    def __init__(self):
        self.InterfaceType = 'USB'
        self.Product = 0
        self.Vendor = 0


class AllUuids(object):
    """

    ==> PyHouse.Uuids.xxx as in the def below
    """
    def __init__(self):
        self.All = {}  # UuidData()
        self.ComputerUuid = None
        self.DomainUuid = None
        self.HouseUuid = None


class UuidData(object):
    """ a dict with the key = UUID and values of ...

    ==> PyHouse.Uuids.All.{} as in the def below
    """
    def __init__(self):
        self.UUID = None
        self.UuidType = None  # Light, Thermostat, Room ...


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
    """ Information about the configuration and control web server
    """
    def __init__(self):
        self.WebPort = 8580
        self.SecurePort = 8588
        self.Logins = {}  # LoginData()


class XmlInformation(object):
    """ A collection of XLM data used for Configuration

    ==> PyHouse.Xml.xxx
    """
    def __init__(self):
        self.XmlConfigDir = '/etc/pyhouse/'
        self.XmlFileName = None
        self.XmlRoot = None
        self.XmlVersion = __version__  # Version from this module.
        self.XmlOldVersion = None  # Version of the file read in at program start.


class BaseUUIDObject(BaseObject):
    """
    """
    def __init__(self):
        super(BaseUUIDObject, self).__init__()
        self.UUID = None


"""
BaseObject dependent.
"""

class FamilyData(BaseObject):
    """ A container for every family that has been defined in modules.
    """
    def __init__(self):
        super(FamilyData, self).__init__()
        self.FamilyModuleAPI = None  # Insteon_device.API()
        self.FamilyDeviceModuleName = None  # Insteon_device
        self.FamilyXmlModuleName = None  # Insteon_xml
        self.FamilyXmlModuleAPI = None  # Address of Insteon_xml
        self.FamilyPackageName = None  # Modules.Families.Insteon


class InternetConnectionData(BaseObject):
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


class RulesData(BaseObject):
    """
    """
    def __init__(self):
        self.Device = None
        self.Condition = None
        self.Action = None


"""
BaseUUIDObject dependent.
"""

class ComputerInformation(BaseUUIDObject):
    """

    ==> PyHouse.Computer.xxx - as in the def below.
    """
    def __init__(self):
        super(ComputerInformation, self).__init__()
        self.Comm = {}  # CommunicationData()
        self.InternetConnection = {}  # InternetConnectionData()
        self.Mqtt = {}  # MqttInformation()
        self.Nodes = {}  # NodeData()
        self.Primary = False
        self.Web = {}  # WebData()


class DeviceData(BaseUUIDObject):
    """ This data is in every other device object.
    Do not use this object, derive objects from it.
    """
    def __init__(self):
        super(DeviceData, self).__init__()
        self.Comment = ''
        self.DeviceFamily = 'Null'
        self.DeviceType = 0  # 0 = Lighting, 1 = HVAC, 2 = Security
        self.DeviceSubType = 0
        self.RoomCoords = None  # CoordinateData()
        self.RoomName = ''
        self.RoomUUID = None


class HouseInformation(BaseUUIDObject):
    """ The collection of information about a house.
    Causes JSON errors due to API type data methinks.

    ==> PyHouse.House.xxx as in the def below.
    """
    def __init__(self):
        super(HouseInformation, self).__init__()
        self.FamilyData = {}  # FamilyData['FamilyName']
        self.HouseMode = 'Home'  # Home, Away, Vacation,
        self.Entertainment = {}  # EntertainmentData()
        self.Hvac = {}  # HvacData()
        self.Irrigation = {}  # IrrigationData()
        self.Lighting = {}  # LightingData()
        self.Location = {}  # LocationData() - one location per house.
        self.Pools = {}  # PoolData()
        self.Rooms = {}  # RoomData()
        self.Rules = {}  # RulesData()
        self.Schedules = {}  # ScheduleBaseData()
        self.Security = {}  # SecurityData()


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


class NodeData(BaseUUIDObject):
    """ Information about a single node.
    Name is the Node's HostName
    The interface info is only for the local node.

    ==> PyHouse.Computer.Nodes[x].xxx - as in the def below.
    """
    def __init__(self):
        super(NodeData, self).__init__()
        self.Comment = None
        self.ConnectionAddr_IPv4 = None
        self.ConnectionAddr_IPv6 = None
        self.ControllerTypes = []  # A list of controller types attached to this node
        self.ControllerCount = 0  # Number of USB controllers attached
        self.LastUpdate = None
        self.NodeId = None
        self.NodeRole = None
        self.NodeInterfaces = {}  # NodeInterfaceData()


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


class PoolData(BaseUUIDObject):
    """ Holds information about the pool(s)

    ==> PyHouse.House.Pools.{}.
    """
    def __init__(self):
        super(PoolData, self).__init__()
        self.Comment = None
        self.PoolType = None  # 'Pool', 'Pond', 'HotTub'


class RoomData(BaseUUIDObject):
    """ A room of the house.
    Used to draw pictures of the house
    Used to define the location of switches, lights etc.

    ==> PyHouse.House.Rooms.xxx as in the def below
    """
    def __init__(self):
        super(RoomData, self).__init__()
        self.Comment = ''
        self.Corner = ''  # CoordinateData()
        self.Floor = '1st'  # Outside | Basement | 1st | 2nd | 3rd | 4th | Attic | Roof
        self.LastUpdate = None
        self.Size = ''  # CoordinateData()
        self.RoomType = 'Room'
        self._AddFlag = False
        self._DeleteFlag = False


class ScheduleBaseData(BaseUUIDObject):
    """ A schedule of when events happen.

    DOW is a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
            0 is no days of the week
            1 is valid on Monday
            2 is valid on Tuesday
            64 is valid on Sunday
    """
    def __init__(self):
        super(ScheduleBaseData, self).__init__()
        self.DOW = None  # a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
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
DeviceData dependent.
"""


class CoreLightingData(DeviceData):
    """ Basic information about some sort of lighting object.
    """

    def __init__(self):
        super(CoreLightingData, self).__init__()
        # self. Lighting Type = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller
        pass


class IrrigationData(DeviceData):
    """ Info about any/all irrigation systems for a house.
    """
    def __init__(self):
        super(IrrigationData, self).__init__()
        self.Systems = {}  # IrrigationSystemData()


class IrrigationSystemData(DeviceData):
    """ Info about an irrigation system (may have many zones).
    """
    def __init__(self):
        super(IrrigationSystemData, self).__init__()
        self.UsesMasterValve = False  # Master valve and/or Pump Relay
        self.FirstZone = 0
        self.Zones = {}  # IrrigationZoneData()


class IrrigationZoneData(object):
    """ Info about an irrigation zone
    """
    def __init__(self):
        # super(IrrigationZoneData, self).__init__()
        self.Name = 'Default zone'
        self.Key = 0
        self.Rate = 0  # litres per Minute
        self.Duration = 0  # On time in seconds
        self.Next = 0
        self.Previous = -1
        self.EmitterCount = 1
        self.EmitterType = 'Rotor'


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
        self.UUID = None


"""
CoreLightingData dependent.
"""


class ButtonData(CoreLightingData):
    """ A Lighting button.
    This is the wall switch and may control more than one light
    Also may control scenes.
    """
    def __init__(self):
        super(ButtonData, self).__init__()


class ControllerData(CoreLightingData):
    """ This data is common to all lighting controllers.

    ==> PyHouse.House.Lighting.Controllers.xxx as in the def below
    """
    def __init__(self):
        super(ControllerData, self).__init__()
        self.InterfaceType = ''  # Serial | USB | Ethernet
        self.Port = ''
        self.Ret = None  # Return Code
        #  The following are not in XML config file
        self._DriverAPI = None  # InterfaceType API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        self._Data = None  # InterfaceType specific data
        self._Message = ''
        self._Queue = None


class GarageDoorData(CoreLightingData):
    """

    ==> PyHouse.House.Security.GarageDoors.xxx as in the def below
    """
    def __init__(self):
        super(GarageDoorData, self).__init__()
        self.Status = None  # Open | Closed


class LightData(CoreLightingData):
    """ This is the light info.

    ==> PyHouse.House.Lighting.Lightss.xxx as in the def below
    """
    def __init__(self):
        super(LightData, self).__init__()
        self.CurLevel = 0
        self.IsDimmable = False


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
