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
        self.Family = None
        self.RoomName = ''
        self.Type = ''

    def reprJSON(self):
        """lighting_core.
        """
        l_ret = dict(
           Name = self.Name, Key = self.Key, Active = self.Active,
           Comment = self.Comment, Coords = self.Coords, Dimmable = self.Dimmable,
           Family = self.Family, RoomName = self.RoomName, Type = self.Type, UUID = self.UUID
           )
        l_attrs = filter(lambda aname: not aname.startswith('__'), dir(self))
        for l_attr in l_attrs:
            if not hasattr(l_ret, l_attr):
                l_val = getattr(self, l_attr)
                if not l_attr.startswith('_'):
                    l_ret[l_attr] = str(l_val)
                    # if l_attr == 'InsteonAddress':
                    #    l_ret[l_attr] = web_utils.int2dotted_hex(l_val)
        return l_ret


class ButtonData(BaseLightingData):

    def __init__(self):
        self.Type = 'Button'


class ControllerData(BaseLightingData):
    """This data is common to all controllers.
    There is also interface information that controllers need.
    """

    def __init__(self):
        self.Type = 'Controller'  # Override the Core definition
        self.Interface = ''
        self.Port = ''
        #
        self._DriverAPI = None  # Interface API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        #
        self._Data = None  # Interface specific data
        self._Message = ''
        self._Queue = None

    def reprJSON(self):
        '''lighting_controllers.
        '''
        # print "lighting_controllers.reprJSON(1)"
        l_ret = super(ControllerData, self).reprJSON()  # lighting_core data
        l_ret.update(dict(
            Interface = self.Interface,
            Port = self.Port
            ))
        # print "lighting_controllers.reprJSON(2) {0:}".format(l_ret)
        return l_ret


class LightData(BaseLightingData):
    """This is the light info.
    Inherits from BaseLightingData and ABaseObject
    """

    def __init__(self):
        self.Controller = None
        self.Type = 'Light'
        self.CurLevel = 0


class FamilyData(ABaseObject):
    """A container for every family that has been defined.
    Usually called 'l_family_obj'
    Since they contain API instances, each house has it's own collection of Family Dicts.
    """

    def __init__(self):
        self.ModuleAPI = None  # Device_Insteon.API()
        self.ModuleName = ''  # Device_Insteon
        self.PackageName = ''  # Modules.families.Insteon

    def reprJSON(self):
        l_ret = dict(Name = self.Name, Key = self.Key, Active = self.Active,
            ModuleName = self.ModuleName,
            PackageName = self.PackageName
            )
        return l_ret


class InsteonData (LightData):
    """This class contains the Insteon specific information about the various devices
    controlled by PyHouse.
    """

    def __init__(self):
        super(InsteonData, self).__init__()
        self.InsteonAddress = 0  # 3 bytes
        self.Controller = False
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.Family = 'Insteon'
        self.GroupList = ''
        self.GroupNumber = 0
        self.Master = False  # False is Slave
        self.ProductKey = ''
        self.Responder = False

    def reprJSON(self, p_ret):
        """Device_Insteon.
        """
        p_ret.update(dict(
            # InsteonAddress = Insteon_utils.int2dotted_hex(self.InsteonAddress),
            Controller = self.Controller,
            DevCat = self.DevCat,
            GroupList = self.GroupList,
            GroupNumber = self.GroupNumber,
            Master = self.Master,
            Responder = self.Responder,
            ProductKey = self.ProductKey
            ))
        return p_ret


class XXXHousesData(ABaseObject):
    """This class holds the data about all houses defined in XML.
    """

    def __init__(self):
        self.HouseAPI = None
        self.HouseObject = {}


class HouseData(ABaseObject):

    def __init__(self):
        """This is about a single House.
        """
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
        self.Buttons = {}
        self.Controllers = {}
        self.FamilyData = {}
        self.Internet = {}
        self.Lights = {}
        self.Nodes = {}  # All the PyHouse Nodes in the house
        self.Rooms = {}
        self.Schedules = {}
        self.Thermostats = {}

    def reprJSON(self):
        """HouseData.
        """
        l_ret = dict(
            Name = self.Name, Key = self.Key, Active = self.Active,
            Buttons = self.Buttons,
            Controllers = self.Controllers,
            Lights = self.Lights,
            Location = self.Location,
            Internet = self.Internet,
            Family = self.FamilyData,
            Rooms = self.Rooms,
            Schedules = self.Schedules,
            UUID = self.UUID
            )
        return l_ret


