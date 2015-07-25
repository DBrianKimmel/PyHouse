"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_data_objects -*-

@Name:      PyHouse/src/Modules/Core/data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 20, 2014
@summary:   This module is the definition of major data objects.

self.Entry        This entry is stored in xml and memory when read in.
self._Entry       This entry in NOT stored in XML but is stored in memory when read in.

Specific data may be loaded into some attributes for unit testing.

"""
from nevow.livepage import self

__version_info__ = (1, 4, 0)
__version__ = '.'.join(map(str, __version_info__))


# Import system type stuff
# from twisted.application.service import Application
# from twisted.internet import reactor

# Import PyMh files and modules.


class PyHouseData(object):
    """ ==> pyhouse_obj

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
        self.Name = 'Undefined ABaseObject'
        self.Key = 0
        self.Active = False


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

class SensorData(object):
    """
    This data is in almost every other object.
    Do not use this object, derive objects from it.
    """
    def __init__(self):
        self.Name = 'Undefined SensorData Object'
        self.Key = 0  # Instance number
        self.Active = False
        self.UUID = None


class CoreLightingData(DeviceData):
    """Basic information about some sort of lighting object.
    """

    def __init__(self):
        super(CoreLightingData, self).__init__()
        self.DeviceFamily = 'Null'
        self.LightingType = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller


class ButtonData(CoreLightingData):
    """A Lighting button.
    This is the wall switch and may control more than one light
    Also may control scenes.
    """
    def __init__(self):
        super(ButtonData, self).__init__()
        # self.LightingType = 'Button'
        pass


class ControllerData(CoreLightingData):
    """This data is common to all lighting controllers.
    """
    def __init__(self):
        super(ControllerData, self).__init__()
        # self.LightingType = 'Controller'  # Override the Core definition
        self.InterfaceType = ''  # Serial | USB | Ethernet
        self.Port = ''
        # The following are not in XML config file
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
        # self.LightingType = 'Light'


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


class ComputerInformation(BaseObject):
    """
    """
    def __init__(self):
        super(ComputerInformation, self).__init__()
        self.Communication = None
        self.Email = None  # EmailData()
        self.InternetConnection = None  # InternetConnectionData()
        self.Mqtt = None  # MqttBrokerData()
        self.Nodes = None  # NodeData()
        self.Web = None  # WebData()


class MqttInformation(object):
    self.Prefix = ''
    self.Brokers = None  # MqttBrokerData


class MqttBrokerData(BaseObject):
    """ 0-N
    """
    def __init__(self):
        super(MqttBrokerData, self).__init__()
        self.BrokerAddress = None
        self.BrokerPort = None
        self._ClientAPI = None
        self._ProtocolAPI = None


class HouseInformation(BaseObject):
    """The collection of information about a house.
    Causes JSON errors due to API type data methinks.
    """
    def __init__(self):
        super(HouseInformation, self).__init__()
        # self.Name = 'New House'
        self.RefOBJs = None  # RefHouseObjs()
        self.DeviceOBJs = None  # DeviceHouseObjs()


class RefHouseObjs(object):
    """This is about a single House.
    """
    def __init__(self):
        self.FamilyData = {}  # FamilyData('FamilyName')
        self.Location = {}  # LocationData() - one location per house.
        self.Rooms = {}  # RoomData()
        self.Schedules = {}  # ScheduleBaseData()


class DeviceHouseObjs(object):
    """This is about a single House.
    """
    def __init__(self):
        self.Buttons = {}  # ButtonData()
        self.Controllers = {}  # ControllerData()
        self.Irrigation = None  # IrrigationData()
        self.Lights = {}  # LightData()
        self.Pools = {}  # PoolData()
        self.Thermostats = {}  # ThermostatData()
        self.Lighting = None
        self.Hvac = None



class JsonHouseData(BaseObject):
    """Simplified for JSON encoding.
    """
    def __init__(self):
        super(JsonHouseData, self).__init__()
        self.Buttons = {}
        self.Controllers = {}
        self.Lights = {}
        self.Location = {}
        self.Rooms = {}
        self.Schedules = {}
        self.Thermostats = {}


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


class NodeData(BaseObject):
    """Information about a single node.
    Name is the Node's HostName
    The interface info is only for the local node.
    """
    def __init__(self):
        super(NodeData, self).__init__()
        self.Comment = None
        self.ConnectionAddr_IPv4 = None
        self.ConnectionAddr_IPv6 = None
        self.NodeId = None
        self.NodeRole = None
        self.NodeInterfaces = {}  # NodeInterfaceData()


class NodeInterfaceData(BaseObject):
    """
    Holds information about each of the interfaces on the *local* node.
    """
    def __init__(self):
        super(NodeInterfaceData, self).__init__()
        self.NodeInterfaceType = None  # Ethernet | Wireless | Loop | Tunnel | Other
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


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


class PoolData(DeviceData):
    """
    """
    def __init__(self):
        super(PoolData, self).__init__()
        self.DeviceFamily = 'Null'


