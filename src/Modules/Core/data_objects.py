"""
@Name: PyHouse/src/Core/data_objects.py

Created on Mar 20, 2014

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module is the definition of major data objects.

Specific data is loaded into some attributes for unit testing.
"""

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
        self.UUID = None


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


class LightData(BaseLightingData):

    def __init__(self):
        self.Controller = None
        self.Type = 'Light'
        self.CurLevel = 0


class FamilyData(object):
    """A container for every family that has been defined.
    Usually called 'l_family_obj'
    Since they contain API instances, each house has it's own collection of Family Dicts.
    """

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = True
        self.API = None  # Device_Insteon.API()
        self.ModuleName = ''  # Device_Insteon
        self.PackageName = ''  # Modules.families.Insteon


class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.
    """

    def __init__(self):
        self.Application = Application('PyHouse')
        self.Reactor = reactor
        #
        self.API = None
        self.CoreAPI = None
        self.HousesAPI = None
        self.LogsAPI = None
        self.WebAPI = None
        #
        self.CoreServicesData = {}
        self.WebData = {}
        self.LogsData = {}
        self.HousesData = {}
        self.Nodes = {}
        #
        self.XmlRoot = None
        self.XmlFileName = ''


class ServicesData(object):

    def __init__(self):
        self.DiscoveryService = None
        self.DomainService = None


class HousesData(object):
    """This class holds the data about all houses defined in XML.
    """

    def __init__(self):
        self.Name = ""
        self.Key = 0
        self.Active = True
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
        self.Thermostat = {}


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


class RoomData(ABaseObject):

    def __init__(self):
        self.Comment = ''
        self.Corner = ''
        self.Size = ''
        self.Type = 'Room'


class NodeData(ABaseObject):

    def __init__(self):
        self.ConnectionAddr_IPv4 = None
        self.Role = 0
        self.Interfaces = {}


class LogData(object):

    def __init__(self):
        self.Debug = None
        self.Error = None


class ThermostatData(ABaseObject):

    def __init__(self):
        self.ThermostatAPI = None
        self.CurrentTemperature = 0
        self.SetTemperature = 0


# ## END DBK