class RoomData(ABaseObject):

    def __init__(self):
        self.Comment = ''
        self.Corner = ''
        self.Size = ''
        self.Type = 'Room'

    def reprJSON(self):
        l_ret = dict(Name = self.Name, Key = self.Key, Active = self.Active,
                    Comment = self.Comment, Corner = self.Corner, Size = self.Size,
                    Type = self.Type, UUID = self.UUID)
        return l_ret


class NodeData(ABaseObject):

    def __init__(self):
        self.ConnectionAddr_IPv4 = None
        self.Role = 0
        self.Interfaces = {}


class NodeInterfaceData(ABaseObject):
    """
    Holds information about each of the interfaces on the local node.

    @param  Type: Ethernet | Wireless | Loop | Tunnel | Other
    """
    def __init__(self):
        self.Type = None
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class ThermostatData(ABaseObject):

    def __init__(self):
        self.ThermostatAPI = None
        self.CurrentTemperature = 0
        self.SetTemperature = 0


class ScheduleData(ABaseObject):

    def __init__(self):
        self.Level = 0
        self.LightName = None
        self.LightNumber = 0  # Depricated methinks
        self.Object = None  # a light (perhaps other) object
        self.Rate = 0
        self.RoomName = None
        self.Time = None
        self.Type = 'Device'  # For future expansion into scenes, entertainment etc.
        # for use by web browser - not saved in xml
        self.HouseIx = None
        self.DeleteFlag = False


class InternetConnectionData(ABaseObject):
    """Check our external IP-v4 address
    """

    def __init__(self):
        self.ExternalDelay = 600  # Minimum value
        self.ExternalIPv4 = None  # returned from url to check our external IPv4 address
        self.ExternalUrl = None
        self.IPv6 = None
        self.DynDns = {}

    def XXreprJSON(self):
        return dict(Name = self.Name, Key = self.Key, Active = self.Active,
                    ExternalDelay = self.ExternalDelay,
                    ExternalIP = self.ExternalIPv4, ExternalUrl = self.ExternalUrl,
                    DynDns = self.DynDns
                    )


class InternetConnectionDynDnsData(ABaseObject):

    def __init__(self):
        self.Interval = 0
        self.Url = None

    def reprJSON(self):
        return dict(Name = self.Name, Key = self.Key, Active = self.Active,
                    Interval = self.Interval, Url = self.Url
                    )


class PyHousesData(object):
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
        self.CoreServicesData = {}  # CoreServicesData()
        self.WebData = {}
        self.LogsData = {}
        # self.HousesData = {}  # HousesData()  Dropped V-1.3.0
        self.HouseData = {}  # added V-1.3.0
        self.Nodes = {}
        # self.HouseIndex = -1  # Dropped V-1.3.0
        #
        self.XmlRoot = None
        self.XmlFileName = ''
        self.XmlVersion = 2


class LocationData(object):

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

    def reprJSON(self):
        l_ret = dict(
            City = self.City, Latitude = self.Latitude, Longitude = self.Longitude, Phone = self.Phone,
            SavingsTime = self.SavingTime, State = self.State, Street = self.Street, TimeZone = self.TimeZone,
            ZipCode = self.ZipCode
            )
        return l_ret


class SerialControllerData(object):
    """The additional data needed for serial interfaces.
    """

    def __init__(self):
        # from Modules.lights import lighting_controllers
        # lighting_controllers.ControllerData().__init__()
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

    def __init__(self):
        self.InterfaceType = 'USB'
        self.Product = 0
        self.Vendor = 0


class  EthernetControllerData(object):

    def __init__(self):
        self.InterfaceType = 'Ethernet'
        self.PortNumber = 0
        self.Protocol = 'TCP'


class LogData(object):

    def __init__(self):
        self.Debug = None
        self.Error = None


class CoreServicesData(object):

    def __init__(self):
        self.DiscoveryService = None
        self.DomainService = None


class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8580
        self.Service = None
        self.Logins = {}  # a dict of login_names as keys and encrypted passwords as values - see web_login for details.


# ## END DBK
