"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_data_objects -*-

@Name: PyHouse/src/Modules/Core/data_objects.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 20, 2014
@summary: This module is the definition of major data objects.

Specific data may be loaded into some attributes for unit testing.

NOTE that the ...Data entries need to be dicts so JSON encoding of the data works properly.
"""

__version_info__ = (1, 3, 0)
__version__ = '.'.join(map(str, __version_info__))


# Import system type stuff
from twisted.application.service import Application
from twisted.internet import reactor

# Import PyMh files and modules.


class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.

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
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.UUID = None  # The UUID is optional, not all objects use this


class BaseLightingData(ABaseObject):
    """Basic information about some sort of lighting object.
    """

    def __init__(self):
        self.Comment = ''
        self.Coords = ''  # Room relative coords of the device
        self.IsDimmable = False
        self.LightingFamily = None
        self.RoomName = ''
        self.LightingType = ''  # Button | Light | Controller


class ButtonData(BaseLightingData):
    """A Lighting button.
    This is the wall switch and may control more than one light
    Also may control scenes.
    """
    def __init__(self):
        self.LightingType = 'Button'


class ControllerData(BaseLightingData):
    """This data is common to all lighting controllers.
    """
    def __init__(self):
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
        self.IsController = None
        self.LightingType = 'Light'
        self.CurLevel = 0


class FamilyData(ABaseObject):
    """A container for every family that has been defined.
    """
    def __init__(self):
        self.ModuleAPI = None  # Device_Insteon.API()
        self.ModuleName = ''  # Device_Insteon
        self.PackageName = ''  # Modules.families.Insteon


class InsteonData (LightData):
    """This class contains the Insteon specific information about the various devices controlled by PyHouse.
    """
    def __init__(self):
        super(InsteonData, self).__init__()
        self.InsteonAddress = 0  # 3 bytes
        self.IsController = False
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.LightingFamily = 'Insteon'
        self.GroupList = ''
        self.GroupNumber = 0
        self.IsMaster = False  # False is Slave
        self.ProductKey = ''
        self.IsResponder = False


class UPBData(LightData):
    """Locally held data about each of the PIM controllers we find.
    """

    def __init__(self):
        self.LightingFamily = 'UPB'
        self.UPBAddress = 11  # Same as NetworkID
        self.Password = None
        self.UnitID = 0xFF


class X10LightingData(LightData):

    def __init__(self):
        self.LightingFamily = "X10"
        self.X10Address = 'ab'


class ComputerInformation(object):
    """
    """
    def __init__(self):
        # self.APIs = {}  # ComputerAPIs()
        self.InternetConnection = {}  # InternetConnectionData()
        self.Logs = {}  # LogData()
        self.Nodes = {}  # NodeData()
        self.Web = {}  # WebData()


class XXXComputerAPIs(object):
    """
    """
    def __init__(self):
        self.LogsAPI = None
        self.NodesAPI = None
        self.WebAPI = None


class HouseInformation(ABaseObject):
    """The collection of information about a house.
    Causes JSON errors
    """
    def __init__(self):
        self.APIs = {}  # HouseAPIs()
        self.OBJs = {}  # HouseObjs()


class HouseObjs(object):
    """This is about a single House.
    """
    def __init__(self):
        self.Buttons = {}  # ButtonData()
        self.Controllers = {}  # ControllerData()
        self.FamilyData = {}  # FamilyData()
        self.Lights = {}  # LightData()
        self.Location = {}  # LocationData() - one location per house.
        self.Rooms = {}  # RoomData()
        self.Schedules = {}  # ScheduleData()
        self.Thermostats = {}  # ThermostatData()


class XXXHouseAPIs(object):
    """
    """
    def __init__(self):
        self.EntertainmentAPI = None
        self.InternetAPI = None
        self.LightingAPI = None
        self.ScheduleAPI = None
        #
        # self.CommunicationsAPI = None
        # self.HvacAPI = None
        # self.IrrigationAPI = None
        # self.LocationAPI = None
        # self.PoolAPI = None
        # self.RoomsAPI = None
        # self.SecurityAPI = None
        # self.WeatherAPI = None



class JsonHouseData(ABaseObject):
    """Simplified for JSON encoding.
    """
    def __init__(self):
        self.Buttons = {}
        self.Controllers = {}
        self.Lights = {}
        self.Rooms = {}
        self.Schedules = {}


class RoomData(ABaseObject):
    """A room of the house.
    Used to draw pictures of the house
    Used to define the location of switches, lights etc.
    """
    def __init__(self):
        self.Comment = ''
        self.Corner = ''
        self.Size = ''
        self.RoomType = 'Room'


class NodeData(ABaseObject):
    """Information about a single node.
    Name is the Node's HostName
    """
    def __init__(self):
        self.ConnectionAddr_IPv4 = None
        self.NodeRole = 0
        self.NodeInterfaces = {}  # NodeInterfaceData()


class NodeInterfaceData(ABaseObject):
    """
    Holds information about each of the interfaces on the local node.
    """
    def __init__(self):
        self.NodeInterfaceType = None  # Ethernet | Wireless | Loop | Tunnel | Other
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class ThermostatData(ABaseObject):

    def __init__(self):
        self.ThermostatAPI = None
        self.CurrentTemperature = 0
        self.SetTemperature = 0


class ScheduleData(ABaseObject):
    """A schedule of when events happen.
    """
    def __init__(self):
        self.Level = 0
        self.LightName = None
        self.LightNumber = 0  # Depricated methinks
        self.Object = None  # a light (perhaps other) object
        self.Rate = 0
        self.RoomName = None
        self.Time = None
        self.ScheduleType = 'Device'  # For future expansion into scenes, entertainment etc.
        # for use by web browser - not saved in xml
        self.HouseIx = None
        self.DeleteFlag = False


class InternetConnectionData(ABaseObject):
    """Check our nodes external IP-v4 address
    """
    def __init__(self):
        self.ExternalDelay = 600  # Minimum value
        self.ExternalIPv4 = None  # returned from url to check our external IPv4 address
        self.ExternalUrl = None
        self.IPv6 = None
        self.DynDns = {}  # InternetConnectionDynDnsData()


class InternetConnectionDynDnsData(ABaseObject):
    """One or more dynamic dns servers that we need to update
    """
    def __init__(self):
        self.Interval = 0
        self.Url = None


class XmlInformation(object):
    """A collection of XLM data used for Configutation
    """
    def __init__(self):
        self.XmlFileName = ''
        self.XmlParsed = None
        self.XmlRoot = None
        self.XmlSection = None
        self.XmlVersion = __version__


class PyHouseAPIs(object):
    """
    """

    def __init__(self):
        self.CoreAPI = None
        self.EntertainmentAPI = None
        self.HouseAPI = None
        self.InternetAPI = None
        self.LightingAPI = None
        self.LogsAPI = None
        self.NodesAPI = None
        self.PyHouseAPI = None
        self.ScheduleAPI = None
        self.WebAPI = None
        #
        # self.CommunicationsAPI = None
        # self.HvacAPI = None
        # self.IrrigationAPI = None
        # self.LocationAPI = None
        # self.PoolAPI = None
        # self.RoomsAPI = None
        # self.SecurityAPI = None
        # self.WeatherAPI = None


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
        self.InternetConnectionService = None
        self.IrControlService = None
        self.WebServerService = None


class LocationData(object):
    """Location of the houses
    Latitude and Longitude allow the computation of local sunrise and sunset
    """
    def __init__(self):
        self.City = ''
        self.Latitude = 28.938448
        self.Longitude = -82.517208
        self.Phone = ''
        self.SavingTime = '-4:00'
        self.State = 'FL'
        self.Street = ''
        self.TimeZone = '-5:00'
        self.ZipCode = '12345'


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


class LogData(object):
    """Locations of various logs
    """
    def __init__(self):
        self.Debug = None
        self.Error = None


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


# ## END DBK
