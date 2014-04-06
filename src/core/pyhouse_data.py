"""
PyHouse/src/core/pyhouse_data.py

Created on Mar 20, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is used to test a single module.
"""

from twisted.application.service import Application
from twisted.internet import reactor


class LocationData(object):

    def __init__(self):
        self.City = 'Beverly Hills'
        self.Latitude = 28.938448
        self.Longitude = -82.517208
        self.Phone = '(352) 270-8096'
        self.SavingTime = '-4:00'
        self.State = 'FL'
        self.Street = '5191 N Pink Poppy Dr'
        self.TimeZone = '-5:00'
        self.ZipCode = '34465'


class HouseData(object):

    def __init__(self):
        """House.
        """
        self.Name = 'Test House #1'
        self.Key = 0
        self.Active = True
        self.UUID = None
        self.InternetAPI = None
        self.LightingAPI = None
        self.ScheduleAPI = None
        self.Location = LocationData()  # one location per house.
        # a dict of zero or more of the following.
        self.Buttons = {}
        self.Controllers = {}
        self.FamilyData = {}
        self.Internet = {}
        self.Lights = {}
        self.Rooms = {}
        self.Schedules = {}


class HousesData(object):
    """This class holds the data about all houses defined in xml.
    """

    def __init__(self):
        """Houses.
        """
        self.Name = "Test House 1"
        self.Key = 0
        self.Active = True
        self.HouseAPI = None
        self.HouseObject = {0: HouseData()}


class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.
    """

    def __init__(self):
        """PyHouse.
        """
        self.Application = Application('PyHouse')
        self.Reactor = reactor
        #
        self.API = self
        self.CoreAPI = None
        self.HousesAPI = None
        self.LogsAPI = None
        self.WebAPI = None
        #
        self.CoreData = {}
        self.WebData = {}
        self.LogsData = None
        self.HousesData = HousesData()
        self.XmlRoot = None
        self.XmlFileName = ''


class RoomData(object):

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.Corner = ''
        self.Size = ''
        self.Type = 'Room'
        self.UUID = None




# ## END DBK
