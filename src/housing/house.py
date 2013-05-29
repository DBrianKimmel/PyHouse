#!/usr/bin/python

"""Handle all the house(s) information.

main/house.py

There is one instance of this module for each house being controlled.

House.py knows everything about a single house.

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such as
moonrise, tides, etc.

"""

# Import system type stuff
import logging

# Import PyMh files
from src.scheduling import schedule
from src.housing import internet
from src.housing import location
from src.housing import rooms


g_debug = 0
# 0 = off

g_logger = None

House_Data = {}


class HouseData(object):

    def __init__(self):
        self.Active = False
        self.Key = 0
        self.Name = ''
        self.InternetAPI = None
        self.LightingAPI = None
        self.ScheduleAPI = None
        self.Location = location.LocationData()
        self.Buttons = {}
        self.Controllers = {}
        self.Internet = {}
        self.Lights = {}
        self.Rooms = {}
        self.Schedule = {}

    def __repr__(self):
        l_ret = ' House:: '
        l_ret += 'Name:{0:}, '.format(self.Name)
        l_ret += "Active:{0:}, ".format(self.Active)
        l_ret += "Key:{0:}, ".format(self.Key)
        l_ret += "Lights:{0:}, ".format(len(self.Lights))
        l_ret += "Controllers:{0:}, ".format(len(self.Controllers))
        l_ret += "Buttons:{0:}, ".format(len(self.Buttons))
        l_ret += "Rooms:{0:}, ".format(len(self.Rooms))
        l_ret += "Schedules:{0:}".format(len(self.Schedule))
        return l_ret


class HouseReadWriteConfig(location.ReadWriteConfig, rooms.ReadWriteConfig):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def read_house(self, p_house_obj, p_house_xml):
        """Read house information, location and rooms.

        The main data is House_Data.
        """
        self.xml_read_common_info(p_house_obj, p_house_xml)
        p_house_obj.Location = self.read_location(p_house_obj, p_house_xml)
        self.read_rooms(p_house_obj, p_house_xml)
        House_Data[0] = p_house_obj
        if g_debug > 1:
            print "house.read_house() - Loading XML data for House:{0:}".format(p_house_obj.Name)
        return House_Data

    def write_house(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = self.xml_create_common_element('House', p_house_obj)
        if g_debug > 2:
            print "house.write_house() - Name:{0:}, Key:{1:}".format(p_house_obj.Name, p_house_obj.Key)
        return l_house_xml


class LoadSaveAPI(HouseReadWriteConfig):
    """
    """

    def get_house_obj(self):
        return self.m_house_obj


class API(LoadSaveAPI):
    """
    """

    def __init__(self):
        """Create a house object for when we add a new house.
        """
        global g_logger
        g_logger = logging.getLogger('PyHouse.House   ')
        if g_debug >= 1:
            print "house.API.__init__()"
        self.m_house_obj = HouseData()
        self.m_house_obj.ScheduleAPI = schedule.API(self.m_house_obj)

    def Start(self, _p_houses_obj, p_house_xml):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        self.read_house(self.m_house_obj, p_house_xml)
        if g_debug >= 1:
            print "house.API.Start() - House:{0:}, Active:{1:}, Key:{2:}".format(self.m_house_obj.Name, self.m_house_obj.Active, self.m_house_obj.Key)
        g_logger.info("Starting House {0:}.".format(self.m_house_obj.Name))
        self.m_house_obj.InternetAPI = internet.API(self.m_house_obj, p_house_xml)
        self.m_house_obj.ScheduleAPI.Start(self.m_house_obj, p_house_xml)
        self.m_house_obj.InternetAPI.Start()
        if g_debug >= 1:
            print "house.API.Start() has found -  Rooms:{0:}, Schedule:{1:}, Lights:{2:}, Controllers:{3:}".format(
                    len(self.m_house_obj.Rooms), len(self.m_house_obj.Schedule), len(self.m_house_obj.Lights), len(self.m_house_obj.Controllers))
        g_logger.info("Started.")
        return self.m_house_obj


    def Stop(self, p_xml):
        """Stop all houses.
        Return a filled in XML for the house.
        """
        if g_debug >= 1:
            print "\nhouse.Stop() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Stopping House:{0:}.".format(self.m_house_obj.Name))
        l_house_xml = self.write_house(self.m_house_obj)
        l_house_xml.append(self.write_location(self.m_house_obj.Location))
        l_house_xml.append(self.write_rooms(self.m_house_obj.Rooms))
        l_house_xml.extend(self.m_house_obj.ScheduleAPI.Stop(l_house_xml))
        l_house_xml.append(self.m_house_obj.InternetAPI.Stop())
        g_logger.info("Stopped.")
        if g_debug >= 1:
            print "house.Stop() - Name:{0:}, Count:{1:}".format(self.m_house_obj.Name, len(l_house_xml))
        return l_house_xml

    def SpecialTest(self):
        if g_debug > 0:
            print "house.API.SpecialTest()"
        self.m_house_obj.ScheduleAPI.SpecialTest()

# ##  END DBK
