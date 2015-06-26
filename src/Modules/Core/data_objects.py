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

__version_info__ = (1, 3, 3)
__version__ = '.'.join(map(str, __version_info__))


# Import system type stuff
from twisted.application.service import Application
from twisted.internet import reactor

# Import PyMh files and modules.


class PyHouseData(object):
    """ ==> pyhouse_obj

    The master object, contains all other 'configuration' objects.

    NOTE that the data entries need to be dicts so json encoding of the data works properly.
    """
    def __init__(self):
        self.APIs = {}  # PyHouseAPIs()
        self.Computer = {}  # ComputerInformation()
        self.House = {}  # HouseInformation()
        self.Services = {}  # CoreServicesInformation()
        self.Twisted = {}  # TwistedInformation()
        self.Xml = {}  # XmlInformation()


class ABaseObject(object):
    """This data is in almost every other object.
    Do not use this object, derive objects from it.
    """
    def __init__(self):
        self.Name = 'Undefined ABaseObject'
        self.Key = 0
        self.Active = False
        self.UUID = None  # The UUID is optional, not all objects use this


class DeviceData(object):
    """
    """
    def __init__(self):
        self.UUID - None
        self.Name = None
        self.DeviceType = 0
        self.DeviceSubType = 0
        self.Key = 0  # Instance number
        self.Active = False


class BaseLightingData(ABaseObject):
    """Basic information about some sort of lighting object.
    """

    def __init__(self):
        super(BaseLightingData, self).__init__()
        self.Comment = ''
        self.Coords = ''  # Room relative coords of the device
        self.IsDimmable = False
        self.ControllerFamily = 'Null'
        self.RoomName = ''
        self.LightingType = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller
        self.DeviceType = 0
        self.DeviceSubType = 0


class ButtonData(BaseLightingData):
    """A Lighting button.
    This is the wall switch and may control more than one light
    Also may control scenes.
    """
    def __init__(self):
        super(ButtonData, self).__init__()
        self.LightingType = 'Button'


class ControllerData(BaseLightingData):
    """This data is common to all lighting controllers.
    """
    def __init__(self):
        super(ControllerData, self).__init__()
        self.LightingType = 'Controller'  # Override the Core definition
        self.InterfaceType = ''  # Serial | USB | Ethernet
        self.Port = ''
        #
        self._DriverAPI = None  # InterfaceType API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        #
        self._Data = None  # InterfaceType specific data
        self._Message = ''
        self._Queue = None


class LightData(BaseLightingData):
    """This is the light info.
    Inherits from BaseLightingData and ABaseObject
    """
    def __init__(self):
        super(LightData, self).__init__()
        self.CurLevel = 0
        self.LightingType = 'Light'


class FamilyData(ABaseObject):
    """A container for every family that has been defined in modules.
    """
    def __init__(self):
        super(FamilyData, self).__init__()
        self.FamilyModuleAPI = None  # Insteon_device.API()
        self.FamilyDeviceModuleName = ''  # Insteon_device
        self.FamilyXmlModuleName = ''  # Insteon_device
        self.FamilyPackageName = ''  # Modules.Families.Insteon


class X10LightingData(LightData):

    def __init__(self):
        super(X10LightingData, self).__init__()
        self.ControllerFamily = "X10"
        self.X10UnitAddress = 'ab'
        self.X10HouseAddress = 0x0F


class ComputerInformation(ABaseObject):
    """
    """
    def __init__(self):
        super(ComputerInformation, self).__init__()
        self.InternetConnection = {}  # InternetConnectionData()
        self.Email = {}  # EmailData()
        self.Mqtt = MqttBrokerData()
        self.Nodes = {}  # NodeData()
        self.Web = {}  # WebData()
        self.Domain = None


class MqttBrokerData(ABaseObject):
    """
    """
    def __init__(self):
        super(MqttBrokerData, self).__init__()
        self.BrokerAddress = None
        self.BrokerPort = None
        self.ClientAPI = None
        self.ProtocolAPI = None


class HouseInformation(ABaseObject):
    """The collection of information about a house.
    Causes JSON errors due to API type data methinks.
    """
    def __init__(self):
        super(HouseInformation, self).__init__()
        self.Name = 'New House'
        self.RefOBJs = {}  # RefHouseObjs()
        self.DeviceOBJs = {}  # DeviceHouseObjs()


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
        self.Irrigation = {}  # IrrigationData()
        self.Lights = {}  # LightData()
        self.Pools = {}  # PoolData()
        self.Thermostats = {}  # ThermostatData()



class JsonHouseData(ABaseObject):
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


class RoomData(ABaseObject):
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


class NodeData(ABaseObject):
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


class NodeInterfaceData(ABaseObject):
    """
    Holds information about each of the interfaces on the *local* node.
    """
    def __init__(self):
        super(NodeInterfaceData, self).__init__()
        self.NodeInterfaceType = None  # Ethernet | Wireless | Loop | Tunnel | Other
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class IrrigationData(ABaseObject):
    """
    """
    def __init__(self):
        super(IrrigationData, self).__init__()
        self.ControllerFamily = 'Null'


class PoolData(ABaseObject):
    """
    """
    def __init__(self):
        super(PoolData, self).__init__()
        self.ControllerFamily = 'Null'


class ThermostatData(ABaseObject):

    def __init__(self):
        super(ThermostatData, self).__init__()
        self.Comment = ''
        self.RoomName = ''
        self.CoolSetPoint = 0
        self.ControllerFamily = 'Null'
        self.CurrentTemperature = 0
        self.HeatSetPoint = 0
        self.ThermostatMode = 'Cool'  # Cool | Heat | Auto | EHeat
        self.ThermostatScale = 'F'  # F | C
        self.ThermostatStatus = 'Off'  # On
        self.DeviceType = 0
        self.DeviceSubType = 0


class ScheduleBaseData(ABaseObject):
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
    """A collection of XLM data used for Configutation
    """
    def __init__(self):
        self.XmlFileName = ''
        self.XmlRoot = None
        self.XmlVersion = __version__


class PyHouseAPIs(object):
    """ ==> pyhouse_obj.APIs
    Most of these have a single entry.
    """

    def __init__(self):
        self.Modules = {}  # A dict of ModuleName : Reference
        self.Comp = {}  # CompAPIs()
        self.House = {}  # HouseAPIs()
        self.CoreSetupAPI = None
        self.PyHouseAPI = None


class CompAPIs(object):
    """ ==> pyhouse_obj.APIs.Comp
    """
    def __init__(self):
        self.CommunicationsAPI = None
        self.ComputerAPI = None
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
        self.Modules = {}  # A dict of ModuleName : Reference
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


class TwistedInformation(object):
    """Twisted info is kept in this class
    """
    def __init__(self):
        self.Application = Application('PyHouse')
        self.Reactor = reactor


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
        self.DomainID = None
        self._TimeZoneOffset = '-5:00'
        self._IsDaylightSavingsTime = False
        # Computed at startup (refreshed periodically)
        self._Sunrise = None
        self._Sunset = None


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
