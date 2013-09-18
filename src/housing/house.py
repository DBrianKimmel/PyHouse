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
# 1 = log extra info
# 2 = major routine entry
# 3 = get/put xml config info
# + = NOT USED HERE
g_logger = None


class HouseData(object):

    def __init__(self):
        self.Active = False
        self.Key = 0
        self.Name = ''
        self.InternetAPI = None
        self.LightingAPI = None
        self.ScheduleAPI = None
        self.FamilyData = None
        self.Location = location.LocationData()
        self.Buttons = {}
        self.Controllers = {}
        self.Internet = {}
        self.Lights = {}
        self.Rooms = {}
        self.Schedules = {}

    def __str__(self):
        l_ret = ' House:: '
        l_ret += 'Name:{0:}, '.format(self.Name)
        l_ret += "Active:{0:}, ".format(self.Active)
        l_ret += "Key:{0:}, ".format(self.Key)
        l_ret += "Lights:{0:}, ".format(len(self.Lights))
        l_ret += "Controllers:{0:}, ".format(len(self.Controllers))
        l_ret += "Buttons:{0:}, ".format(len(self.Buttons))
        l_ret += "Rooms:{0:}, ".format(len(self.Rooms))
        l_ret += "Schedules:{0:};\n".format(len(self.Schedules))
        return l_ret

    def __repr__(self):
        l_ret = "{"
        l_ret += "'Name':'{0:}', ".format(self.Name)
        l_ret += "'Key':'{0:}', ".format(self.Key)
        l_ret += "'Active':'{0:}', ".format(self.Active)
        l_ret += "'Lights':'{0:}', ".format(len(self.Lights))
        l_ret += "'Controllers':'{0:}', ".format(len(self.Controllers))
        l_ret += "'Buttons':'{0:}', ".format(len(self.Buttons))
        l_ret += "'Rooms':'{0:}', ".format(len(self.Rooms))
        l_ret += "'Internet':'{0:}', ".format(len(self.Internet))
        l_ret += "'Schedules':'{0:}'".format(len(self.Schedules))
        return l_ret

    def reprJSON(self):
        return dict(Active = self.Active, Key = self.Key, Name = self.Name, Location = self.Location)


class HouseReadWriteConfig(location.ReadWriteConfig, rooms.ReadWriteConfig):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def read_house_xml(self, p_house_obj, p_house_xml):
        """Read house information, location and rooms.
        """
        self.xml_read_common_info(p_house_obj, p_house_xml)
        p_house_obj.Location = self.read_location_xml(p_house_obj, p_house_xml)
        p_house_obj.Rooms = self.read_rooms_xml(p_house_obj, p_house_xml)
        if g_debug >= 3:
            print "house.read_house_xml() - Loading XML data for House:{0:}".format(p_house_obj.Name)
        return p_house_obj

    def write_house_xml(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = self.xml_create_common_element('House', p_house_obj)
        if g_debug >= 3:
            print "house.write_house_xml() - Name:{0:}, Key:{1:}".format(p_house_obj.Name, p_house_obj.Key)
        return l_house_xml


class API(HouseReadWriteConfig):
    """
    """

    def __init__(self):
        """Create a house object for when we add a new house.
        """
        global g_logger
        g_logger = logging.getLogger('PyHouse.House   ')
        if g_debug >= 1:
            print "house.API()"
        self.m_house_obj = HouseData()

    def Start(self, p_house_xml):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        if g_debug >= 2:
            print "house.API.Start() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Starting House {0:}.".format(self.m_house_obj.Name))
        self.read_house_xml(self.m_house_obj, p_house_xml)
        self.m_house_obj.ScheduleAPI = schedule.API(self.m_house_obj)
        self.m_house_obj.InternetAPI = internet.API()
        self.m_house_obj.ScheduleAPI.Start(self.m_house_obj, p_house_xml)
        self.m_house_obj.InternetAPI.Start(self.m_house_obj, p_house_xml)
        if g_debug >= 2:
            print "house.API.Start() has found -  Rooms:{0:}, Schedule:{1:}, Lights:{2:}, Controllers:{3:}".format(
                    len(self.m_house_obj.Rooms), len(self.m_house_obj.Schedules), len(self.m_house_obj.Lights), len(self.m_house_obj.Controllers))
        g_logger.info("Started. - House:{0:}".format(self.m_house_obj.Name))
        return self.m_house_obj


    def Stop(self, p_xml, p_house_obj):
        """Stop all houses.
        Return a filled in XML for the house.
        """
        if g_debug >= 2:
            print "\nhouse.API.Stop() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Stopping House:{0:}.".format(self.m_house_obj.Name))
        l_house_xml = self.Reload(p_house_obj)
        if g_debug >= 2:
            print "house.API.Stop() - Name:{0:}, Count:{1:}".format(self.m_house_obj.Name, len(l_house_xml))
        g_logger.info("Stopped.")
        return l_house_xml

    def Reload(self, p_house_obj):
        if g_debug >= 2:
            print "house.API.Reload()", p_house_obj
        g_logger.info("Reloading.")
        l_house_xml = self.write_house_xml(p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj))
        l_house_xml.extend(self.m_house_obj.ScheduleAPI.Stop(l_house_xml, p_house_obj))
        l_house_xml.append(self.m_house_obj.InternetAPI.Reload())
        g_logger.info("Reloaded.")
        return l_house_xml

    def SpecialTest(self):
        if g_debug >= 2:
            print "house.API.SpecialTest()"
        self.m_house_obj.ScheduleAPI.SpecialTest()

# ##  END DBK
