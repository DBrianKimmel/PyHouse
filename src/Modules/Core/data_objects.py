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
"""

__version_info__ = (1, 3, 0)
__version__ = '.'.join(map(str, __version_info__))


# Import system type stuff
from twisted.application.service import Application
from twisted.internet import reactor

# Import PyMh files and modules.


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
        self.Dimmable = False
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
        self.ControllerInterface = ''  # Serial | USB | Ethernet
        self.Port = ''
        #
        self._DriverAPI = None  # ControllerInterface API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        #
        self._Data = None  # ControllerInterface specific data
        self._Message = ''
        self._Queue = None


class LightData(BaseLightingData):
    """This is the light info.
    Inherits from BaseLightingData and ABaseObject
    """
    def __init__(self):
        self.Controller = None
        self.LightingType = 'Light'
        self.CurLevel = 0


class FamilyData(ABaseObject):
    """A container for every family that has been defined.
    Usually called 'l_family_obj'
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
        self.Controller = False
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.LightingFamily = 'Insteon'
        self.GroupList = ''
        self.GroupNumber = 0
        self.Master = False  # False is Slave
        self.ProductKey = ''
        self.Responder = False


class HouseData(ABaseObject):
    """This is about a single House.
    """
    def __init__(self):
        self.CommunicationsAPI = None
        self.EntertainmentAPI = None
        self.HvacAPI = None
        self.InternetAPI = None
        self.IrrigationAPI = None
        self.LocationAPI = None
        self.LightingAPI = None
        self.PoolAPI = None
        self.RoomsAPI = None
        self.ScheduleAPI = None
        self.SecurityAPI = None
        self.WeatherAPI = None
        #
        self.Location = LocationData()  # one location per house.
        # a dict of zero or more of the following.
        self.Buttons = {}  # ButtonData()
        self.Controllers = {}  # ControllerData()
        self.FamilyData = {}
        self.Internet = {}
        self.Lights = {}  # LightData()
        self.Nodes = {}  # All the PyHouse Nodes in the house
        self.Rooms = {}
        self.Schedules = {}
        self.Thermostats = {}


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


class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.
    """
    def __init__(self):
        # Twisted stuff
        self.Application = Application('PyHouse')
        self.Reactor = reactor
        #
        self.API = None
        self.CoreAPI = None
        # self.HousesAPI = None  # Dropped  V-1.3.0
        self.HouseAPI = None  # added V-1.3.0
        self.LogsAPI = None
        self.WebAPI = None
        #
        self.ComputerData = {}
        self.CoreServicesData = {}  # CoreServices()
        self.FamilyData = {}
        self.LogsData = {}
        # self.HousesData = {}  # HousesData()  Dropped V-1.3.0
        self.HouseData = HouseData()  # added V-1.3.0
        self.Nodes = {}
        self.WebData = {}
        # self.HouseIndex = -1  # Dropped V-1.3.0
        #
        self.XmlFileName = ''
        self.XmlParsed = None
        self.XmlRoot = None
        self.XmlSection = None
        self.XmlVersion = 2


class LocationData(object):
    """Location of the houses
    Lat and Long allow the computation of local sunrise and sunset
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
        self.ControllerInterface = 'Serial'
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
        self.ControllerInterface = 'USB'
        self.Product = 0
        self.Vendor = 0


class  EthernetControllerData(object):
    """A lighting controller that is connected to the noede via ethernet
    """
    def __init__(self):
        self.ControllerInterface = 'Ethernet'
        self.PortNumber = 0
        self.Protocol = 'TCP'


class LogData(object):
    """Locations of varoous logs
    """
    def __init__(self):
        self.Debug = None
        self.Error = None


class CoreServices(object):
    """various twisted services in PyHouse
    """
    def __init__(self):
        self.DiscoveryService = None
        self.DomainService = None
        self.WebServerService = None


class WebData(object):
    """Information about the configuration and control web server
    """
    def __init__(self):
        self.WebPort = 8580
        self.Service = None
        self.Logins = {}  # LoginData()


class LoginData(object):
    """a dict of login_names as keys and encrypted passwords as values - see web_login for details.
    """
    def __init__(self):
        self.LoginName = None
        self.LoginEncryptedPassword = None


# ## END DBK