class ThermostatData(DeviceData):

    def __init__(self):
        super(ThermostatData, self).__init__()
        self.Comment = ''
        self.RoomName = ''
        self.CoolSetPoint = 0
        self.DeviceFamily = 'Null'
        self.CurrentTemperature = 0
        self.HeatSetPoint = 0
        self.ThermostatMode = 'Cool'  # Cool | Heat | Auto | EHeat
        self.ThermostatScale = 'F'  # F | C
        self.ThermostatStatus = 'Off'  # On
        self.DeviceType = 0
        self.DeviceSubType = 0


class ScheduleBaseData(BaseObject):
    """A schedule of when events happen.
    """
    def __init__(self):
        super(ScheduleBaseData, self).__init__()
        self.ScheduleType = 'Device'  # For future expansion into scenes, entertainment etc.
        self.Time = None
        self.DOW = None
        self.Mode = 0
        # for use by web browser - not saved in xml
        self._DeleteFlag = False


class ScheduleLightData(object):
    """A schedule piece for lighting events.
    """
    def __init__(self):
        self.Level = 0
        self.LightName = None
        self.Rate = 0
        self.RoomName = None
        self.ScheduleType = 'LightingDevice'  # For future expansion into scenes, entertainment etc.


class ScheduleThermostatData(object):
    """
    """
    def __init__(self):
        self.HeatSetting = None
        self.CoolSetting = None


class InternetConnectionData(object):
    """Check our nodes external IP-v4 address
    """
    def __init__(self):
        self.ExternalIPv4 = None
        self.ExternalIPv6 = None
        self.LastChanged = None
        self.LocateUrls = {}
        self.UpdateUrls = {}


class XmlInformation(object):
    """A collection of XLM data used for Configuration
    """
    def __init__(self):
        self.XmlFileName = None
        self.XmlRoot = None
        self.XmlVersion = __version__  # Version from this module.
        self.XmlOldVersion = None  # Version of the file read in at program start.


class PyHouseAPIs(object):
    """
    ==> pyhouse_obj.APIs

    Most of these have a single entry.
    """

    def __init__(self):
        self.Computer = None  # ComputerAPIs()
        self.House = None  # HouseAPIs()
        self.CoreSetupAPI = None
        self.PyHouseMainAPI = None


class ComputerAPIs(object):
    """ ==> pyhouse_obj.APIs.Comp
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


class HouseAPIs(object):
    """ ==> pyhouse_obj.APIs.House
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


class TwistedInformation(object):
    """Twisted info is kept in this class
    """
    def __init__(self):
        self.Application = None  # Application('PyHouse')
        self.Reactor = None  # reactor


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


class RiseSetData(object):
    """
    These fields are each an "aware" datetime.datetime
    They were calculated by the sunrisesunset module for the house's location and timezone.
    They are therefore, the local time of sunrise and sunset.
    """
    def __init__(self):
        self.SunRise = None
        self.SunSet = None


class LocationData(object):
    """Location of the houses
    Latitude and Longitude allow the computation of local sunrise and sunset
    """
    def __init__(self):
        self.Street = ''
        self.City = ''
        self.State = 'FL'
        self.ZipCode = '12345'
        self.Latitude = 28.938448
        self.Longitude = -82.517208
        self.Phone = ''
        self.TimeZoneName = 'America/New_York'
        #
        self.DomainID = None
        self.RiseSet = None  # RiseSetData()
        self._TimeZoneOffset = '-5:00'
        self._IsDaylightSavingsTime = False
        # Computed at startup (refreshed periodically)
        # self._Sunrise = None
        # self._Sunset = None


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


class USBControllerData(object):
    """A lighting controller that is plugged into one of the nodes USB ports
    """
    def __init__(self):
        self.InterfaceType = 'USB'
        self.Product = 0
        self.Vendor = 0


class  EthernetControllerData(object):
    """A lighting controller that is connected to the node via Ethernet
    """
    def __init__(self):
        self.InterfaceType = 'Ethernet'
        self.PortNumber = 0
        self.Protocol = 'TCP'


class  NullControllerData(object):
    """A lighting controller that is connected to the node via Nothing
    """
    def __init__(self):
        self.InterfaceType = 'Null'


class WebData(object):
    """Information about the configuration and control web server
    """
    def __init__(self):
        self.WebPort = 8580
        self.Logins = {}  # LoginData()


class LoginData(object):
    """A dict of login_names as keys and encrypted passwords as values - see web_login for details.
    """
    def __init__(self):
        self.LoginName = None
        self.LoginEncryptedPassword = None
        self.LoginFullName = 'Not logged in'
        self.IsLoggedIn = False
        self.ServerState = None


class EmailData(object):
    """Email information.
    """
    def __init__(self):
        self.EmailFromAddress = ''
        self.EmailToAddress = ''
        self.GmailLogin = ''
        self.GmailPassword = ''

# ## END DBK
