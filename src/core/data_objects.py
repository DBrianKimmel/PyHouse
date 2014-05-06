"""
@Name: PyHouse/src/core/data_objects.py

Created on Mar 20, 2014

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module is the definition of major data objects.

Specific data is loaded into some attributes for unit testing.
"""

from twisted.application.service import Application
from twisted.internet import reactor


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
        self.CoreData = {}
        self.WebData = {}
        self.LogsData = {}
        self.HousesData = {}
        #
        self.XmlRoot = None
        self.XmlFileName = ''


class CoreData(object):

    def __init__(self):
        self.Nodes = {}
        self.DiscoveryService = None
        self.DomainService = None


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


class BasePyHouseObject(object):

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.UUID = None


class HousesData(object):
    """This class holds the data about all houses defined in XML.
    """

    def __init__(self):
        self.Name = ""
        self.Key = 0
        self.Active = True
        self.HouseAPI = None
        self.HouseObject = {}


class HouseData(BasePyHouseObject):

    def __init__(self):
        """House.
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
        self.Rooms = {}
        self.Schedules = {}
        self.Thermostat = {}


class RoomData(BasePyHouseObject):

    def __init__(self):
        self.Comment = ''
        self.Corner = ''
        self.Size = ''
        self.Type = 'Room'


class NodeData(BasePyHouseObject):

    def __init__(self):
        self.ConnectionAddr = None
        self.Role = 0
        self.Interfaces = {}


class LogData(object):

    def __init__(self):
        self.Debug = None
        self.Error = None


class BaseLightingData(BasePyHouseObject):
    """Information
    """

    def __init__(self):
        self.Comment = ''
        self.Coords = ''  # Room relative coords of the light switch
        self.Dimmable = False
        self.Family = ''
        self.RoomName = ''
        self.Type = ''


class LightData(BaseLightingData):

    def __init__(self):
        # super(LightData, self).__init__()
        self.Controller = None
        self.Type = 'Light'
        self.CurLevel = 0


class ButtonData(BaseLightingData):

    def __init__(self):
        # super(ButtonData, self).__init__()
        self.Type = 'Button'


class ControllerData(BaseLightingData):
    """This data is common to all controllers.
    There is also interface information that controllers need.
    """

    def __init__(self):
        # super(ControllerData, self).__init__()  # The core data
        self.Type = 'Controller'  # Override the core definition
        self.Interface = ''
        self.Port = ''
        #
        self._DriverAPI = None  # Interface API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        #
        self._Data = None  # Interface specific data
        self._Message = ''
        self._Queue = None


class ThermostatData(BasePyHouseObject):

    def __init__(self):
        self.ThermostatAPI = None
        self.CurrentTemperature = 0
        self.SetTemperature = 0


# ## END DBK
